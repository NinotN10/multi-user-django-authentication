from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth import login, update_session_auth_hash
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from accounts.forms import *
from accounts.models import *


# Registrations

class RegisterStudent(CreateView):
    model = User
    form_class = StudentCreateForm
    template_name = 'registration/student_form.html'
    success_url = reverse_lazy(login)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('accounts:login')
    
class RegisterCompany(CreateView):
    model = User
    form_class = CompanyCreateForm
    template_name = 'registration/company_form.html'
    success_url = reverse_lazy(login)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('accounts:login')


class RegisterRepresentative(CreateView):
    model = User
    form_class = RepresentativeCreateForm
    template_name = 'registration/representative_form.html'
    success_url = reverse_lazy(login)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'representative'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('accounts:login')





#Authentication and redirection by type

class Login_View(LoginView):
    def get_success_url(self):
        if self.request.user.is_student == True:
            return reverse_lazy('accounts:profile_student', args=[self.request.user.pk])
        elif self.request.user.is_company == True:
            return reverse_lazy('accounts:profile_company', args=[self.request.user.company.siret])
        elif self.request.user.is_representative == True:
            return reverse_lazy('accounts:profile_representative', args=[self.request.user.pk])




#Information display
class ProfileStudent(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/profile_student.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class ProfileCompany(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/profile_company.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class ProfileRepresentative(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/profile_representative.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user



#Deconnexion
class Logout_View(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('accounts:home')



#Deleting the account
class Delete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/confirm_delete.html'



#Update of information

@login_required
def StudentUpdate(request, pk):
    if request.method == 'POST':
        form_user = UpdateUserStudentForm(request.POST, instance=request.user)
        form_student = StudentUpdateForm(request.POST, instance=request.user.student)

        if form_user.is_valid():
            form_user.save()
            form_student.save()
            return redirect('accounts:profile_student', pk)
    else:
        form_user = UpdateUserStudentForm(instance=request.user)
        form_student = StudentUpdateForm(instance=request.user.student)
        args = {'form': form_user, 'student': form_student}
    return render(request, 'registration/update_student.html', args)

@login_required
def CompanyUpdate(request, siret):
    if request.method == 'POST':
        form_user = UpdateUserCompanyForm(request.POST, instance=request.user)
        form_company = CompanyUpdateForm(request.POST, instance=request.user.company)

        if form_user.is_valid():
            form_user.save()
            form_company.save()
            return redirect('accounts:profile_company', siret)
    else:
        form_user = UpdateUserCompanyForm(instance=request.user)
        form_company = CompanyUpdateForm(instance=request.user.company)
        args = {'form': form_user, 'company': form_company}
    return render(request, 'registration/update_company.html', args)

@login_required
def RepresentativeUpdate(request, pk):
    if request.method == 'POST':
        form_user = UpdateUserRepresentativeForm(request.POST, instance=request.user)

        if form_user.is_valid():
            form_user.save()
            return redirect('accounts:profile_representative', pk)
    else:
        form_user = UpdateUserRepresentativeForm(instance=request.user)
        args = {'form': form_user}
    return render(request, 'registration/update_representative.html', args)



#change the password

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if not form.is_valid():
            return redirect('accounts:change_password')
        form.save()
        update_session_auth_hash(request, form.user)
        if request.user.is_student == True:
            return redirect('accounts:profile_student', request.user.pk)
        elif request.user.is_company == True:
            return redirect('accounts:profile_company', request.user.company.siret)
        elif request.user.is_representative == True:
            return redirect('accounts:profile_representative', request.user.pk)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'registration/change_password.html', args)