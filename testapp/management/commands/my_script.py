import os
import json
import logging
from django.core.management.base import BaseCommand
from weather_shared_model.database_model.models import WeatherForecast, WeatherTimeSeries

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()  # Sends logging output to the console
logger.addHandler(console_handler)

class Command(BaseCommand):
    help = 'My periodic data processing script'

    def handle(self, *args, **options):
        logger.debug("Extracting data from JSON file") 
        logger.info("Creating WeatherForecast object")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        data_file = os.path.join(base_dir, 'weather_shared_model', 'database_model', 'fixtures', 'forecast_2023-02-25_13_48_31')

        with open(data_file, 'r') as f:
            weather_data = json.load(f)

        for feature in weather_data['features']:
            properties = feature['properties']

            logger.debug("feature")

            # Create WeatherForecast object 
            forecast_object = WeatherForecast(
                model_run_date=properties['modelRunDate']
            )
            forecast_object.save()

            # Create WeatherTimeSeries objects for each item
            for timeseries_data in properties['timeSeries']:
                time_series_object = WeatherTimeSeries(
                    forecast=forecast_object,
                    time=timeseries_data['time'],
                    screen_temperature=timeseries_data['screenTemperature'],
                    max_screen_air_temp=timeseries_data['maxScreenAirTemp'] if 'maxScreenAirTemp' in timeseries_data else None,
                    min_screen_air_temp=timeseries_data['minScreenAirTemp'] if 'minScreenAirTemp' in timeseries_data else None,
                    screen_dew_point_temperature=timeseries_data['screenDewPointTemperature'],
                    feels_like_temperature=timeseries_data['feelsLikeTemperature'],
                    wind_speed_10m=timeseries_data['windSpeed10m'],
                    wind_direction_from_10m=timeseries_data['windDirectionFrom10m'],
                    wind_gust_speed_10m=timeseries_data['windGustSpeed10m'],
                    max_10m_wind_gust=timeseries_data['max10mWindGust'] if 'max10mWindGust' in timeseries_data else None,
                    visibility=timeseries_data['visibility'],
                    screen_relative_humidity=timeseries_data['screenRelativeHumidity'],
                    mslp=timeseries_data['mslp'],
                    uv_index=timeseries_data['uvIndex'],
                    significant_weather_code=timeseries_data['significantWeatherCode'],
                    precipitation_rate=timeseries_data['precipitationRate'],
                    total_precip_amount=timeseries_data['totalPrecipAmount'] if 'totalPrecipAmount' in timeseries_data else None,
                    total_snow_amount=timeseries_data['totalSnowAmount'] if 'totalSnowAmount' in timeseries_data else None,
                    prob_of_precipitation=timeseries_data['probOfPrecipitation']

                )
                time_series_object.save()


