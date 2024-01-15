import statistics

from collections import Counter

from ..models import Request
from ..sql import mLHistoryCmd




def getRequest(*, awayML=None, homeML=None, teamML=None, awaySpread=None, homeSpread=None, spread=None, total=None, hA="home"):

    andCmd = ""
    if awayML:
        andCmd += " AND away.money = ? "
    if homeML:
        andCmd += " AND home.money = ? "
    if teamML:
        andCmd += " AND {}.money = ? ".format(hA)
    if awaySpread:
        andCmd += " AND away.spread = ? "
    if homeSpread:
        andCmd += " AND home.spread = ? "
    if spread:
        andCmd += " AND {}.spread = ? ".format(hA)
    if total:
        andCmd += " AND ou = ? "

    req = Request()
    args = []
    for value in (awayML, homeML, teamML, awaySpread, homeSpread, spread, total):
        if value:
            args.append(value)

    req.args = tuple(args)
    req.cmd = mLHistoryCmd.format(andCmd)
    req.fetch = "fetchAll"
    req.labels =  ("homeML", "homeWin", "homeCover", "homeSpread", "homeResult",
                    "awayML", "awayWin", "awayCover", "awaySpread", "awayResult",
                    "oU", "ouOutcome", "total")

    return req


def countResults(answer):
    total = len(answer)
    result = {"away":{}, "home":{}}
    result["gp"] = total
    try:
        for hA in ("away", "home"):
            ML = statistics.mean([int(x["{}ML".format(hA)]) for x in answer if x["{}ML".format(hA)]])

            wins = sum([item["{}Win".format(hA)] for item in answer if item["{}Win".format(hA)] == 1])
            covers = sum([item["{}Cover".format(hA)] for item in answer if item["{}Cover".format(hA)] == 1])
            overs = sum([item["ouOutcome"] for item in answer if item["ouOutcome"] == 1])
            unders = sum([item["ouOutcome"] for item in answer if item["ouOutcome"] == -1])

            spreadBoxes  = [x["{}Result".format(hA)] for x in answer]

            result[hA]["spreadCount"] = Counter(spreadBoxes)
            result[hA]["spreadBoxes"] = spreadBoxes

            result[hA]["ML"] =  int(ML) if int(ML)  < 0 else "+"+str(int(ML))
            result[hA]["cover%"] = covers /total*100
            result[hA]["win%"] = wins /total*100
            result[hA]["over%"] = overs / total*100

            result[hA]["spread"] = statistics.median([x["{}Spread".format(hA)] for x in answer if x["{}Spread".format(hA)]])
            result[hA]["result"] = statistics.median([x["{}Result".format(hA)] for x in answer if x["{}Spread".format(hA)]])
            result[hA]["oU"] = statistics.median([x["oU"] for x in answer if x["oU"]])
            result[hA]["total"] = statistics.median([x["total"] for x in answer if x["total"]])


            if ML > 0:
                result[hA]["winROI"] = (((ML+100)*wins)-total*100)/total
            elif ML <0:
                result[hA]["winROI"] = (((  (10000/ML*-1)  +100)*wins)-total*100)/total

            result[hA]["coverROI"] = ((covers*191.91)-total*100)/total
            result[hA]["overROI"] = ((overs*191.91)-total*100)/total
            result[hA]["underROI"] = ((unders*191.91)-total*100)/total
    except:
        result = {"away":{}, "home":{}}
        result["gp"] = 0

    return result
