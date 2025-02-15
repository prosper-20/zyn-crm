from rest_framework import serializers
from .models import CustomUser, Contact, Industry, Department, Organization, Lead, Product, CustomerAccount, Opportunity
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class DepratmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class OrganizationDepartmentSerializer(serializers.ModelSerializer):
    departments = DepratmentSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["departments"]


class ListOrganizationSerializer(serializers.ModelSerializer):
    industry_name = serializers.SerializerMethodField("get_industry_name")
    industry_slug = serializers.SerializerMethodField("get_industry_slug")
    class Meta:
        model = Organization
        fields = ["name",  "slug", "industry", "industry_name", "industry_slug"]

    def get_industry_name(self, obj):
        return obj.industry.industry_name
    
    def get_industry_slug(self, obj):
        return obj.industry.industry_slug

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "industry"]

# class DashBoardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lead
#         fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ["id", "industry_name", "industry_slug", "industry_description"]


class CreateOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ["opportunity_name", "account_name", "product_description", "amount", "rating", "owner"]


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ["id", "opportunity_name", "Opportunity_slug", "account_name", "product_description", "amount", "rating", "owner"]


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
    

class PartnerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    organization = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "organization", "password", "password2"]
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
        user.is_partner = True
        user.save()
        user.profile.organization = self.validated_data["organization"]
        user.profile.save()
        return user
    


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    organization = serializers.CharField(max_length=100, required=True)
    department = serializers.CharField(max_length=100, required=True)

    def validate_organization(self, value):
        try:
            # Check if an organization with the given slug exists
            # Organization.objects.get(slug=value)
            current_organization = get_object_or_404(Organization, name=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization with this slug does not exist.")
        return value
    
    def validate_department(self, value):
        organization_name = self.initial_data.get('organization')
        try:
            organization = Organization.objects.get(name=organization_name)
            print(organization.departments)
            # Check if the department exists within the organization
            if not organization.departments.filter(name=value).exists():
                raise serializers.ValidationError("Department with this slug does not exist in the specified organization.")
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Cannot validate department because organization does not exist.")
        return value


    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "organization", "department", "password", "password2"]
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
        user.is_employee = True
        user.save()
        user.profile.organization = self.validated_data["organization"]
        user.profile.department = self.validated_data["department"]
        user.profile.save()
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
        fields = ['id', 'first_name', 'last_name', 'lead_source', 'job_title', 'phone', 'office_email', 'personal_email', 'address', 'company', 'lead_rating', 'city', 'state', 'zip_code', 'country', 'description', 'lead_owner', 'company_id', 'created_by', 'created_date', 'modified_by', 'modified_date']



class RetrieveLeadsSeializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField()
    phone_number = serializers.SerializerMethodField("get_phone_number")
    lead_count = serializers.SerializerMethodField("get_leads_count")
    email = serializers.SerializerMethodField("get_personal_email")
    alias = serializers.SerializerMethodField("get_alias")


    class Meta:
        model = Lead
        fields = ['id', 'lead_count', 'first_name', 'account_name', 'job_title', 'phone_number', 'email', 'alias', 'company', 'lead_rating', 'lead_status']

    
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