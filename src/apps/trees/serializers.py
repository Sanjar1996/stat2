from rest_framework import serializers

from .models import TreeHeightReport

class TreeHeightDepartmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = TreeHeightReport
    fields = ("__all__")