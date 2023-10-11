import codecs
import csv

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_cors import CORS
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from Models import PollutantWithValues, HeatmapValue, Station

app = Flask(__name__)
api = Api(app)
CORS(app)
class AirPollutantsResponseSchema(Schema):
    pollutant = fields.String()
    mean = fields.Float()
    lowerBound = fields.Float()
    upperBound = fields.Float()


class AirPollutantsRequestSchema(Schema):
    longitude = fields.Float(required=True, description="Location longitude")
    latitude = fields.Float(required=True, description="Location latitude")


class HeatmapResponseSchema(Schema):
    longitude = fields.Float()
    latitude = fields.Float()
    value = fields.Float()


class StationsRequestResponseSchema(Schema):
    station = fields.String()
    longitude = fields.Float()
    latitude = fields.Float()
    operator = fields.String()
    locationName = fields.String()


class PollutantsApi(MethodResource, Resource):

    @doc(description='List of analyzed levels of pollutants for a specific location.', tags=['Air Pollutants API'])
    @use_kwargs(AirPollutantsRequestSchema, location='json')
    @marshal_with(AirPollutantsResponseSchema(many=True))
    def post(self, **kwargs):
        pollutants = read_pollutants_from_csv(
            "C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/pollutants.csv")
        return pollutants


api.add_resource(PollutantsApi, '/airQuality')


class HeatmapApi(MethodResource, Resource):

    @doc(description='When latitude and longitude parameters are sent, this API returns mean value for the air quality in the selected location.', tags=['Heatmap data API'])
    @use_kwargs(AirPollutantsRequestSchema, location='json')
    @marshal_with(HeatmapResponseSchema)
    def post(self, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']

        heatmap_values = read_heatmap_from_csv("C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/heatmapvaluescoloring.csv")

        for heatmap_value in heatmap_values:
            if abs(float(heatmap_value.latitude) - latitude) <= 0.002 \
                    and abs(float(heatmap_value.longitude) - longitude) <= 0.002:
                return heatmap_value

        return HeatmapValue(0.0, 0.0, 0.0)

    @doc(description='Returns all mean analyzed values for heatmap.', tags=['Heatmap data API'])
    @marshal_with(HeatmapResponseSchema(many=True))
    def get(self):
        print('get')
        return read_heatmap_from_csv("C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/heatmapvaluescoloring.csv")


api.add_resource(HeatmapApi, '/heatmap')


class AirQualityStationsApi(MethodResource, Resource):
    @doc(description='Get locations for all stations.', tags=['Air Quality Stations API'])
    @marshal_with(StationsRequestResponseSchema(many=True))
    def get(self):
        csv_file_path = 'C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/stationsdata.csv'
        stations = read_stations_from_csv(csv_file_path)
        return stations

    @doc(description='Insert new station.', tags=['Air Quality Stations API'])
    @use_kwargs(StationsRequestResponseSchema, location='json')
    @marshal_with(StationsRequestResponseSchema)
    def post(self, **kwargs):
        station = kwargs['station']
        longitude = kwargs['longitude']
        latitude = kwargs['latitude']
        operator = kwargs['operator']
        location_name = kwargs['locationName']
        new_station = Station(station, longitude, latitude, operator, location_name)
        write_station_to_csv(new_station, 'C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/stationsdata.csv')
        return new_station


api.add_resource(AirQualityStationsApi, '/stations')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Air Quality APIs',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

docs.register(PollutantsApi)
docs.register(HeatmapApi)
docs.register(AirQualityStationsApi)



def read_stations_from_csv(file_path):
    stations = []
    with open(file_path, 'r', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            station2 = Station(*row)
            stations.append(station2)
    return stations


def write_station_to_csv(station, file_path):
    with codecs.open(file_path, 'a', encoding='cp1252') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([station.station, station.longitude, station.latitude, station.operator, station.locationName])


def read_pollutants_from_csv(file_path):
    pollutants = []
    with open(file_path, 'r', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            pollutant = PollutantWithValues(*row)
            pollutants.append(pollutant)
    return pollutants


def read_heatmap_from_csv(file_path):
    heatmap_values = []
    with open(file_path, 'r', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            heatmap_value = HeatmapValue(*row)
            heatmap_values.append(heatmap_value)
    return heatmap_values

# # Usage example
csv_file_path = 'C:/Users/35987/Desktop/MSc Thesis/AirQuality/flask-algorithm/AirQualityApi/DemoData/stationsdata.csv'
stations = read_stations_from_csv(csv_file_path)

# # Accessing the station objects in the list
for station in stations:
    print(station.station, station.longitude, station.latitude, station.operator, station.locationName)
    
if __name__ == '__main__':
    app.run(debug=True)
