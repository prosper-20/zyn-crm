from django.urls import path
from .views import RegistrationAPIView, RetrieveUserProfile, ProductView, SingleProductView, GetUpdateDeleteLeadsView, RetrieveLeadsView, CreateLeadView, ContactAPIView, VerifyOTPView, LoginAPIView, PasswordChangeView, HomePage, TokenResetView, LogoutAPIView, InitiatePasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path("create/", RegistrationAPIView.as_view(), name="account-create"),
    path("lead/create/", CreateLeadView.as_view(), name="lead-create"),
    path("leads/", RetrieveLeadsView.as_view(), name="all-leads"),
    path("leads/<str:id>/", GetUpdateDeleteLeadsView.as_view(), name="single-lead"),
    path("products/all/", ProductView.as_view(), name="product-list"),
    path("products/<slug:product_slug>/", SingleProductView.as_view(), name="single-product"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", RetrieveUserProfile.as_view(), name="profile"),
    path("home/", HomePage.as_view(), name="home"),
    path("create-contact/", ContactAPIView.as_view(), name="contact-us"),
    path("verify/otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("password/reset/", InitiatePasswordResetView.as_view(), name="password-reset"),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password/change/", PasswordChangeView.as_view(), name='password-change'),
    path("token/reset/", TokenResetView.as_view(), name="token-reset")

]