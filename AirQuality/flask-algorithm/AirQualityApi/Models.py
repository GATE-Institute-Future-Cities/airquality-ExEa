class PollutantWithValues:
    def __init__(self, pollutant, mean, lowerBound, upperBound):
        self.pollutant = pollutant
        self.mean = mean
        self.lowerBound = lowerBound
        self.upperBound = upperBound


class HeatmapValue:
    def __init__(self, longitude, latitude, value):
        self.longitude = longitude
        self.latitude = latitude
        self.value = value


class Station:
    def __init__(self, station, longitude, latitude, operator, locationName):
        self.station = station
        self.longitude = longitude
        self.latitude = latitude
        self.operator = operator
        self.locationName = locationName
