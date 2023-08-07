from rest_framework import serializers

from .models import ReportKey, ReportGroup


class ReportKeysSerializer(serializers.ModelSerializer):
    report_group_one = serializers.SlugRelatedField(slug_field='name', read_only=True)
    report_group_two = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ReportKey
        fields = ('id', 'name', 'report_group_one', 'report_group_two',)


class ReportGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportGroup
        fields = ('id', 'name')