from typing import Dict
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    def validate(self, attrs: Dict):
        if self.instance:
            if attrs.get('currency') != self.instance.currency:
                raise serializers.ValidationError({
                    'currency': 'Unsupported update currency %s to %s'
                                % (self.instance.currency, attrs.get('currency'))
                })
        return super(PaymentSerializer, self).validate(attrs=attrs)

    class Meta:
        model = Payment
        fields = '__all__'
