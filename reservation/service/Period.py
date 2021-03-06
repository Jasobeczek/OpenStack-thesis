import datetime
from dateutil import parser

class Period:

    id = None
    start = None
    stop = None
    laboratory_id = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.stop = kwargs.get("stop")
        if self.stop is not None:
            self.stop = parser.parse(str(self.stop))
        self.start = kwargs.get("start")
        if self.start is not None:
            self.start = parser.parse(str(self.start))
        self.laboratory_id = kwargs.get("laboratory_id")

    def parseDict(self, dict):
        if "id" in dict:
            self.id = dict["id"]
        if "start" in dict:
            if isinstance(dict["start"], datetime.date):
                self.start = dict["start"]
            else:
                self.start = parser.parse(str(dict["start"]))
        if "stop" in dict:
            if isinstance(dict["stop"], datetime.date):
                self.stop = dict["stop"]
            else:
                self.stop = parser.parse(str(dict["stop"]))
        if "laboratory_id" in dict:
            self.laboratory_id = dict["laboratory_id"]
        return self

    def to_dict(self):
        return dict(id=self.id, start=str(self.start), stop=str(self.stop), laboratory_id=self.laboratory_id)


class Periods:

    period = []

    def __init__(self):
        self.period = []

    def parseJSON(self, data):
        if "periods" in data:
            for period in data["periods"]:
                if "start" in period and "stop" in period:
                    self.period.append(Period(start=period["start"], stop=period["stop"]))
                else:
                    continue
            return self
        else:
            return None

    def parseArray(self, array):
        for period in array:
            self.period.append(Period(id=period["id"], start=period["start"], stop=period["stop"], laboratory_id=period["laboratory_id"], ))

        return self

    def to_dict(self):
        newPeriod = []
        for period in self.period:
            newPeriod.append(period.to_dict())

        return newPeriod
