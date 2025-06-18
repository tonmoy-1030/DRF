from django.contrib import admin
from .models import Employee, Salary, SalaryCertificate, PaySlip
from django.db.models import ManyToManyField


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "EID",
        "name",
        "department",
        "designation",
        "date_of_joining",
        "business_unit",
    )
    list_display_links = ("EID", "name")
    search_fields = ("EID", "name")
    list_filter = ("department", "business_unit")
    list_per_page = 20
    ordering = ("EID",)
    date_hierarchy = "date_of_joining"


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("employee", "salary_month", "gross_salary", "net_payable")
    list_display_links = ("employee", "salary_month")
    search_fields = ("employee__EID", "employee__name")
    list_filter = ("salary_month",)
    list_per_page = 20
    date_hierarchy = "salary_month"


@admin.register(SalaryCertificate)
class SalaryCertificateAdmin(admin.ModelAdmin):
    list_display = ("salary__employee", "salary", "issue_date", "reference_number")
    list_display_links = ("salary__employee", "salary")
    search_fields = ("employee__EID", "employee__name")
    list_filter = ("issue_date",)
    list_per_page = 20
    date_hierarchy = "issue_date"
    ordering = ("-issue_date",)


@admin.register(PaySlip)
class PaySlipAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in PaySlip._meta.fields
        if field.name != "id" and not field.many_to_many and not field.one_to_many
    ] + ["get_employee"]
    list_display_links = ("get_employee",)
    search_fields = ("employee__EID", "employee__name")
    list_filter = ("issue_date",)
    list_per_page = 20
    date_hierarchy = "issue_date"
    ordering = ("-issue_date",)

    def get_employee(self, obj):
        return obj.salary.first().employee if obj.salary else "-"

    get_employee.short_description = "Employee"
