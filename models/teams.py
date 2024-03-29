from copy import deepcopy
from datetime import datetime, date, timedelta
import pytz
from statistics import mean, median, mode, stdev
from threading import Event

from .stats import BasketballTeamStats
from .threading_db import Request

from ..sql import b2BCmd, gamePoolCmd, teamOddsCmd, teamRecordsCmd, teamStatsCmd



class Team:

    _info = { "abrv": "n/a",
              "firstName": "n/a",
              "lastName": "n/a",
              "primaryColor": None,
              "secondColor": None,
              "teamId": -1,
              }

    _possValues = None

    def __init__(self, league=None, teamInfo=None):

        try:
            self._teamId = teamInfo["teamId"]
            self.teamInfo = teamInfo
        except:
            self._teamId = -1
            self.teamInfo = self._info.copy()

        self.activeGames = None
        self.gamePool = None
        self.league = league
        self.odds = {}
        self.players = {}
        self.gamePlayers = None
        self.records = {}
        self.sos = None
        self.stats = None


    def __str__(self,):
        return "Team{:6d}:   {}".format(*[self.teamInfo[x] for x in ("teamId", "abrv")])


    def getActiveGameIds(self):
        return [x["gameId"] for x in self.activeGames]


    def getActiveSql(self):
        # self.gamePoolEvent.wait()
        gameIds = self.getActiveGameIds()
        activeSql = "game_id = {}".format(gameIds[0]) if len(gameIds) <= 1 else "game_id IN {}".format(str(tuple(gameIds)))
        return activeSql


    def getColors(self):
        return [self.teamInfo[key] for key in ("primaryColor", "secondColor")]


    def getGameLog(self, *, homeAway=None):
        games = self.activeGames
        if homeAway:
            if homeAway == "away":
                games = [game for game in games if game["isHome"] == 0]
            elif homeAway == "home":
                games = [game for game in games if game["isHome"] == 1]
        return games.copy()


    def getGamePool(self):
        return deepcopy(self.gamePool)


    def getInfo(self, key):
        value = None
        if key == "leagueId":
            return self.league._leagueId
        return self.teamInfo.get(key, "--")


    def getOdds(self, key):
        return self.odds.get(key,None)


    def getPossessions(self):

        pace = {"boxes":[],}
        possValues = self._possValues
        tempBoxes = {0:[], 1:[], 2:[], 3:[], 4:[]}
        games = deepcopy(self.activeGames)
        values = [game["poss"] for game in games]
        pace["mean"] = mean(values)
        pace["median"] = median(values)
        pace["mode"] = mode(values)
        pace["std"] = stdev(values)

        for game in games:
            entered = False
            poss = game["poss"]
            for i, val in enumerate(possValues):
                if poss <= val:
                    tempBoxes[i].append(game)
                    entered = True
                    break
            if not entered:
                tempBoxes[len(possValues)].append(game)

        length = len(tempBoxes.keys())
        for i in range(length):
            paceBox = {"win%":0, "spread%":0, "over%":0, "spread":0, "o/u":0}
            paceBox["gp"] = len(tempBoxes[i])
            if i == 0:
                paceBox["title"] = "under {}".format(possValues[i])
            elif i == length - 1:
                paceBox["title"] = "over {}".format(possValues[-1])
            else:
                paceBox["title"] = "{} - {}".format(possValues[i-1], possValues[i])

            if len([x for x in tempBoxes[i] if x["spread"] != None]):
                paceBox["win%"] = sum([game["isWinner"] for game in tempBoxes[i] if game["isWinner"] ==1]) / len(tempBoxes[i]) *100

                paceBox["spread%"] = sum([game["isCover"] for game in tempBoxes[i] if game["isCover"] ==1]) / len([x for x in tempBoxes[i] if x["spread"] != None]) *100

                paceBox["over%"] = sum([game["isOver"] for game in tempBoxes[i] if game["isOver"] ==1 and game["o/u"] != None]) / len([x for x in tempBoxes[i] if x["o/u"] != None]) *100

                paceBox["spread"] = sum([game["spread"] for game in tempBoxes[i] if game["spread"] != None]) / len([x for x in tempBoxes[i] if x["spread"] != None])

                paceBox["o/u"] = sum([game["o/u"] for game in tempBoxes[i] if game["o/u"] != None]) / len([x for x in tempBoxes[i] if x["o/u"] != None])

                paceBox["opp"] = [(game["gameId"], game["oppId"]) for game in tempBoxes[i]]
            pace["boxes"].append(deepcopy(paceBox))
        return deepcopy(pace)


    def getRecords(self, key):
        return self.records.get(key,None)


    def getSOSWeights(self):
        return [self.sos[key] for key in ("awayWeight", "homeWeight")]


    def getSOS(self, key):
        return self.sos[key]


    def getStats(self, stat):
        value = None
        try:
            value = self.stats.getValue(stat)
        except:
            value = "--"
        return value


    def getTeamStats(self):
        """This function is put into a thread and sent to dB.run
        """
        req = self.newStatAvgs()
        req.callback = None
        return req


    def getValueColor(self, key, value, reverse=False):
        return self.league.overview.getTeamBackgroundColor(key, value, reverse)


    def newGamePool(self):
        req = Request()
        req.args = (self.league.season, self._teamId)
        req.callback = self.setGamePool
        req.cmd = gamePoolCmd.format(self.league._leagueId)
        req.fetch = "fetchAll"
        req.labels = ("leagueId", "gameId", "gameDate", "oppId", "poss", "teamPts", "oppPts", "isHome",
                        "isWinner", "result", "money", "spread", "total", "o/u", "isCover", "isOver")
        return req


    def newPlayers(self):
        req = Request()
        req.args = (self._teamId,)
        req.callback = self.setPlayers
        req.cmd = self.league._newPlayer._newPlayerCmd.format(self.getActiveSql())
        req.fetch = "fetchAll"
        req.labels = self.league._newPlayer._newPlayerLabels
        return req


    def newStatAvgs(self):
        req = Request()
        req.args = (self._teamId,)
        req.callback = self.setStatAvgs
        req.cmd = teamStatsCmd.format(self.getActiveSql())
        req.fetch = "fetchOne"
        req.labels = ("team_gp", "team_offEff", "team_defEff", "team_score", "team_poss",
                        "offense_poss", "offense_pts", "offense_fga", "offense_fgm",
                        "offense_fg%", "offense_fta", "offense_ftm", "offense_ft%", "offense_tpa",
                        "offense_tpm", "offense_tp%", "offense_tov%", "offense_oreb%", "offense_dreb%",
                         "defense_poss", "defense_pts", "defense_fga", "defense_fgm", "defense_fg%",
                         "defense_fta", "defense_ftm", "defense_ft%", "defense_tpa", "defense_tpm",
                         "defense_tp%", "defense_tov%", "defense_oreb%", "defense_dreb%",)
        return req


    def newTeamOdds(self):
        req = Request()
        req.args = (self._teamId,)
        req.callback = self.setTeamOdds
        req.cmd = teamOddsCmd.format(self.getActiveSql())
        req.fetch = "fetchOne"
        req.labels = ("spread", "result", "money", "teamSpreadROI", "teamMoneyROI",
                        "oppSpreadROI", "oppMoneyROI", "o/u", "total", "overROI", "underROI")
        return req


    def newTeamRecords(self):
        req = Request()
        req.args = (self._teamId,)
        req.callback = self.setRecords
        req.cmd = teamRecordsCmd.format(self.getActiveSql())
        req.fetch = "fetchOne"
        req.labels = ("gameWin", "gameLoss", "gamePush", "win%", "spreadWin","spreadLoss",
                        "spreadPush", "cover%", "totalOver", "totalUnder", "totalPush",
                        "over%",)
        return req



    def setActiveGames_to_GamePool(self):
        self.activeGames = self.gamePool


    def setGamePool(self, gamePool):
        assert isinstance(gamePool, list)
        for game in gamePool:
            game["gameDate"] = datetime.strptime(game["gameDate"], "%a, %d %b %Y %H:%M:%S %z").astimezone(pytz.timezone('US/Eastern'))
        self.gamePool = gamePool
        self.setActiveGames_to_GamePool()


    def setPlayers(self, players):
        for info in players:
            self.players[info["playerId"]] = self.league._newPlayer(team=self, playerInfo=info)



    def getPlayers(self, *, item="pts"):
        players = sorted(self.players.values(), key=lambda player: player.getItem(item), reverse=True)
        return players



    def setRecords(self, records):
        self.records = records.copy()


    def setSOS(self, oppPtsScore, victoryScore, homeScore, awayScore):
        self.sos["oppPtsScore"] = oppPtsScore
        self.sos["victoryScore"] = victoryScore
        self.sos["homeScore"] = homeScore
        self.sos["awayScore"] = awayScore
        self.sos["SOS"] = oppPtsScore+victoryScore+homeScore+awayScore


    def setSOSWeights(self, awayWeight, homeWeight):
        self.sos={}
        self.sos["awayWeight"] = awayWeight
        self.sos["homeWeight"] = homeWeight


    def setStatAvgs(self, stats):
        self.stats = BasketballTeamStats(stats)


    def setTeamOdds(self, odds):
        self.odds = odds.copy()


class NBATeam(Team):

    _b2B = False
    _possValues = (193, 198, 203, 209)

    def __init__(self, league=None, teamInfo=None):
        super().__init__(league, teamInfo)

        self.b2B = False


    def newB2B(self):
        yesterday = date.today() - timedelta(1)
        req = Request()
        req.args = (yesterday.year, "{}.{}".format(*str(yesterday).split("-")[1:]), self._teamId)
        req.callback = self.setB2B
        req.cmd = b2BCmd
        req.fetch = "fetchItem"
        req.labels = ( "gameId",)
        return req


    def setB2B(self, item):
        self.b2B = True if item else False


class NCAABTeam(Team):

    _b2B = False
    _possValues = (127, 133, 138, 145)

    def __init__(self, league=None, teamInfo=None):
        super().__init__(league, teamInfo)

        self.b2B = False


    def newB2B(self):
        yesterday = date.today() - timedelta(1)
        req = Request()
        req.args = (yesterday.year, "{}.{}".format(*str(yesterday).split("-")[1:]), self._teamId)
        req.callback = self.setB2B
        req.cmd = b2BCmd
        req.fetch = "fetchItem"
        req.labels = ( "gameId",)
        return req


    def setB2B(self, item):
        self.b2B = True if item else False
