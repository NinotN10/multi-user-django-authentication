from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_company', False)
        extra_fields.setdefault('is_representative', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    telephone_validator = RegexValidator("^(\\+33|0|0033)[1-9][0-9]{8}$", "The phone number is not valid")
    postal_validator = RegexValidator("^(([0-8][0-9])|(9[0-5])|(2[ab]))[0-9]{3}$", "The postcode is not valid")

    username = None
    email = models.EmailField(_('email address'), unique=True)

    #Les 3 types d'utilisateur que je désire
    is_student = models.BooleanField(_('student'), default=False)
    is_company = models.BooleanField(_('company'), default=False)
    is_representative = models.BooleanField(_('representative'), default=False)

    address = models.CharField(max_length=60)
    city = models.CharField(max_length=35)
    postal_code = models.CharField(validators=[postal_validator], max_length=5, verbose_name="postal code")
    telephone = models.CharField(max_length=12, validators=[telephone_validator])
    modification = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Student(models.Model):
    student_validator = RegexValidator("^[1-9][0-9]{7}$", "The student number is not valid")

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    student_number = models.CharField(validators=[student_validator], max_length=8, verbose_name="student number", unique=True)

    def __str__(self):
        return self.student_number


class Company(models.Model):
    siret_validator = RegexValidator("^[1-9][0-9]{13}$", "the siret is not valid")

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='company')
    siret = models.CharField(validators=[siret_validator], max_length=14, unique=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.siret


class Representative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='representative')
    company = models.ForeignKey(Company, to_field='siret', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
