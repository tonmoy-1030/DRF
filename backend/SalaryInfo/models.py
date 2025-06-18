from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class Employee(models.Model):
    BUSINESS_UNIT = [
        ("Consumer Division", "Consumer Division"),
        ("Prime Pusti Limited", "Prime Pusti Limited"),
        ("Prime Cosmetics Limited", "Prime Cosmetics Limited"),
        ("T.K. Logistics", "T.K. Logistics"),
        (
            "T.K. Food Products Distribution Limited",
            "T.K. Food Products Distribution Limited",
        ),
    ]

    COMPANY = [
        ("Prime Pusti Limited", "Prime Pusti Limited"),
        ("Prime Cosmetics Limited", "Prime Cosmetics Limited"),
        ("Super Oil Refinery Limited", "Super Oil Refinery Limited"),
        ("T.K. Logistics", "T.K. Logistics"),
        (
            "T.K. Food Products Distribution Limited",
            "T.K. Food Products Distribution Limited",
        ),
    ]

    EID = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    date_of_joining = models.DateField()
    cash_salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    business_unit = models.CharField(max_length=50, choices=BUSINESS_UNIT)
    company = models.CharField(max_length=50, choices=COMPANY)

    def __str__(self):
        return f"{self.EID} - {self.name}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_month = models.DateField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    ma = models.DecimalField(max_digits=10, decimal_places=2)
    ca = models.DecimalField(max_digits=10, decimal_places=2)
    ea = models.DecimalField(max_digits=10, decimal_places=2)
    payable_days = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable_salary = models.DecimalField(max_digits=10, decimal_places=2)

    # add deductions fields as needed
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    benevolent_fund = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    food_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    loan = models.DecimalField(max_digits=10, decimal_places=2)
    exceed_mobile_bill = models.DecimalField(max_digits=10, decimal_places=2)
    other_deduction = models.DecimalField(max_digits=10, decimal_places=2)

    # Addition with the salary
    arrear = models.DecimalField(max_digits=10, decimal_places=2)
    car_allowance = models.DecimalField(max_digits=10, decimal_places=2)

    def total_deductions(self):
        return (
            self.provident_fund
            + self.benevolent_fund
            + self.tax
            + self.food_consumption
            + self.loan
            + self.exceed_mobile_bill
            + self.other_deduction
        )

    def net_payable(self):
        return self.gross_salary - self.total_deductions() + self.arrear

    def save(self, *args, **kwargs):
        self.basic_salary = self.gross_salary * 0.5
        self.hra = self.gross_salary * 0.25
        self.ma = self.gross_salary * 0.10
        self.ca = self.gross_salary * 0.10
        self.ea = self.gross_salary * 0.05
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.salary_month}"


class SalaryCertificate(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    reference_number = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Add any custom logic here if needed
        if not self.issue_date:
            self.issue_date = timezone.now()

        if not self.reference_number:
            current_month = self.issue_date.month
            current_year = self.issue_date.year
            unit = self.salary.employee.business_unit

            max_reference_number = SalaryCertificate.objects.filter(
                issue_date__month=current_month,
                issue_date__year=current_year,
                salary__employee__business_unit=unit,
            ).aggregate(models.Max("reference_number"))["reference_number__max"]

            self.reference_number = int((max_reference_number or 0)) + 1

        super().save(*args, **kwargs)


class PaySlip(models.Model):
    salary = models.ManyToManyField(Salary, blank=False)
    issue_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Pay Slip for {self.issue_date} - {self.salary.first().employee.name}"


class ExcelFileProcess(models.Model):
    file = models.FileField(upload_to="excel_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
