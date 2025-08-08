from rest_framework import generics, viewsets
from .models import Employee, Salary, SalaryCertificate, PaySlip, ExcelFileProcess
from .serializers import (
    EmployeeSerializer,
    SalarySerializer,
    UploadFileSerializer,
    SalaryCertificateSerializer,
    PayslipSerializer,
    ExcelFileSerializer,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import pandas as pd
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (
    SalaryFilter,
    SalaryCertificateFilter,
    EmployeeFilter,
    PaySlipFilter,
)
from rest_framework.decorators import action
from rest_framework.views import APIView
from .SalaryCertificate import (
    Generate_Salary_Certificate,
    Generate_Salary_Certificate_without_deduction,
)
from PyPDF2 import PdfMerger
import io
from .PaySlip import Generate_PaySlip
from django.http import HttpResponse
from .number2text import format_number, convert_to_words


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request):
        queryset = self.get_queryset()
        paginator = PageNumberPagination()
        paginator.page_size = 12  # Number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = EmployeeSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=204)


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all().select_related("employee")
    serializer_class = SalarySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SalaryFilter
    search_fields = ["employee__name", "employee__EID", "employee__designation"]
    ordering_fields = ["salary_month", "gross_salary", "employee__name"]
    ordering = ["-salary_month"]

    def get_queryset(self):
        queryset = super().get_queryset()
        month = self.request.query_params.get("month", None)
        year = self.request.query_params.get("year", None)
        id = self.request.query_params.get("id", None)

        if month:
            queryset = queryset.filter(salary_month__month=month)
        if year:
            queryset = queryset.filter(salary_month__year=year)
        if id:
            queryset = queryset.filter(employee__id=id)

        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = PageNumberPagination()
        paginator.page_size = 12  # Number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = SalarySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Salary.objects.all()
        salary = get_object_or_404(queryset, pk=pk)
        serializer = SalarySerializer(salary)
        return Response(serializer.data)

    def create(self, request):
        serializer = SalarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        salary = get_object_or_404(Salary, pk=pk)
        serializer = SalarySerializer(salary, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        salary = get_object_or_404(Salary, pk=pk)
        salary.delete()
        return Response(status=204)


class UploadViewSet(viewsets.ModelViewSet):
    queryset = ExcelFileProcess.objects.all()
    serializer_class = ExcelFileSerializer

    @action(detail=True, methods=["post"])
    def sheet_data(self, request, pk=None):
        excel_file = self.get_object()
        sheet_name = request.query_params.get("sheet")
        salary_month = request.data.get("salary_month")
        business_unit = request.data.get("business_unit")
        company = request.data.get("company")

        if not excel_file.file:
            return Response("No file uploaded", status=400)

        try:
            df = pd.read_excel(
                excel_file.file, sheet_name=sheet_name, dtype={"Employee \nID": str}
            )
            df.columns = df.columns.str.strip().str.replace("\n", "", regex=False)
            df.dropna(subset=["Employee ID", "Name"], inplace=True)

            created_employees, updated_employees = 0, 0
            created_salaries, updated_salaries = 0, 0
            employee_map = {}
            errors = []

            # Process employees first
            for index, row in df.iterrows():
                try:
                    if not row.get("Date of Joining"):
                        raise ValueError("Date of Joining is required")

                    if not isinstance(row.get("Employee ID"), str):
                        raise ValueError("Employee ID must be a string")

                    employee, created = Employee.objects.update_or_create(
                        EID=row["Employee ID"],
                        defaults={
                            "name": row["Name"],
                            "designation": row.get("Designation", "N/A"),
                            "department": row.get("Department", "N/A"),
                            "date_of_joining": row["Date of Joining"],
                            "business_unit": business_unit,
                            "company": company,
                        },
                    )
                    if created:
                        created_employees += 1
                    else:
                        updated_employees += 1
                    employee_map[row["Employee ID"]] = employee
                except Exception as e:
                    errors.append(
                        {
                            "row": index
                            + 2,  # Excel rows are 1-based and header is row 1
                            "employee_id": row.get("Employee ID", "Unknown"),
                            "error": f"Employee creation failed: {str(e)}",
                            "type": "employee_error",
                        }
                    )

            # Process salaries second
            for index, row in df.iterrows():
                try:
                    employee = employee_map.get(row["Employee ID"])
                    if not employee:
                        continue

                    # Validate numeric fields
                    required_numeric_fields = [
                        ("Gross Salary", "gross_salary"),
                        ("Payable Days", "payable_days"),
                        ("Total Payable", "total_payable_salary"),
                        ("PF", "provident_fund"),
                    ]

                    for excel_field, _ in required_numeric_fields:
                        if pd.isna(row[excel_field]) or not isinstance(
                            row[excel_field], (int, float)
                        ):
                            raise ValueError(f"{excel_field} must be a valid number")

                    salary, created = Salary.objects.update_or_create(
                        employee=employee,
                        salary_month=salary_month,
                        defaults={
                            "gross_salary": row["Gross Salary"],
                            "payable_days": row["Payable Days"],
                            "total_payable_salary": row["Total Payable"],
                            "provident_fund": row["PF"],
                            "benevolent_fund": row.get("Benevolent Fund", 0),
                            "tax": row.get("Tax", 0),
                            "food_consumption": row.get("Food Consumption", 0),
                            "loan": row.get("Cash, Advanced & Loan", 0),
                            "exceed_mobile_bill": row.get("Exceed Mobile bill", 0),
                            "other_deduction": row.get("Others Deduction", 0),
                            "arrear": row.get("Arrear", 0),
                            "car_allowance": row.get("Car Expense", 0),
                        },
                    )
                    if created:
                        created_salaries += 1
                    else:
                        updated_salaries += 1
                except Exception as e:
                    errors.append(
                        {
                            "row": index
                            + 2,  # Excel rows are 1-based and header is row 1
                            "employee_id": row.get("Employee ID", "Unknown"),
                            "error": f"Salary creation failed: {str(e)}",
                            "type": "salary_error",
                        }
                    )

            response_data = {
                "message": "File processed with status",
                "employees_created": created_employees,
                "employees_updated": updated_employees,
                "salaries_created": created_salaries,
                "salaries_updated": updated_salaries,
                "errors": errors,
                "status": "success" if not errors else "partial_success",
            }

            status_code = (
                200 if not errors else 207
            )  # Using 207 Multi-Status for partial success
            return Response(response_data, status=status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class SalaryCertificateViewSet(viewsets.ModelViewSet):
    queryset = SalaryCertificate.objects.all()
    serializer_class = SalaryCertificateSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SalaryCertificateFilter
    search_fields = [
        "salary__employee__name",
        "salary__employee__EID",
        "salary__employee__designation",
    ]
    ordering = ["-issue_date"]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = PageNumberPagination()
        paginator.page_size = 12
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        certificate = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(certificate)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        certificate = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(certificate, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        certificate = get_object_or_404(self.get_queryset(), pk=pk)
        certificate.delete()
        return Response(status=204)


class SalaryCertificateAPIView(APIView):
    def get(self, request, pk):
        Salary_Certificate = SalaryCertificate.objects.get(id=pk)
        employee_data = {
            "name": Salary_Certificate.salary.employee.name,
            "emp_id": Salary_Certificate.salary.employee.EID,
            "company": f"{Salary_Certificate.salary.employee.business_unit}",
            "designation": Salary_Certificate.salary.employee.designation,
            "department": Salary_Certificate.salary.employee.department,
            "joining_date": Salary_Certificate.salary.employee.date_of_joining,
            "gross_salary": format_number(
                float(Salary_Certificate.salary.gross_salary)
            ),
            "salary_in_words": f"{convert_to_words(int(Salary_Certificate.salary.gross_salary))} only",
            "Basic Salary": float(Salary_Certificate.salary.basic_salary),
            "House Rent": float(Salary_Certificate.salary.hra),
            "Conveyance Allowance": float(Salary_Certificate.salary.ca),
            "Medical Allowance": float(Salary_Certificate.salary.ma),
            "Entertainment Allowance": float(Salary_Certificate.salary.ea),
            "reference": Salary_Certificate.reference_number,
            "issue_date": Salary_Certificate.issue_date,
            "Car Allowance": Salary_Certificate.salary.car_allowance,
            "total_salary": Salary_Certificate.salary.gross_salary,
            "cash": Salary_Certificate.salary.employee.cash_salary,
        }
        pdf_bytes = Generate_Salary_Certificate(employee_data)

        filename = f"Salary_Certificate_{int(employee_data['reference']):02d}_{employee_data['issue_date'].strftime('%m-%Y')}.pdf"

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response


class SalaryCertificateWithDeductionAPIView(APIView):
    def get(self, request, pk):
        Salary_Certificate = SalaryCertificate.objects.get(id=pk)

        employee_data = {
            "name": Salary_Certificate.salary.employee.name,
            "emp_id": Salary_Certificate.salary.employee.EID,
            "company": f"{Salary_Certificate.salary.employee.business_unit}",
            "designation": Salary_Certificate.salary.employee.designation,
            "department": Salary_Certificate.salary.employee.department,
            "joining_date": Salary_Certificate.salary.employee.date_of_joining,
            "gross_salary": format_number(
                float(Salary_Certificate.salary.gross_salary)
            ),
            "salary_in_words": f"{convert_to_words(int(Salary_Certificate.salary.gross_salary))} only",
            "Basic Salary": float(Salary_Certificate.salary.basic_salary),
            "House Rent": float(Salary_Certificate.salary.hra),
            "Conveyance Allowance": float(Salary_Certificate.salary.ca),
            "Medical Allowance": float(Salary_Certificate.salary.ma),
            "Entertainment Allowance": float(Salary_Certificate.salary.ea),
            "reference": Salary_Certificate.reference_number,
            "issue_date": Salary_Certificate.issue_date,
            "Car Allowance": Salary_Certificate.salary.car_allowance,
            "total_salary": Salary_Certificate.salary.gross_salary,
            "pf": Salary_Certificate.salary.provident_fund,
            "bf": Salary_Certificate.salary.benevolent_fund,
            "tax": Salary_Certificate.salary.tax,
            "food": Salary_Certificate.salary.food_consumption,
            "loan": Salary_Certificate.salary.loan,
            "exceed_mobile": Salary_Certificate.salary.exceed_mobile_bill,
            "other_deduction": Salary_Certificate.salary.other_deduction,
            "total_deduction": int(Salary_Certificate.salary.total_deductions()),
            "cash": Salary_Certificate.salary.employee.cash_salary,
        }

        pdf_bytes = Generate_Salary_Certificate_without_deduction(employee_data)

        filename = f"Salary_Certificate_{int(employee_data['reference']):02d}_{employee_data['issue_date'].strftime('%m-%Y')}.pdf"

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response


# Payslip API View


class PaySlipViewSet(viewsets.ModelViewSet):
    queryset = PaySlip.objects.all()
    serializer_class = PayslipSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PaySlipFilter
    search_fields = ["salary__employee__EID", "Salary__employee__name"]

    ordering = ["-issue_date"]

    def List(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = PageNumberPagination()
        paginator.page_size = 12
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        payslip = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(payslip)
        return Response(serializer.data)

    def update(self, request, pk=None):
        payslip = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(payslip, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        payslip = get_object_or_404(self.get_queryset(), pk=pk)
        payslip.delete()
        return Response(status=204)


class SalaryPaySlipAPIView(APIView):

    def get(self, request, pk):
        merger = PdfMerger()
        merged_buffered = io.BytesIO()

        payslips = get_object_or_404(PaySlip, id=pk)

        for salary in payslips.salary.all():
            buffer = io.BytesIO()
            employee_data = {
                "issue_date": payslips.issue_date,
                "salary_month": salary.salary_month,
                "name": salary.employee.name,
                "emp_id": salary.employee.EID,
                "company": f"{salary.employee.company}",
                "designation": salary.employee.designation,
                "department": salary.employee.department,
                "joining_date": salary.employee.date_of_joining,
                "gross_salary": format_number(float(salary.gross_salary)),
                "Basic Salary": format_number(salary.basic_salary),
                "House Rent": format_number(salary.hra),
                "Conveyance Allowance": format_number(salary.ca),
                "Medical Allowance": format_number(salary.ma),
                "Entertainment Allowance": format_number(salary.ea),
                "Car Allowance": salary.car_allowance,
                "total_salary": salary.gross_salary,
                "pf": salary.provident_fund,
                "bf": salary.benevolent_fund,
                "tax": salary.tax,
                "food": salary.food_consumption,
                "loan": salary.loan,
                "exceed_mobile": salary.exceed_mobile_bill,
                "other_deduction": salary.other_deduction,
                "total_deduction": salary.total_deductions(),
                "net_salary": salary.net_payable(),
                "cash_salary": salary.employee.cash_salary,
            }
            Generate_PaySlip(employee_data=employee_data, pdf_path=buffer)
            buffer.seek(0)
            merger.append(buffer)
        merger.write(merged_buffered)
        merged_buffered.seek(0)

        filename = f"PaySlip.pdf"

        response = HttpResponse(
            merged_buffered.getvalue(), content_type="application/pdf"
        )
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response
