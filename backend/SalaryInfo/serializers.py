from rest_framework import serializers
from .models import Employee, Salary, SalaryCertificate, PaySlip, ExcelFileProcess
from rest_framework import serializers
import pandas as pd


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Salary
        fields = "__all__"


class UploadFileSerializer(serializers.Serializer):

    BUSINESS_UNIT = [
        ("Consumer Division", "Consumer Division"),
        ("Prime Pusti Limited", "Prime Pusti Limited"),
        ("Prime Cosmetics Limited", "Prime Cosmetics Limited"),
        ("T.K. Logistics", "T.K. Logistics"),
    ]

    COMPANY = [
        ("Prime Pusti Limited", "Prime Pusti Limited"),
        ("Prime Cosmetics Limited", "Prime Cosmetics Limited"),
        ("Super Oil Refinery Limited", "Super Oil Refinery Limited"),
    ]

    file = serializers.FileField()
    salary_month = serializers.DateField()
    business_unit = serializers.CharField(max_length=100)
    company = serializers.CharField(max_length=100)

    class Meta:
        fields = ["file", "Salary Month", "Business Unit", "Company"]


class SalaryCertificateSerializer(serializers.ModelSerializer):
    salary = SalarySerializer(read_only=True)
    salary_id = serializers.PrimaryKeyRelatedField(
        queryset=Salary.objects.all(), write_only=True
    )

    class Meta:
        model = SalaryCertificate
        exclude = ["reference_number"]

    def create(self, validated_data):
        salary = validated_data.pop("salary_id")
        certificate = SalaryCertificate.objects.create(salary=salary, **validated_data)
        return certificate

    def update(self, instance, validated_data):
        salary = validated_data.pop("salary_id", None)
        if salary:
            instance.salary = salary
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PayslipSerializer(serializers.ModelSerializer):
    salary = SalarySerializer(many=True, read_only=True)
    salary_id = serializers.PrimaryKeyRelatedField(
        queryset=Salary.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = PaySlip
        fields = "__all__"

    def create(self, validated_data):
        salaries = validated_data.pop("salary_id")
        payslip = PaySlip.objects.create(**validated_data)
        payslip.salary.set(salaries)
        return payslip

    def update(self, instance, validated_data):
        salaries = validated_data.pop("salary_id", None)
        if salaries is not None:
            instance.salary.set(salaries)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ExcelFileSerializer(serializers.ModelSerializer):
    sheets = serializers.SerializerMethodField()

    class Meta:
        model = ExcelFileProcess
        fields = ["id", "file", "uploaded_at", "sheets"]
        read_only_fields = ["sheets"]

    def get_sheets(self, obj):
        try:
            xls = pd.ExcelFile(obj.file)
            return xls.sheet_names
        except:
            return []
