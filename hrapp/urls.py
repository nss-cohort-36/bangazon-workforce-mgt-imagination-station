from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),

    path('employees/', employee_list, name='employee_list'),
    path('employee/form', employee_form, name='employee_form'),
    path("employees/<int:employee_id>/",
         employee_details, name="employee_details"),
    path('employee/trainingprogram/<int:employee_id>/',
         employee_training_program_form, name="employee_training_program_form"),

    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path("departments/<int:department_id>/",
         department_details, name="department_details"),
    

    path('computers/', computer_list, name='computer_list'),
    path('computers/form', computer_form, name='computer_form'),
    path('computers/<int:computer_id>/',
         computer_details, name="computer_details"),

    path('training_programs/', training_program_list,
         name='training_program_list'),
    path('training_programs/form', training_program_form,
         name='training_program_form'),
    path("training_programs/<int:training_program_id>/",
         training_program_details, name="training_program_details"),
    path("training_programs/<int:training_program_id>/form/",
         training_program_edit_form, name="training_program_edit_form"),

]
