from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import *
from django.db import transaction


class StudentCreateForm(UserCreationForm):

    student_validator = RegexValidator("^[1-9][0-9]{7}$", "The student number is not valid")
    student_number = forms.CharField(
        validators=[student_validator], max_length=8)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'student_number', 'first_name', 'last_name', 'address', 'city', 'postal_code', 'telephone']

    def clean_student_number(self):
        student_number = self.cleaned_data.get("student_number")
        if Student.objects.filter(student_number=student_number).exists():
            raise forms.ValidationError("This student number is already in use")
        return student_number

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.student_number = self.cleaned_data['student_number']
        student.save()
        return user


class CompanyCreateForm(UserCreationForm):
    siret_validator = RegexValidator( "^[1-9][0-9]{13}$", "The siret is not valid")

    siret = forms.CharField(validators=[siret_validator], max_length=14)
    description = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'siret', 'last_name', 'description', 'address', 'city', 'postal_code', 'telephone' ]


    def clean_siret(self):
        siret = self.cleaned_data.get("siret")
        if Company.objects.filter(siret=siret).exists():
            raise forms.ValidationError("A company is already registered under this siret")
        return siret

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user)
        company.siret = self.cleaned_data['siret']
        company.description = self.cleaned_data['description']
        company.save()
        return user


class RepresentativeCreateForm(UserCreationForm):
    siret_validator = RegexValidator(
        "^[1-9][0-9]{13}$", "The siret is not valid")

    siret = forms.CharField(validators=[siret_validator], max_length=14)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'siret', 'first_name', 'last_name', 'address', 'city', 'postal_code', 'telephone' ]


    def clean_siret(self):
        siret = self.cleaned_data.get("siret")
        if not Company.objects.filter(siret=siret).exists():
            raise forms.ValidationError("this company does not exist")
        return siret

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_representative = True
        user.save()
        siret = self.cleaned_data['siret']
        company = Company.objects.get(siret=siret)
        representative = Representative.objects.create(user=user, company=company)
        representative.save()
        return user


class UpdateUserStudentForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'city', 'postal_code', 'telephone']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number']




class UpdateUserCompanyForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['email', 'last_name', 'address', 'city', 'postal_code', 'telephone']

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['siret', 'description']


class UpdateUserRepresentativeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'city', 'postal_code', 'telephone']