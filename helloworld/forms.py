from django import forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
        'password': forms.PasswordInput(),
        'password2': forms.PasswordInput()
    }