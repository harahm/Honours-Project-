from django import forms

from django.contrib.auth.models import User
from hubcarapp.models import Garage, Item

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ("name", "phone", "address", "logo")

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ("garage",)
