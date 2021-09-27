from rest_framework import serializers
from django.core.exceptions import ValidationError
from ipaddress import ip_network, ip_address
from .models import Network, Router


class RouterReadSerializer(serializers.ModelSerializer):
    networks = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Router
        fields = '__all__'


class RouterWriteSerializer(serializers.ModelSerializer):

    def validate_management_ip(self, value):
        try:
            ip_address(value)
        except ValueError:
            raise ValidationError('The value you have provided is not a valid host IP address. '
                                  'Example of a valid network address: 192.168.10.58')
        return value

    class Meta:
        model = Router
        fields = '__all__'


class NetworkReadSerializer(serializers.ModelSerializer):
    router = RouterReadSerializer(many=False)

    class Meta:
        model = Network
        fields = '__all__'


class NetworkWriteSerializer(serializers.ModelSerializer):

    def validate_network_address(self, value):
        try:
            ip_network(value)
        except ValueError:
            raise ValidationError('The value you have provided is not a valid network IP address. '
                                  'Example of a valid network address: 192.168.0.0/16')
        return value

    def validate_vlan_tag(self, value):
        error_message = 'The vlan_tag is a number with values between 1 and 4095'
        try:
            if int(value) not in range(1, 4096):
                raise ValidationError(error_message)
            return value
        except ValueError:
            raise ValidationError(error_message)

    class Meta:
        model = Network
        fields = '__all__'
