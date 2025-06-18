from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
#     path('employees/<str:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),
#     path('salaries/', SalaryListCreateView.as_view(), name='salary-list-create'),
#     path('salaries/<int:pk>/', SalaryRetrieveUpdateDestroyView.as_view(), name='salary-retrieve-update-destroy'),
# ]

router = DefaultRouter()
router.register(r"employees", viewset=views.EmployeeViewSet, basename="employee")
router.register(r"salaries", viewset=views.SalaryViewSet, basename="salary")
router.register(r"upload", viewset=views.UploadViewSet, basename="upload")
router.register(
    r"certificate", viewset=views.SalaryCertificateViewSet, basename="certificate"
)

router.register(r"payslip", viewset=views.PaySlipViewSet, basename="payslip")


urlpatterns = [
    path(
        "salary-certificate/<int:pk>",
        views.SalaryCertificateAPIView.as_view(),
        name="salary-certificate",
    ),
    path(
        "salary-certificate-deduction/<int:pk>",
        views.SalaryCertificateWithDeductionAPIView.as_view(),
        name="salary-certificate",
    ),
    path(
        "payslip/<int:pk>",
        views.SalaryPaySlipAPIView.as_view(),
        name="payslip",
    ),
]


urlpatterns += router.urls
