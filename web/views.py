from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic, View

from .forms import CreateEmployeeForm, UpdateSalaryForm, UpdateEmployeeForm
from .models import EmployeeDetails
from .utils import check_employee_exists


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """
        If the user is authenticated, redirect them to the homepage. Otherwise, render the login page

        :param request: The request object
        :return: The login page is being returned.
        """
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'authentication/login.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        It logs out the user and redirects them to the login page

        :param request: The request object
        :return: The user is being logged out and redirected to the login page.
        """
        logout(request)
        return redirect("login")


class IndexView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        """
        It takes a request, and returns a rendered template with a list of all employees who have the
        current user as their manager

        :param request: The request object
        :return: The list of all employees that are assigned to the manager.
        """
        all_employees = EmployeeDetails.objects.filter(manager=request.user)
        return render(request, 'employee/list.html', {'object_list': all_employees})


class CreateEmployee(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """
        It renders a form template with a form object and a heading

        :param request: The request object
        :return: A form that allows the user to create a new employee.
        """
        employee_form = CreateEmployeeForm()
        return render(request, 'employee/form_template.html', {
            'form': employee_form,
            'heading': 'Add Employee'
        })

    def post(self, request, *args, **kwargs):
        """
        If the form is valid, save the form, but don't commit it to the database yet.
        Then, set the manager field to the current user, and save the form to the database.
        If the form is not valid, render the form template with the form and a heading

        :param request: The request object
        :return: A redirect to the update-salary page.
        """
        employee_form = CreateEmployeeForm(request.POST)
        if employee_form.is_valid():
            employee = employee_form.save(commit=False)
            employee.manager = request.user
            employee.save()
            return redirect('update-salary', slug=employee.slug)
        else:
            return render(request, 'employee/form_template.html', {
                'form': employee_form,
                'heading': 'Add Employee'
            })


class UpdateSalary(LoginRequiredMixin, View):

    @check_employee_exists
    def get(self, request, *args, **kwargs):
        """
        If the employee exists, then render the form

        :param request: The request object
        :return: A form with the heading "Add Salary"
        """
        employee = kwargs.get('employee')
        employee_form = UpdateSalaryForm(instance=employee)
        return render(request, 'employee/form_template.html', {
            'form': employee_form,
            'heading': 'Add Salary'
        })

    @check_employee_exists
    def post(self, request, *args, **kwargs):
        """
        It checks if the employee exists, if it does, it updates the salary, if it doesn't, it redirects
        to the homepage

        :param request: The request object
        :return: The employee_form is being returned.
        """
        employee = kwargs.get('employee')
        employee_form = UpdateSalaryForm(instance=employee, data=request.POST)
        if employee_form.is_valid():
            employee.salary = employee_form.cleaned_data['salary']
            employee.save()
        else:
            return render(request, 'employee/form_template.html', {
                'form': employee_form,
                'heading': 'Add Salary'
            })
        messages.success(request, 'The record was saved successfully')
        return redirect('/')


class UpdateEmployee(LoginRequiredMixin, View):

    @check_employee_exists
    def get(self, request, *args, **kwargs):
        """
        If the employee exists, then render the form template with the employee form and heading

        :param request: The request object
        :return: A form with the employee's information already filled in.
        """
        employee = kwargs.get('employee')
        employee_form = UpdateEmployeeForm(instance=employee)
        return render(request, 'employee/form_template.html', {
            'form': employee_form,
            'heading': 'Update Employee'
        })

    @check_employee_exists
    def post(self, request, *args, **kwargs):
        """
        If the employee exists, then update the employee with the data from the form

        :param request: The request object
        :return: The employee_form is being returned.
        """
        employee = kwargs.get('employee')
        employee_form = UpdateEmployeeForm(instance=employee, data=request.POST)
        if employee_form.is_valid():
            employee_form.save()
            return redirect('/')
        else:
            return render(request, 'employee/form_template.html', {
                'form': employee_form,
                'heading': 'Update Employee'
            })


class DeleteEmployee(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        """
        If the employee exists, delete the employee and return a JSON response with a success message

        :param request: The request object
        :return: A JsonResponse object is being returned.
        """
        employee = EmployeeDetails.objects.get(slug=request.POST['slug'])
        employee.delete()
        messages.success(request, 'The record was deleted successfully')
        return JsonResponse({'success': True})
