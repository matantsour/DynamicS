from django import forms
class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=200,
    error_messages={
        "required": "יש להזין שם משתמש/אימייל",
        "max_length":"יש להזין שם קצר יותר"
    })
    passcode=forms.CharField(error_messages={
        "required": "יש להזין סיסמה"
    })