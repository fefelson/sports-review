import pytz

from datetime import datetime

from .odds import GameOdds



class Game:


    def __init__(self, league, info=None):

        self.league = league
        self.info = info
        try:
            self.gameId = info["gameId"]
            self.gameTime = datetime.strptime(info["gameTime"], "%a, %d %b %Y %H:%M:%S %z").astimezone(pytz.timezone('US/Eastern'))
            self.injuries = info["injuries"]
            self.odds = GameOdds(info["odds"])
            self.teams = {"away":info["awayId"], "home":info["homeId"]}
        except KeyError:
            self.injuries = None
            self.odds = None
            self.teams = {"away": -1, "home": -1}


    def getGamedate(self):
        return self.gameTime


    def getInfo(self, key):
        value = None
        if key == "gameId":
            value = self.gameId
        elif key == "leagueId":
            value = self.league._leagueId
        elif key == "gameTime":
            value = self.gameTime
        return value


    def getOdds(self):
        return self.odds


    def getTeam(self, hA):
        teamId = int(self.teams[hA])
        team = self.league.teams.get(teamId, None)
        if team == None:
            team = self.league._newTeam(self.league, self.info["teams"][hA])
            self.league.teams[teamId] = team
        return team
