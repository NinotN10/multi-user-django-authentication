from django.urls import path
from django.views.generic.base import TemplateView
from accounts.views import *

app_name='accounts'
urlpatterns = [
    #Inscription
    path('register/student/', RegisterStudent.as_view(), name='registerStudent'),
    path('register/company/', RegisterCompany.as_view(), name='registerCompany'),
    path('register/representative/', RegisterRepresentative.as_view(), name='registerRepresentative'),

    #Connexion
    path('login/', Login_View.as_view(), name='login'),

    #Déconnexion
    path('logout/', Logout_View.as_view(), name='logout'),
    
    #Detail des profils
    path('profil_student/<int:pk>', ProfileStudent.as_view(), name='profile_student'),
    path('profil_company/<int:siret>', ProfileCompany.as_view(), name='profile_company'),
    path('profil_representative/<int:pk>', ProfileRepresentative.as_view(), name='profile_representative'),

    #home
    path('home/', TemplateView.as_view(template_name="registration/home.html"), name='home'),

    #Suppression des comptes
    path('profil_student/<int:pk>/delete/', Delete.as_view(), name='delete'),
    path('profil_company/<int:siret>/delete/', Delete.as_view(), name='delete'),
    path('profil_representative/<int:pk>/delete/', Delete.as_view(), name='delete'),

    #Mise à jour des profils
    path('profil_student/<int:pk>/update/', StudentUpdate, name='student_update'),
    path('profil_company/<int:siret>/update/', CompanyUpdate, name='company_update'),
    path('profil_representative/<int:pk>/update/', RepresentativeUpdate, name='representative_update'),

    #Changement de mot de passe
    path('changepassword/', ChangePassword, name='change_password'),
]