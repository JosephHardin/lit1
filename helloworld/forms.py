from django.forms import ModelForm
from helloworld.models import User
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        #widgets = {
        #'password': forms.PasswordInput(),
        #'password2': forms.PasswordInput()
    #}

