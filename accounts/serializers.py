from rest_framework import serializers
from .models import CustomUser, Contact, Lead, Product, CustomerAccount, Opportunity
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# class DashBoardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lead
#         fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class CreateOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ["opportunity_name", "account_name", "product_description", "rating", "owner"]


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password", "password2"]
        extra_kwargs = {
            "password":  {"write_only": True}
        }
    

    def save(self):
        user = CustomUser(
            username = self.validated_data["username"],
            email = self.validated_data["email"],
            phone_number = self.validated_data["phone_number"]
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Error": "Both passwords must match"})
        
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    email_or_phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    
    def validate(self, data):
        email = data.get('email_or_phone_number')
        password = data.get('password')

        if email and password:
            if "@" not in email:
                phone_number = data.get("email_or_phone_number")
                email = get_object_or_404(CustomUser, phone_number=phone_number).email
                user = authenticate(email=email, password=password)

                if user:
                    if not user.is_active:
                        msg = 'User account is disabled.'
                        raise serializers.ValidationError(msg, code='authorization')
                else:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                user = authenticate(email=email, password=password)

                if user:
                    if not user.is_active:
                        msg = 'User account is disabled.'
                        raise serializers.ValidationError(msg, code='authorization')
                else:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

        # print(email)
        # print(password)

        # if email and password:
        #     if "@" in email:
        #         print("abs")

    
        # if email and password:
        #     if "@" not in email:
        #         phone_number = data.get("email")
        #         email = CustomUser.objects.get(phone_number=phone_number).email
        #         print("ee", email)
        #         user = authenticate(email=email, password=password)

        #         print(user)

        #         if user:
        #             if not user.is_active:
        #                 msg = 'User account is disabled.'
        #                 raise serializers.ValidationError(msg, code='authorization')
        #         else:
        #             msg = 'Unable to log in with provided credentials.'
        #             raise serializers.ValidationError(msg, code='authorization')
        #     else:
       



class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100, required=True)
    confirm_new_password = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Both passwords do not match.")

        return data
    


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1000, required=True)



class InitiatePasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError("Email address does not exist.")



class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=20, style= {'input_type': 'password'}, write_only=True)
    confirm_new_password = serializers.CharField(max_length=20, style= {'input_type': 'password'}, write_only=True)

    def validate_passwords(self, value):
        if self.new_password != self.confirm_new_password:
            raise serializers.ValidationError({"Response": "Both passwords must match"})
        

class VerifyOTPSerializer(serializers.Serializer):
    otp_token = serializers.CharField(max_length=4)



class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'lead_source', 'job_title', 'phone', 'office_email', 'personal_email', 'address', 'city', 'state', 'zip_code', 'country', 'company', 'lead_rating', 'description', 'lead_owner', 'company_id', 'created_by', 'created_date', 'modified_by', 'modified_date']



class RetrieveLeadsSeializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField()
    phone_number = serializers.SerializerMethodField("get_phone_number")
    lead_count = serializers.SerializerMethodField("get_leads_count")
    email = serializers.SerializerMethodField("get_personal_email")
    alias = serializers.SerializerMethodField("get_alias")


    class Meta:
        model = Lead
        fields = ['id', 'lead_count', 'first_name', 'account_name', 'job_title', 'phone_number', 'email', 'alias']

    
    def get_leads_count(self, obj):
        return Lead.objects.all().count()
    
    def get_phone_number(self, obj):
        return obj.phone
    
    def get_personal_email(self, obj):
        return obj.personal_email
    
    def get_alias(self, obj):
        return obj.first_name
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]



class CreateCustomerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAccount
        fields = "__all__"