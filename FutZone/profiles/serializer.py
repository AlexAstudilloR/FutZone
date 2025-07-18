from rest_framework import serializers
from .models import ProfileModel

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get('request')
        if request and not request.user.is_admin:
            fields['is_admin'].read_only = True

        return fields


class PaymentMethodQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['payment_qr']