from rest_framework import serializers
from partner.models import Person, Remittance
from virtual_money.models import Transaction,TransactionHistory, Branch
from django.contrib.auth.models import User


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
    status = serializers.ReadOnlyField()

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


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.CharField(max_length=255)
    branch = serializers.CharField(max_length=255)
    reference_id = serializers.ReadOnlyField()

    class Meta:
        model = TransactionHistory
        fields = (
                "reference_id",
                "account",
                "branch",
                "amount",
                "type",
                )

    def validate_account(self, value):
        try:
            person = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User Not Existing")
        return person

    def validate_branch(self, value):
        try:
            branch = Branch.objects.get(name=value)
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch Does Not Exists")
        return branch

    def validate(self, value):
        # Perform user amount checking

        if value['type'] == "WITHDRAW":
            user = User.objects.get(username=value['account'])
            transactions = TransactionHistory.objects.filter(account=user)
            deposits = transactions.filter(
                                    type="DEPOSIT"
                                  ).filter(
                                    status="PAID")
            withdraws = transactions.filter(
                                    type="WITHDRAW"
                                  ).filter(
                                    status="PAID")
            deposits_sum = sum([n.amount for n in deposits])
            withdraws_sum = sum([n.amount for n in withdraws])
            money = deposits_sum - withdraws_sum

            if money < value['amount']:
                raise serializers.ValidationError(
                                "Not enough money to withdraw")

        if value['amount'] < 1:
            raise serializers.ValidationError("Amount too Small")

        return value


class TransactionDetailSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    branch = serializers.StringRelatedField()

    class Meta:
        model = TransactionHistory
        fields = (
                "reference_id",
                "account",
                "branch",
                "amount",
                "date_created",
                "status",
                "type",
                )


class TransactionCompleteSerializer(serializers.Serializer):
    reference_id = serializers.CharField(max_length=255)
