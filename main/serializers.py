from rest_framework import serializers

class TrafficSerializer(serializers.Serializer):
    sensor_id = serializers.IntegerField()
    sensor_name = serializers.CharField()
    mon_avg_count = serializers.IntegerField()
    tue_avg_count = serializers.IntegerField()
    wed_avg_count = serializers.IntegerField()
    thu_avg_count = serializers.IntegerField()
    fri_avg_count = serializers.IntegerField()
    sat_avg_count = serializers.IntegerField()
    sun_avg_count = serializers.IntegerField()
