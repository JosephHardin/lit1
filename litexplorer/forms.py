from django import forms


class IdForm(forms.Form):
    idtype = forms.CharField(label="ID_Type")
    id = forms.CharField(label="ID", max_length=15, error_messages={"required": "Please Provide a valid ID"})