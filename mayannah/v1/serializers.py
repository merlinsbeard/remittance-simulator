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
                 "payout_currency",
                 "status",
                 )

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
