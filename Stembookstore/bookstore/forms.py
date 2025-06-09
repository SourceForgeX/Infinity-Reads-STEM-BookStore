from django import forms
from .models import *
class CategoryForm(forms.Form):
    Category=forms.ModelChoiceField()