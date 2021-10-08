from django.contrib import admin

from accounts.models import Company, Student, Representative, User

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Representative)