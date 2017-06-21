from rest_framework import serializers
from partner.models import Person, Remittance


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
                "first_name",
                "last_name",
                "contact_number",
                "address",
                "country",
                "identification_type",
                "identification_id",
                )


class RemittanceSerializer(serializers.HyperlinkedModelSerializer):
    remitter = PersonSerializer()
    beneficiary = PersonSerializer()

    class Meta:
        model = Remittance
        fields = (
                 "source_reference_number",
                 "slug",
                 "remitter",
                 "beneficiary",
                 "payout_amount",
                 "date_created",
                 "date_paid_out",
                 "payout_currency",
                 "status",
                 )

    def validate_payout_amount(self, value):
        amount = value
        cents = abs(value) % 100
        if amount < 1000:
            error_message = "Amount Should be greatern than 1000"
            raise serializers.ValidationError(error_message)
        elif cents > 0:
            error_message = "No cents allowed"
            raise serializers.ValidationError(error_message)
        else:
            return value

    def create(self, validated_data):
        remitter = validated_data.pop('remitter')
        remitter = Person.objects.create(**remitter)
        beneficiary = validated_data.pop('beneficiary')
        beneficiary = Person.objects.create(**beneficiary)
        validated_data['remitter'] = remitter
        validated_data['beneficiary'] = beneficiary
        remittance = Remittance.objects.create(**validated_data)
        return remittance

    def update(self, instance, validated_data):
        beneficiary = validated_data.get(
                'beneficiary', instance.beneficiary)
        beneficiary = Person(**beneficiary)
        beneficiary.save()
        instance.beneficiary = beneficiary
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class RemittancePaySerializer(serializers.Serializer):
    source_reference_number = serializers.CharField(max_length=255)
