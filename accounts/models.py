from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import secrets, random
import string
from django.conf import settings
from django.utils.text import slugify



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users'  # Unique related_name for CustomUser model
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users'  # Change or add related_name here
    )
    

    objects = CustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]



    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Users"



class CustomToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token_expires_at = models.DateTimeField()
    refresh_token_expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} token"


    def save(self, *args, **kwargs):
        if not self.id:
            self.access_token_expires_at = timezone.now() + timedelta(hours=1, minutes=60)
            self.refresh_token_expires_at = timezone.now() + timedelta(hours=1, days=1)
        super(CustomToken, self).save(*args, **kwargs)

    def is_access_token_expired(self):
        return timedelta(hours=1) + timezone.now() >= self.access_token_expires_at

    def is_refresh_token_expired(self):
        return timedelta(hours=1)+ timezone.now() >= self.refresh_token_expires_at
    


class OTPToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=4, default=''.join(random.choices(string.digits, k=4)))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def _str__(self):
        return self.user.username
    
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Opportunity(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4)
    opportunity_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    product_description = models.TextField()
    close_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rating = models.IntegerField( validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ])
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.opportunity_name
    
    class Meta:
        verbose_name_plural = "Opportunities"
    

STAGE_CHOICES = (
    ("In Talks", "In Talks"),
    ("Part Payment", "Part Payment")
)

FORECAST_CATEGORY_CHOICES = (
    ("1", "1"),

)

NEXT_STEP_CHOICES = (
    ("Call", "Call"),
    ("Visit", "Visit")
)


class Status(models.Model):
    opportunity = models.OneToOneField(Opportunity, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES)
    forecast_category = models.CharField(max_length=100, choices=FORECAST_CATEGORY_CHOICES)
    probability = models.CharField(max_length=100)
    next_step = models.CharField(choices=NEXT_STEP_CHOICES, max_length=100)

    def __str__(self):
        return self.opportunity.opportunity_name
    
    class Meta:
        verbose_name_plural = "Status"



class Contact(models.Model):
    title = models.CharField(max_length=11)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    report_to = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    office_email = models.EmailField()
    personal_email = models.EmailField()
    address = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=100)
    zip_or_post_code = models.CharField(max_length=10)
    region = models.CharField(max_length=30)
    country = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    
class AccountType(models.Model):
    name = models.CharField(max_length=100)
    TempID = models.CharField(max_length=10, unique=True)
    AccountTypeID = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name




class DeptName(models.Model):
    DeptName = models.CharField(max_length=100)
    CompanyID = models.CharField(max_length=10)
    TempID = models.CharField(max_length=10, unique=True)
    DeptID = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.DeptName



class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.country_name




class LeadSource(models.Model):
    lead_source = models.CharField(max_length=200)
    TempID = models.CharField(max_length=10, unique=True)
    LeadSourceID = models.CharField(max_length=10, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.lead_source


class Lead(models.Model):
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    lead_source = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    office_email = models.EmailField(max_length=100)
    personal_email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    lead_rating = models.CharField(max_length=100)
    description = models.TextField()
    lead_owner = models.CharField(max_length=100)
    company_id = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    


class Employee(models.Model):
    EmpFirstName = models.CharField(max_length=100)
    EmpLastName = models.CharField(max_length=100)
    DeptID = models.CharField(max_length=100)
    ReportTo = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone = models.CharField(max_length=20)
    Address = models.CharField(max_length=200)
    Town = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    CompanyID = models.CharField(max_length=100)
    TempID = models.CharField(max_length=100)
    EmployeeID = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)


    def __str__(self):
        return self.EmpFirstName
    


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_slug = models.SlugField(max_length=100, blank=True, null=True)
    product_code = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    product_family = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    company_id = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_name)
        super().save(*args, **kwargs)




class LeadStatus(models.Model):
    LeadStatusID = models.AutoField(primary_key=True)
    LeadStatus = models.CharField(max_length=100, blank=True, null=True)
    TempID = models.CharField(max_length=100, blank=True, null=True)
    SalutationID = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.LeadStatus
    


class Privileges(models.Model):
    privilege_id = models.AutoField(primary_key=True)
    privilege_name = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.privilege_name
    


class RolePrivileges(models.Model):
    privilege_id = models.AutoField(primary_key=True)
    role_id = models.CharField(max_length=100)

    def __str__(self):
        return self.privilege_id



    



        
    



