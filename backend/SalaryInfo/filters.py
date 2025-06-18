# filters.py
import django_filters
from .models import Salary, SalaryCertificate, Employee, PaySlip


class SalaryFilter(django_filters.FilterSet):
    eid = django_filters.CharFilter(field_name="employee__EID", lookup_expr="exact")
    id = django_filters.CharFilter(field_name="employee__id", lookup_expr="exact")

    class Meta:
        model = Salary
        fields = ["eid", "id"]  # you can add more filterable fields here


class SalaryCertificateFilter(django_filters.FilterSet):
    eid = django_filters.CharFilter(
        field_name="salary__employee__EID", lookup_expr="exact"
    )

    class Meta:
        model = SalaryCertificate
        fields = ["eid"]


class EmployeeFilter(django_filters.FilterSet):
    EID = django_filters.CharFilter(field_name="EID", lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Employee
        fields = ["EID", "name"]


class PaySlipFilter(django_filters.FilterSet):
    EID = django_filters.CharFilter(
        field_name="salary__employee__EID", lookup_expr="icontains"
    )
    name = django_filters.CharFilter(
        field_name="salary__employee__name", lookup_expr="icontains"
    )

    class meta:
        model = PaySlip
        fields = ["EID", "name"]
