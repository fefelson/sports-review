from .threading_db import Request, Event

from ..sql import nbaNewPlayerCmd, ncaabPlayerStatsCmd

class Player:

    _info = { "fullName": "n/a",
              "pos": "n/a",
              "inj": "n/a",
              }

    def __init__(self, team=None, playerInfo=None):

        self.playerId = playerInfo["playerId"]
        self.team = team
        self.info = playerInfo


    def newStatAvgs(self):
        req = Request()
        req.args = (self.playerId,)
        req.callback = self.setPlayerStats
        req.cmd = self._playerStatsCmd.format(self.team.getActiveSql())
        req.fetch = "fetchOne"
        req.labels = self._playerStatsLabels
        return req


    def setPlayerInfo(self, info):
        self.info = info.copy()



    def getValueColor(self, key, value, reverse=False):
        backColor = "grey"
        textColor = "black"
        try:
            backColor, textColor = self.team.league.overview.getPlayerBackgroundColor(key, value, reverse)
        except:
            pass
        return backColor, textColor


    def getItem(self, item):

        value = None
        value = self.info.get(item, "--")
        return value


class NBAPlayer(Player):

    _newPlayerCmd = nbaNewPlayerCmd
    _newPlayerLabels = ("playerId", "fullName", "pos", "gp", "start%", "fga", "fgm",
                    "fg%", "fta", "ftm", "ft%", "tpa", "tpm", "tp%", "pts",
                    "oreb", "reb", "ast", "stl", "blk", "trn", "fls", "mins", "plmn")

    def __init__(self, team, playerInfo):
        super().__init__(team, playerInfo)





class NCAABPlayer(Player):

    _newPlayerCmd = ncaabPlayerStatsCmd
    _newPlayerLabels = ("playerId", "fullName", "pos", "gp", "start%", "fga", "fgm",
                    "fg%", "fta", "ftm", "ft%", "tpa", "tpm", "tp%", "pts",
                    "oreb", "reb", "ast", "stl", "blk", "trn", "fls", "mins")

    def __init__(self, team, playerInfo):
        super().__init__(team, playerInfo)
