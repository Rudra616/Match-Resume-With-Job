from django import forms
from .models import Job

class ResumeUploadForm(forms.Form):
    resume = forms.FileField()

class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'skills']
