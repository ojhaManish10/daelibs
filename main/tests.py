from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from main.models import Sensor, SensorEvent
from main.serializers import TrafficSerializer

class DayOfWeekAverageCountViewTestCase(TestCase):

    def setUp(self):
        # sample sensor
        self.sensor = Sensor.objects.create(name="Test Sensor")

        # sample sensor events
        self.event_datetime1 = datetime(2023, 8, 1, 12, 30)
        self.event_datetime2 = datetime(2023, 8, 2, 14, 45)
        self.event_datetime3 = datetime(2023, 8, 3, 16, 15)

        SensorEvent.objects.create(sensor=self.sensor, event_datetime=self.event_datetime1)
        SensorEvent.objects.create(sensor=self.sensor, event_datetime=self.event_datetime2)
        SensorEvent.objects.create(sensor=self.sensor, event_datetime=self.event_datetime3)

    def test_day_of_week_average_count_view(self):
        # client to simulate HTTP requests
        client = APIClient()

        url = reverse('day_of_week_average_count')

        # GET request to the view with start_date and end_date as query parameters
        start_date = datetime(2023, 8, 1)
        end_date = datetime(2023, 8, 3)
        response = client.get(url, {'start_date': start_date, 'end_date': end_date})

        # response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response data is correctly serialized and contains the expected keys
        expected_keys = ['sensor_id', 'sensor_name', 'mon_avg_count', 'tue_avg_count', 'wed_avg_count', 'thu_avg_count', 'fri_avg_count', 'sat_avg_count', 'sun_avg_count']
        for item in response.data['results']:
            self.assertTrue(all(key in item for key in expected_keys))

        # serializer properly serializes the data
        serializer = TrafficSerializer(data=response.data['results'], many=True)
        self.assertTrue(serializer.is_valid())


    def test_day_of_week_average_count_view_missing_parameters(self):
        # client to simulate HTTP requests
        client = APIClient()

        url = reverse('day_of_week_average_count')

        # GET request to the view without start_date and end_date parameters
        response = client.get(url)

        # response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Error message
        expected_error = {"error": "Both start_date and end_date parameters are required."}
        self.assertEqual(response.data, expected_error)
