import datetime
import json
import os

from copy import deepcopy
from pprint import pprint
from scipy.optimize import minimize
from threading import Event

from .games import Game
from .overview import NBAOverview, NCAABOverview
from .players import NBAPlayer, NCAABPlayer
from ..sql import gameStatsCmd, mLHistoryCmd,atsHistoryCmd,  totalHistoryCmd
from .teams import NBATeam, NCAABTeam
from .threading_db import ThreadedDB, Request

from FelsonSports.DB import NBADB, NCAABDB

today = datetime.date.today()

def calculate_sos(weight, expected_results, actual_results):
    total_weighted_difference = 0

    # Iterate through each game
    for i in range(len(expected_results)):
        expected_score = expected_results[i]
        actual_score = actual_results[i]

        # Calculate the weighted difference between expected and actual results
        weighted_difference = ((weight * expected_score) - actual_score)**2

        # Accumulate the total weighted difference
        total_weighted_difference += weighted_difference

    # Return the total weighted difference as the objective to be minimized
    return total_weighted_difference



class League:

    _dB = None
    _gameDayPath = None
    _newGame = None
    _newPlayer = None
    _newTeam = None
    _overview = None
    _reportPath = None
    _setTeamsCmd = "SELECT team_id, abrv, first_name, last_name, conference, division, primary_color, secondary_color FROM teams"
    _setTeamLabels = ("teamId", "abrv", "firstName", "lastName", "conference", "division", "primaryColor", "secondColor")


    def __init__(self, season):

        self.season = season
        self.dB = ThreadedDB(self._dB)
        self.games = {}
        self.overview = self._overview(self)
        self.players = {}
        self.teams = {}

        self.dB.run(self.setTeams())
        for team in self.teams.values():
            self.dB.run(team.newGamePool())
            self.dB.run(team.newPlayers())
            self.dB.run(team.newTeamRecords())
            self.dB.run(team.newStatAvgs())
            self.dB.run(team.newTeamOdds())

        self.setTeamSOS()
        self.setGames()
        self.leagueSpecific()


    def _SOSWeights(self, team):
        weights = []

        for hA in ("away", "home"):
            results = team.getGameLog(homeAway=hA)
            expected_results = [r["spread"]*-1 for r in results if r["spread"] != None]
            actual_results = [r["result"] for r in results if r["spread"] != None]
            initial_weight = 0.5
            result = minimize(calculate_sos, initial_weight, args=(expected_results, actual_results))
            optimal_weight = result.x[0]

            weights.append(optimal_weight)
        return weights


    def getGameDayPath(self):
        """function meant to be overriden
        """
        raise AssertionError


    def getValueColor(self, label, key, value):
        color = "grey"
        try:
            color = self.overview.valueColor(label, key, value)
        except:
            pass
        return color


    def leagueSpecific(self):
        raise


    def getGameStats(self, gameId, oppId):
        """This function is put into a thread and sent to dB.run
        """
        req = Request()
        req.args = (gameId, oppId)
        req.callback = None
        req.cmd = gameStatsCmd
        req.fetch = "fetchOne"
        req.labels = ("offense_name",
                        "offense_poss", "offense_pts", "offense_fga", "offense_fgm",
                        "offense_fg%", "offense_fta", "offense_ftm", "offense_ft%", "offense_tpa",
                        "offense_tpm", "offense_tp%", "offense_tov%", "offense_oreb%", "offense_dreb%",
                         "defense_name",
                         "defense_poss", "defense_pts", "defense_fga", "defense_fgm", "defense_fg%",
                         "defense_fta", "defense_ftm", "defense_ft%", "defense_tpa", "defense_tpm",
                         "defense_tp%", "defense_tov%", "defense_oreb%", "defense_dreb%",)
        return req


    def getTotalView(self, gameId):
        """This function is put into a thread and sent to dB.run
        """
        game = self.games[gameId]
        book = game.odds.getBook()
        oU = None
        for i in range(len(book["total"])):
            x = book["total"][(i+1)*-1].get("total", None)
            if x:
                oU = x
                break

        req = Request()
        req.args = (oU,)
        req.cmd = totalHistoryCmd
        req.odds = game.odds
        req.fetch = "fetchAll"
        req.labels =  ("result", "outcome")

        return req


    def getOverview(self):
        """This function is put into a thread and sent to dB.run
        """
        options = self._options.copy()
        options["hAJoin"] = "(team.team_id = gm.home_id OR team.team_id = gm.away_id)"
        req = Request()
        req.args = (self.league.season, )
        req.callback = None
        req.cmd = overviewCmd.format(options)
        req.fetch = "fetchAll"
        req.labels = ("team", "gp", "win%", "ML", "moneyROI", "oppML", "oppROI",
                        "spread", "result", "cover%", "atsROI", "o/u", "total",
                        "over%", "overROI", "underROI", "teamId")
        return req


    def getTeam(self, teamId):
        return self.teams[teamId]


    def setGames(self):
        gameDayPath = self.getGameDayPath()
        # Iterate through files in gameDayPath that start with 'M'
        for fileName in [gameDayPath +fileName for fileName in os.listdir(gameDayPath) if fileName[0] == "M"]:
            # Create a new Game object

            with open(fileName) as fileIn:

                info = json.load(fileIn)
                if datetime.datetime.strptime(info["gameTime"], "%a, %d %b %Y %H:%M:%S %z").timestamp():# > datetime.datetime.now().timestamp():

                    self.games[info["gameId"]] = self._newGame(self, info)
                    # for hA in ("away", "home"):
                    #     teamId = info["teams"][hA]["teamId"]
                    #     players = info["players"][hA]
                    #
                    #     try:
                    #         self.teams[teamId].setPlayers(players)
                    #     except KeyError:
                    #         self.teams[teamId] = self._newTeam(self, info["teams"][hA])
                    #         self.teams[teamId].setPlayers(players)



    def setTeamInfo(self, info):
        for team in info:
            newTeam = self._newTeam(self, team.copy())
            self.teams[team["teamId"]] = newTeam


    def setTeams(self):
        req = Request()
        req.callback = self.setTeamInfo
        req.cmd = self._setTeamsCmd
        req.fetch = "fetchAll"
        req.labels = self._setTeamLabels
        return req


    def setTeamSOS(self):

        maxValues = {}
        for i, team in enumerate(self.teams.values()):
            resultsPer = team.getOdds("result")/team.getStats("gp")
            oppPtsPer = team.getStats("defense_pts")/team.getStats("gp")
            awayWeight, homeWeight = self._SOSWeights(team)
            team.setSOSWeights(awayWeight, homeWeight)

            if i == 0:
                maxValues["resultsPer"] = resultsPer
                maxValues["oppPtsPer"] = oppPtsPer
                maxValues["awayWeight"] = awayWeight
                maxValues["homeWeight"] = homeWeight
            else:
                if resultsPer > maxValues["resultsPer"]:
                    maxValues["resultsPer"] = resultsPer

                if oppPtsPer > maxValues["oppPtsPer"]:
                    maxValues["oppPtsPer"] = oppPtsPer

                if awayWeight > maxValues["awayWeight"]:
                    maxValues["awayWeight"] = awayWeight

                if homeWeight > maxValues["homeWeight"]:
                    maxValues["homeWeight"] = homeWeight

        for team in self.teams.values():
            resultsPer = team.getOdds("result")/team.getStats("gp")
            oppPtsPer = team.getStats("defense_pts")/team.getStats("gp")
            awayWeight, homeWeight = team.getSOSWeights()

            oppPtsScore = (oppPtsPer+1)/(maxValues["oppPtsPer"]+1)*100
            victoryScore = ((resultsPer+10)/(maxValues["resultsPer"]+10))*100
            homeScore = ((homeWeight+.1)/(maxValues["homeWeight"]+.1))*50
            awayScore = ((awayWeight+.1)/(maxValues["awayWeight"]+.1))*50

            team.setSOS(oppPtsScore, victoryScore, homeScore, awayScore)


class NBA(League):

    _dB = NBADB
    _gameDayPath = "/home/ededub/FEFelson/nba/{}/{}/{}/"
    _leagueId = "nba"
    _newGame = Game
    _newPlayer = NBAPlayer
    _newTeam = NBATeam
    _overview = NBAOverview


    def __init__(self, season):
        super().__init__(season)


    def getGameDayPath(self):
        return self._gameDayPath.format(self.season, *str(today).split("-")[1:])


    def leagueSpecific(self):
        for team in self.teams.values():
            self.dB.run(team.newB2B())



class NCAAB(League):

    _dB = NCAABDB
    _gameDayPath = "/home/ededub/FEFelson/ncaab/{}/{}/{}/"
    _leagueId = "ncaab"
    _newGame = Game
    _newPlayer = NCAABPlayer
    _newTeam = NCAABTeam
    _overview = NCAABOverview
    _setTeamsCmd = "SELECT team_id, abrv, first_name, last_name, conference, primary_color, secondary_color FROM teams"
    _setTeamLabels = ("teamId", "abrv", "firstName", "lastName", "conference", "primaryColor", "secondColor")


    def __init__(self, season):
        super().__init__(season)


    def getGameDayPath(self):
        return self._gameDayPath.format(self.season, *str(today).split("-")[1:])


    def leagueSpecific(self):
        for team in self.teams.values():
            self.dB.run(team.newB2B())
