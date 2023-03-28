from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create-employee/', views.CreateEmployee.as_view(), name='create-employee'),
    path('update-salary/<slug:slug>', views.UpdateSalary.as_view(), name='update-salary'),
    path('update-employee/<slug:slug>', views.UpdateEmployee.as_view(), name='update-employee'),
    path('delete-employee/', views.DeleteEmployee.as_view(), name='delete-employee')
]
