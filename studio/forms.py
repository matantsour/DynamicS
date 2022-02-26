from django import forms


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
    fname1 = forms.CharField(max_length=100)
    lname1 = forms.CharField(max_length=100)
    city1 = forms.CharField(max_length=100)
    phone1 = forms.CharField(max_length=12)
    dob1 = forms.DateField()
    organization1 = forms.CharField(max_length=100)
    current_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    repeat_new_password1 = forms.CharField(widget=forms.PasswordInput())