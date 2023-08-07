from rest_framework import serializers

from .models import User, UserInformation, Department, Region


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInformationSerializer(serializers.ModelSerializer):
    year_of_graduation = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    start_position_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    end_position_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = UserInformation
        fields = "__all__"


class DepartmentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class RegionInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"
