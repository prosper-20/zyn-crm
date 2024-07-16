from django.urls import path
from .views import RegistrationAPIView, IndustryView, PartnerRegistrationAPIView, OrganizationView, EmployeeRegistrationAPIView, CreateOpportunityView, DashboardView, RetrieveUserProfile, OpportunityView, ProductView, SingleProductView, GetUpdateDeleteLeadsView, RetrieveLeadsView, CreateLeadView, ContactAPIView, VerifyOTPView, LoginAPIView, PasswordChangeView, HomePage, TokenResetView, LogoutAPIView, InitiatePasswordResetView, PasswordResetConfirmView, CreateCustomerAccountView


urlpatterns = [
    path("create/", RegistrationAPIView.as_view(), name="account-create"),
    path("create/partner/", PartnerRegistrationAPIView.as_view(), name="partner-create"),
    path("create/employee/", EmployeeRegistrationAPIView.as_view(), name="employee-create"),
    path("create/accounts/", CreateCustomerAccountView.as_view(), name="create-account"),
    path("create/opportunity/", CreateOpportunityView.as_view(), name="create-opportunity"),
    path("industry/", IndustryView.as_view(), name="industry"),
    path("organizations/", OrganizationView.as_view(), name="organization"),
    path("opportunity/<slug:opportunity_slug>/", OpportunityView.as_view(), name="opportunity"),
    path("lead/create/", CreateLeadView.as_view(), name="lead-create"),
    path("leads/", RetrieveLeadsView.as_view(), name="all-leads"),
    path("leads/<str:id>/", GetUpdateDeleteLeadsView.as_view(), name="single-lead"),
    path("products/all/", ProductView.as_view(), name="product-list"),
    path("products/<slug:product_slug>/", SingleProductView.as_view(), name="single-product"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", RetrieveUserProfile.as_view(), name="profile"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("home/", HomePage.as_view(), name="home"),
    path("contact/", ContactAPIView.as_view(), name="contact-us"),
    path("verify/otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("password/reset/", InitiatePasswordResetView.as_view(), name="password-reset"),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password/change/", PasswordChangeView.as_view(), name='password-change'),
    path("token/reset/", TokenResetView.as_view(), name="token-reset")

]