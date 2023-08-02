from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, F, Q, Value, IntegerField, Count
from main.models import SensorEvent, Sensor
from .serializers import TrafficSerializer
from django.db.models.functions import Coalesce

@api_view(['GET'])
def day_of_week_average_count(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return Response({"error": "Both start_date and end_date parameters are required."}, status=400)

    # Assuming you have a 'event_datetime' field in the SensorEvent model
    # to store the date and time of each event
    queryset = Sensor.objects.filter(sensor_events__event_datetime__range=[start_date, end_date]).annotate(
        sensor_id = F('id'),
        sensor_name = F('name'),
    ).values('sensor_id', 'sensor_name')[:1000]

    reports = []
    # if not queryset.exists():
    #     return Response({"error": "No data available for the given date range."}, status=404)
    for q in queryset:

    # Calculate the average count for each day of the week (Monday to Sunday)
        averages = SensorEvent.objects.filter(event_datetime__range=[start_date, end_date], sensor__id=q['sensor_id']).values('sensor__id').annotate(
        
            mon_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=2),
                            output_field=IntegerField()),
                    Value(0),
                ),
            tue_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=3),
                            output_field=IntegerField()),
                    Value(0),
                ),
            wed_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=4),
                            output_field=IntegerField()),
                    Value(0),
                ),
            thu_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=5),
                            output_field=IntegerField()),
                    Value(0),
                ),
            fri_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=6),
                            output_field=IntegerField()),
                    Value(0),
                ),
            sat_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=7),
                            output_field=IntegerField()),
                    Value(0),
                ),
            sun_count= Coalesce(
                    Count(F('sensor_id'),
                            filter=Q(event_datetime__week_day=1),
                            output_field=IntegerField()),
                    Value(0),
                )
        ).aggregate(
            mon_avg_count = Avg(F('mon_count')),
            tue_avg_count = Avg(F('tue_count')),
            wed_avg_count = Avg(F('wed_count')),
            thu_avg_count = Avg(F('thu_count')),
            fri_avg_count = Avg(F('fri_count')),
            sat_avg_count = Avg(F('sat_count')),
            sun_avg_count = Avg(F('sun_count')),
        )
        reports.append({**q,**averages})
    print(reports)
    serializer = TrafficSerializer(reports, many=True)

    return Response({"results": serializer.data})
