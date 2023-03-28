import re
from functools import wraps

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from django.shortcuts import redirect

from web.models import EmployeeDetails


def valid_pincode(value):
    """
    If the length of the string representation of the value is not equal to 6, raise a ValidationError
    
    :param value: The value that is being validated
    """
    if len(str(value)) != 6:
        raise forms.ValidationError('Invalid Pincode(Valid e.g., 123456)')


def valid_contact(value):
    """
    If the length of the string representation of the value is not equal to 10, raise a validation error
    
    :param value: The value that is being validated
    """
    if len(str(value)) != 10:
        raise forms.ValidationError('Invalid Contact Number(Valid e.g., 9988774455)')


def valid_salary(value):
    """
    If the value doesn't match the regex or is longer than 7 characters, raise a validation error
    
    :param value: The value that is being validated
    """
    salary_regex = re.compile(r'^[1-9][0-9]*$')
    if not salary_regex.match(value) or len(value) > 7:
        raise forms.ValidationError('Invalid Salary, Should be a positive integer with maximum 7 digit')


def check_employee_exists(view_func):
    """
    Used for checking whether slug matching object exists in db
    
    :param view_func: The view function that we are decorating
    :return: The wrapper function is being returned.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        try:
            employee = EmployeeDetails.objects.get(slug=kwargs.get('slug'))
            kwargs['employee'] = employee
            return view_func(self, request, *args, **kwargs)
        except ObjectDoesNotExist:
            messages.error(request, 'No record found')
            return redirect('/')
    return wrapper
