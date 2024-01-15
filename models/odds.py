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
            for key, value in [(key, value) for key, value in odds.items() if key != "timestamp"]:
                book = self.odds.get(key, None)
                if not book:
                    book = deepcopy(self._book)
                    book["bookName"] = value["book_name"]

                timestamp = odds["timestamp"]

                if is_number(value["away_ml"]) or is_number(value["home_ml"]):
                    temp = self._money.copy()
                    try:
                        temp["awayML"] = float(value["away_ml"])
                    except:
                        temp["awayML"] = None
                    try:
                        temp["homeML"] = float(value["home_ml"])
                    except:
                        temp["homeML"] = None

                    temp["timestamp"] = timestamp
                    book["money"].append(temp)


                if is_number(value["away_spread"]) or is_number(value["home_spread"]):
                    temp = self._spread.copy()
                    try:
                        temp["awaySpread"] = float(value["away_spread"])
                    except:
                        temp["awaySpread"] = None
                    try:
                        temp["homeSpread"] = float(value["home_spread"])
                    except:
                        temp["homeSpread"] = None

                    try:
                        temp["awayLine"] = float(value["away_line"])
                        temp["homeLine"] = float(value["home_line"])
                    except:
                        temp["awayLine"] = None
                        temp["homeLine"] = None

                    temp["timestamp"] = timestamp
                    book["spread"].append(temp)

                if is_number(value["total"]) and float(value["total"]) > 0:
                    temp = self._total.copy()
                    temp["total"] = float(value["total"])
                    temp["timestamp"] = timestamp
                    book["total"].append(temp)

            self.odds[key] = book



    def getBook(self, bookName="BetMGM"):
        book = None
        try:
            for key in self.odds.keys():
                if self.odds[key].get("bookName", None) == bookName:
                    book = self.odds[key]
        except KeyError:
            try:
                book = [x for x in self.odds.values()[-1]]
            except:
                book = None
        return book


    def getItem(self, group, item, *, bookName="BetMGM"):
        book = self.getBook(bookName)
        value = None
        for i in range(len(book[group])):
            x = book[group][(i+1)*-1].get(item, None)
            if x:
                value = x
                break
        return value
