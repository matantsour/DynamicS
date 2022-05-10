from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from .models import Note,CreationFile
import datetime

class newProgramSingleForm(forms.Form):
    creator_choice=forms.CharField(max_length=100, required=True,widget=forms.HiddenInput())
    creation_name=forms.CharField(max_length=200, required=True,widget=forms.HiddenInput())
    phases_names=forms.CharField(max_length=1000, required=True,widget=forms.HiddenInput())
    creation_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('musical', 'יצירה מוזיקלית'), ('other', 'יצירה אחרת')],initial={'musical':'יצירה מוזיקלית'})
    start_date=forms.DateField(required=True,initial=datetime.date.today,widget=DatePickerInput)
    start_time=forms.TimeField(required=True,widget=TimePickerInput)
#widget=forms.HiddenInput()


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


class TimePickerInput(forms.TimeInput):
        input_type = 'time'

class ReportHoursForm(forms.Form):
    reporting_date=forms.DateField(required=True,initial=datetime.date.today)
    creation=forms.CharField(max_length=200, required=True)
    starting_time=forms.TimeField(required=True,widget=TimePickerInput)
    ending_time = forms.TimeField(required=True,widget=TimePickerInput)
#widget=forms.HiddenInput()