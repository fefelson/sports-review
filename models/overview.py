from json import load
from pprint import pprint

from ..sql import overviewCmd, basketballPlayerReportCmd, teamReportCmd
from .threading_db import Request


class Overview:

    _options = {"hAJoin": "",
                "whereCmd": ""}

    def __init__(self, league):

        self.league = league
        self.playerReports = {}
        self.teamReports = {}

        self.league.dB.run(self.makePlayerReport())
        self.league.dB.run(self.makeTeamReport())


    def makePlayerReport(self):
        req = Request()
        req.args = (self.league.season, )
        req.callback = self.playerScore
        req.cmd = self._playerReportCmd
        req.fetch = "fetchAll"
        req.labels = self._playerReportLabels
        return req


    def makeTeamReport(self):
        req = Request()
        req.args = (self.league.season, )
        req.callback = self.teamScore
        req.cmd = teamReportCmd
        req.fetch = "fetchAll"
        req.labels = ("win%", "cover%", "over%", "under%", "teamMoneyROI", "teamSpreadROI", "overROI",
                        "underROI", "offEff", "defEff", "score", "poss",
                        "pts", "fga", "fgm", "fg%", "fta", "ftm", "ft%", "tpa",
                        "tpm", "tp%", "tov%", "oreb%", "dreb%",
                        )
        return req


    def playerScore(self, info):
        for key in info[0].keys():

            values = sorted([x[key] for x in info if x[key]])
            sDict = {}

            sDict[9] = values[int(.95*len(values))]
            sDict[8] = values[int(.9*len(values))]
            sDict[6] = values[int(.65*len(values))]
            sDict[4] = values[int(.35*len(values))]
            sDict[2] = values[int(.1*len(values))]
            sDict[1] = values[int(.05*len(values))]

            self.playerReports[key] = sDict.copy()



    def teamScore(self, info):
        for key in info[0].keys():

            values = sorted([x[key] for x in info if x[key]])
            sDict = {}

            sDict[9] = values[int(.9*len(values))]
            sDict[8] = values[int(.8*len(values))]
            sDict[6] = values[int(.6*len(values))]
            sDict[4] = values[int(.4*len(values))]
            sDict[2] = values[int(.2*len(values))]
            sDict[1] = values[int(.1*len(values))]

            self.teamReports[key] = sDict.copy()


    def getPlayerBackgroundColor(self, key, value, reverse=False):
        # print("key "+key, "value "+str(value), "reverse=" + str(reverse), end="\n\n")

        color = "grey"
        textColor = "black"
        colors = ["gold", "green", "pale green", "white", "pink", "red", "grey"]
        values = [1,2,4,6,8,9] if reverse else [9,8,6,4,2,1]

        labelColors = dict(zip(values, colors))
##        pprint(self.report[label][key])
##        pprint(labelColors)

        levels = self.playerReports[key]
        # print(levels)
        color = "red"

        if value != None:
            for k in values[:-2]:
                # print(k, levels[k], value, value >= levels[k])
                if reverse:
                    if value <= float(levels[k]):
                        color = labelColors[k]
                        break
                else:
                    # print(float(value) >= float(levels[k]))
                    if float(value) >= float(levels[k]):
                        # print(str(value) +" >= " + str(levels[k]))
                        color = labelColors[k]
                        break

            if color in ('green', 'red', 'grey'):
                textColor = "white"

            # print(k, color, textColor)
            # input("\n\n\n")
        return (color, textColor)


    def getTeamBackgroundColor(self, key, value, reverse=False):
        # print("key "+key, "value "+str(value), "reverse=" + str(reverse), end="\n\n")

        color = "grey"
        textColor = "black"
        colors = ["gold", "green", "pale green", "white", "pink", "red", "grey"]
        values = [1,2,4,6,8,9] if reverse else [9,8,6,4,2,1]

        labelColors = dict(zip(values, colors))
##        pprint(self.report[label][key])
##        pprint(labelColors)

        levels = self.teamReports[key]
        # print(levels)
        color = "red"
        if value != None:
            for k in values[:-1]:
                # print(k, levels[k], value, value >= levels[k])
                if reverse:
                    if value <= float(levels[k]):
                        color = labelColors[k]
                        break
                else:
                    # print(float(value) >= float(levels[k]))
                    if float(value) >= float(levels[k]):
                        # print(str(value) +" >= " + str(levels[k]))
                        color = labelColors[k]
                        break

            textColor = "black"
            if color in ('green', 'red', 'grey'):
                textColor = "white"

        # print(k, color, textColor)
        # input("\n\n\n")
        return (color, textColor)



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



class NBAOverview(Overview):

    _playerReportCmd = basketballPlayerReportCmd.format(", AVG(plmn)")
    _playerReportLabels = ("gp", "start%", "fga", "fgm", "fg%", "fta", "ftm",
                            "ft%", "tpa", "tpm", "tp%", "pts", "oreb", "reb", "ast",
                            "stl", "blk", "trn", "fls", "mins", "plmn")

    def __init__(self, league):
        super().__init__(league)



class NCAABOverview(Overview):

    _playerReportCmd = basketballPlayerReportCmd.format("")
    _playerReportLabels = ("gp", "start%", "fga", "fgm", "fg%", "fta", "ftm",
                            "ft%", "tpa", "tpm", "tp%", "pts", "oreb", "reb", "ast",
                            "stl", "blk", "trn", "fls", "mins")

    def __init__(self, league):
        super().__init__(league)
