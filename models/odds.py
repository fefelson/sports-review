from copy import deepcopy


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True



class GameOdds:

    _book = {"money": [], "spread": [], "total":[], "bookName": None}
    _money = {"awayML": None, "homeML": None, "timestamp": None}
    _spread = {"awayLine": None, "awaySpread": None, "homeSpread": None, "homeSpread": None, "timestamp": None}
    _total = {"total": None, "overLine": None, "underLine": None, "timestamp": None}

    def __init__(self, info):

        self.odds = {}

        for odds in info:
            timestamp = odds["timestamp"]
            for key, value in [(key, value) for key, value in odds.items() if key != "timestamp"]:
                book = self.odds.get(key, None)
                if not book:
                    book = self._book.copy()
                    book["bookName"] = value["book_name"]

                if is_number(value["away_ml"]) and is_number(value["home_ml"]):
                    temp = self._money.copy()
                    temp["awayML"] = float(value["away_ml"])
                    temp["homeML"] = float(value["home_ml"])
                    temp["timestamp"] = timestamp
                    book["money"].append(temp)

                if is_number(value["away_spread"]) and is_number(value["home_spread"]):
                    temp = self._spread.copy()
                    temp["awaySpread"] = float(value["away_spread"])
                    temp["homeSpread"] = float(value["home_spread"])
                    temp["awayLine"] = float(value["away_line"])
                    temp["homeLine"] = float(value["home_line"])
                    temp["timestamp"] = timestamp
                    book["spread"].append(temp)

                if is_number(value["total"]) and float(value["total"]) > 0:
                    temp = self._total.copy()
                    temp["total"] = float(value["total"])
                    temp["overLine"] = float(value["over_line"])
                    temp["underLine"] = float(value["under_line"])
                    temp["timestamp"] = timestamp
                    book["total"].append(temp)

                self.odds[book["bookName"]] = deepcopy(book)


    def getItem(self, group, item, *, bookName="BetMGM"):
        try:
            book = self.odds[bookName]
        except KeyError:
            try:
                book = [x for x in self.odds.values()[-1]]
            except:
                book = None

        try:
            value = book[group][-1][item]
        except:
            value = self._book = {"money": self._money, "spread": self._spread, "total":self._total, "bookName": None}

        return value
