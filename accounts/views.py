from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import ContactSerializer, EmployeeRegistrationSerializer, PartnerRegistrationSerializer, OpportunitySerializer, CreateOpportunitySerializer, CreateCustomerAccountSerializer, ProductSerializer, UserSerializer, RetrieveLeadsSeializer, LeadSerializer, CustomUserRegistrationSerializer, VerifyOTPSerializer, LoginSerializer, PasswordChangeSerializer, TokenRefreshSerializer, InitiatePasswordResetSerializer, PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Contact, Opportunity, Product,  Lead, CustomToken, OTPToken, Contact
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from decouple import config
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
import mailtrap as mt
from django.contrib.auth import authenticate, login
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


class ContactAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        all_contacts = Contact.objects.all()
        serializer = ContactSerializer(all_contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Contact Info saved"}, status=status.HTTP_201_CREATED)


class RegistrationAPIView(APIView):
    def post(self, reuqest, fomrat=None):
        serializer = CustomUserRegistrationSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Account creation successful"}, status=status.HTTP_201_CREATED)
    

class PartnerRegistrationAPIView(APIView):
    def post(self, reuqest, fomrat=None):
        serializer = PartnerRegistrationSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Partner Account creation successful"}, status=status.HTTP_201_CREATED)
    

class EmployeeRegistrationAPIView(APIView):
    def post(self, reuqest, fomrat=None):
        serializer = EmployeeRegistrationSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Employee Account creation successful"}, status=status.HTTP_201_CREATED)
    


class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            email = serializer.validated_data['email_or_phone_number']
            password = serializer.validated_data['password']
            if '@' in email:
                user = get_object_or_404(CustomUser, email=email).email
            else:
                user = get_object_or_404(CustomUser, phone_number=email).email
            
            current_user = authenticate(request, username=user, password=password)
            if current_user is not None:
                login(request, current_user)
                # refresh = RefreshToken.for_user(user)
                # access_token = AccessToken.for_user(user)

                # # Store tokens in CustomToken model
                # custom_token, _ = CustomToken.objects.get_or_create(user=user)
                # custom_token.access_token = str(access_token)
                # custom_token.refresh_token = str(refresh)
                # custom_token.access_token_expires_at = timezone.now() + timedelta(hours=1, minutes=60)
                # custom_token.refresh_token_expires_at = timezone.now() + timedelta(hours=1, days=1)
                # custom_token.save()     
                # if user.is_superuser and user.is_staff:
                #     data["user_type"] = "Admin"  
                # elif user.is_staff and user.is_active:
                #     data["user_type"] = "Manager"
                # else:
                #     data["user_type"] = "Regular"

                # #YOU JUST ADDED THIS
                # user = authenticate(request, username=email, password=password)
                # if user is not None:
                    # subject = 'OTP LOGIN'
                    # html_message = render_to_string('accounts/otp_email.html')
                    # plain_message = strip_tags(html_message)
                    # from_email = config('DEFAULT_FROM_EMAIL_2')  # Replace with your email
                    # to = email
                    # send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    # login(request, user)

                # print("user", user)

                return Response({
                        "Success": "User Info Accurate",
                        "otp_verification_link": "http://127.0.0.1:8000/accounts/verify/otp",
                        # "data": data,
                        # 'access_token': str(access_token),
                        # 'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Get the access token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):]
            access_token_obj = AccessToken(access_token)

            # Check if the access token is associated with the current user
            try:
                user_instance = CustomUser.objects.get(email=request.user.email)
                custom_token = CustomToken.objects.filter(user=user_instance).first()
            except User.DoesNotExist:
                return Response({"Error": "User credentials invalid"})
            if custom_token:
                custom_token.delete()

                return Response({'message': 'User successfully logged out'}, status=status.HTTP_200_OK)

        # If the access token is invalid or not associated, respond with an error
        return Response({'error': 'Invalid access token or user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        current_user = CustomUser.objects.get(email=request.user)
        serializer.is_valid(raise_exception=True)
        current_user.set_password(serializer.validated_data['new_password'])
        current_user.save()
        return Response({"Success": "Password successfully changed"}, status=status.HTTP_202_ACCEPTED)
    


class HomePage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        return Response("Home Page")
    


class TokenResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None, *kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']


        try:
            custom_token = CustomToken.objects.get(refresh_token=refresh_token)
            user = custom_token.user
            current_user = CustomUser.objects.get(email=user)
        except CustomToken.DoesNotExist:
            return Response({'error': 'Invalid access token or user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        

        if custom_token.is_refresh_token_expired() == False:
            refresh_token = RefreshToken.for_user(current_user)
            new_access_token = AccessToken.for_user(custom_token.user)

            custom_token.access_token = str(new_access_token)
            custom_token.refresh_token = str(refresh_token)
            custom_token.access_token_expires_at = timezone.now() + timedelta(hours=1, minutes=1)
            custom_token.refresh_token_expires_at = timezone.now() + timedelta(hours=1, days=1)
            custom_token.save()

            return Response({'access_token': str(new_access_token), 'refresh_token': str(refresh_token)},  status=status.HTTP_200_OK)
            
        else:
            return Response({"Error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)
        


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = serializer.validated_data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
        

class InitiatePasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = InitiatePasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = get_object_or_404(CustomUser, email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"https://zyn-crm.onrender.com/accounts/reset-password/{uid}/{token}/"
        # subject = 'Password Reset!'
        # html_message = render_to_string('accounts/password_reset_email.html', {'uid': uid, 'token': token, 'reset_link': reset_link})
        # plain_message = strip_tags(html_message)
        # from_email = config('DEFAULT_FROM_EMAIL_2')  # Replace with your email
        # to = email
        # send_mail(subject, plain_message, from_email, [to], html_message=html_message)
       

        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
            to=[mt.Address(email="edwardprosper001@gmail.com")],
            subject="Password Reset!",
            text=reset_link,
            category="Integration Test",
        )

        client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
        client.send(mail)
        return Response({"Success": "Password Reset email sent!"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None, **kwargs):
        data = {}
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_otp = serializer.validated_data.get("otp_token")
        user = get_object_or_404(OTPToken, otp_code=input_otp).user
        if OTPToken.objects.filter(user=user).last().otp_code == input_otp:
            refresh = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            custom_token, _ = CustomToken.objects.get_or_create(user=user)
            custom_token.access_token = str(access_token)
            custom_token.refresh_token = str(refresh)
            custom_token.access_token_expires_at = timezone.now() + timedelta(hours=1, minutes=60)
            custom_token.refresh_token_expires_at = timezone.now() + timedelta(days=1, hours=1)
            custom_token.save()
            if user.is_superuser and user.is_staff:
                    data["user_type"] = "Admin"  
            elif user.is_staff and user.is_active:
                    data["user_type"] = "Manager"
            else:
                data["user_type"] = "Regular"
  
            return Response({"Success": "Verification successful",
                             "data": data,
                            'access_token': str(access_token),
                            'refresh_token': str(refresh)
                             }, status=status.HTTP_200_OK)
        return Response({"Message": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)
    


class CreateLeadView(ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class RetrieveLeadsView(ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = RetrieveLeadsSeializer
    permission_classes = [IsAuthenticated]
    search_fields = ['first_name', 'last_name', 'lead_source']
    filter_backends = [SearchFilter, OrderingFilter]


class GetUpdateDeleteLeadsView(APIView):
    def get(self, request, id, format=None, **kwargs):
        current_lead = get_object_or_404(Lead, id=id)
        serializer = RetrieveLeadsSeializer(current_lead)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, format=None, **kwargs):
        current_lead = get_object_or_404(Lead, id=id)
        serializer = RetrieveLeadsSeializer(current_lead, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Update saved!"}, status=status.HTTP_202_ACCEPTED)
    

    def delete(self, request, id, format=None, **kwargs):
        current_lead = get_object_or_404(Lead, id=id)
        current_lead.delete()
        return Response({"Success": "Lead deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]


class SingleProductView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, product_slug, format=None, **kwargs):
        current_product = get_object_or_404(Product, product_slug=product_slug)
        serializer = ProductSerializer(current_product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, product_slug, format=None, **kwargs):
        current_product = get_object_or_404(Product, product_slug=product_slug)
        serializer = ProductSerializer(current_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, product_slug, format=None, **kwargs):
        current_product = get_object_or_404(Product, product_slug=product_slug)
        current_product.delete()
        return Response({"Success": "Product Deletion Successful"}, status=status.HTTP_204_NO_CONTENT)

       
class RetrieveUserProfile(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)




    # def post(self, request, format=None, **Kwargs):
    #     new_lead = LeadSerializer(data=request.data)
    #     new_lead.is_valid(raise_exception=True)
    #     new_lead.save()
    #     return Response({"Success": "Lead Creation Successful"}, status=status.HTTP_201_CREATED)



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        print(user)
        total_leads_count = Lead.objects.all().count()
        # user_leads = Lead.objects.filter(user=user).count()
        return Response({
            "total_leads_count": total_leads_count,
            # "user_leads": user_leads
        }, status=status.HTTP_200_OK)
    


class CreateCustomerAccountView(APIView):
    def post(self, request, format=None, *args, **kwargs):
        serializer = CreateCustomerAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Customer Account Creation Successful",
                         "data": serializer.data}, status=status.HTTP_201_CREATED)
    

class CreateOpportunityView(APIView):
    def post(self, request, format=None, *args, **kwargs):
        serializer = CreateOpportunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Opportunity Creation Successful",
                         "data": serializer.data}, status=status.HTTP_201_CREATED)
    


class OpportunityView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        opportunity_slug = kwargs.get("opportunity_slug")
        current_opportunity = get_object_or_404(Opportunity, Opportunity_slug=opportunity_slug)
        serializer = OpportunitySerializer(current_opportunity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


        

