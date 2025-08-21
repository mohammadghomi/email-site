from django import forms


class UserLoginForms(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'autocomplete': 'off'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_id',
            }
        )
    )
    show = forms.BooleanField(
        label='show password',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'show-password',
            }
        ),
        required=False
    )

