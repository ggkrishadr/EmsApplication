from django import forms

from web.models import EmployeeDetails
from web.utils import valid_contact, valid_pincode, valid_salary


class BasicFieldMixin(forms.Form):
    name = forms.CharField(required=True)
    code = forms.CharField(required=True)


class ExtraFieldsMixin(forms.Form):
    address = forms.CharField(required=True, widget=forms.Textarea)
    pincode = forms.CharField(validators=[valid_pincode])
    contact = forms.CharField(validators=[valid_contact])


class SalaryFieldMixin(forms.Form):
    salary = forms.CharField(validators=[valid_salary])


class CreateEmployeeForm(BasicFieldMixin, ExtraFieldsMixin, forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ('name', 'code', 'address', 'pincode', 'contact')

    def __init__(self, *args, **kwargs):
        super(CreateEmployeeForm, self).__init__(*args, **kwargs)


class UpdateSalaryForm(BasicFieldMixin, SalaryFieldMixin, forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ('name', 'code', 'salary')

    def __init__(self, *args, **kwargs):
        super(UpdateSalaryForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['code'].widget.attrs['readonly'] = True


class UpdateEmployeeForm(BasicFieldMixin, ExtraFieldsMixin, SalaryFieldMixin, forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ('name', 'code', 'address', 'pincode', 'contact', 'salary')
