from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from .models import Note,CreationFile
from django.forms.formsets import BaseFormSet



class phaseForm(forms.Form):
    phaseName=forms.CharField(max_length=100, required=True)

class newProgramSingleForm(forms.Form):
    customer_id=forms.CharField(max_length=100, required=True)


class CreationFileForm(forms.ModelForm):
    class Meta:
        model=CreationFile
        fields=['audioFile']
        widgets = {
            'audioFile': forms.FileInput(attrs={'accept': 'audio/*'}),
        }


class phaseStatusForm(forms.Form):
    changes = forms.CharField(widget=forms.Textarea(attrs={'dir': 'ltr'}))

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=200,
                                error_messages={
                                    "required": "יש להזין שם משתמש/אימייל",
                                    "max_length": "יש להזין שם קצר יותר"
                                })
    passcode = forms.CharField(widget=forms.PasswordInput(),
                               error_messages={
        "required": "יש להזין סיסמה"
    })


class UpdateUserDetailsForm(forms.Form):
    fname = forms.CharField(max_length=100,min_length=2)
    lname=forms.CharField(max_length = 100,min_length=2)
    city=forms.CharField(max_length=100,min_length=2)
    phone=forms.CharField(max_length=100,min_length=2)
    dob = forms.DateField(
        #widget=forms.DateInput(format='%d-%m-%Y'),
        widget=DatePickerInput,        
    )

    organization=forms.CharField(max_length=100,required=False)
    current_password=forms.CharField(widget=forms.PasswordInput())
    new_password=forms.CharField(widget=forms.PasswordInput())
    repeat_new_password=forms.CharField(widget=forms.PasswordInput(), required=False)


class AddNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
