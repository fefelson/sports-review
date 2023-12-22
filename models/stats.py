

class BasketballTeamStats:

    def __init__(self, stats):

        self.stats = {"team":{}, "offense": {}, "defense": {}}

        for key, value in stats.items():
            tag, key = key.split("_")
            self.stats[tag][key] = value



    def getValue(self, stat):
        value = None
        if stat in ("offEff", "defEff", "score", "poss", "gp"):
            value = self.stats["team"][stat]
        else:
            try:
                tag, stat = stat.split("_")
            except:
                tag = "offense"
            value = self.stats[tag][stat]
        return value
