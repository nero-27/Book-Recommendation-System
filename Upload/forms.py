from django import forms
from Accounts.models import Users


class login_form(forms.Form):
    Username = forms.CharField(
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
                                )
    Password = forms.CharField(
                                    widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}),
                                    required=True
                                )
    def clean(self):
        user = self.cleaned_data['Username']
        pass1 = self.cleaned_data['Password']
        if Users.objects.filter(Username=user):
            user1 = Users.objects.get(Username=user)
            if user1.Password == pass1:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Incorrect Password!")
        else:
            raise forms.ValidationError("User doesn't exist!")

    class Meta:
        model = Users
        fields = ["Username", "Password"]
        verbose_name_plural = "login_form"

class registration_form(forms.ModelForm):
    Password = forms.CharField(
                                    min_length = 5,
                                    widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}),
                                    required=True
                                )
    Username = forms.CharField(
                                    max_length=50,
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
                                )
    Age = forms.IntegerField(
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
                            )
    Re_Password = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-Password'}),
        required=True
    )

    def clean(self):
        user = self.cleaned_data['Username']
        if Users.objects.filter(Username = user):
            raise forms.ValidationError("User already exist!")
        else:
            pass1 = self.cleaned_data['Password']
            pass2 = self.cleaned_data['Re_Password']
            if pass2 != pass1:
                raise forms.ValidationError("Password don't match!")
            elif (user==pass1) or (user==pass2):
                raise forms.ValidationError("Username and Password should not be same!")
            else:
                age = self.cleaned_data['Age']
                if age < 5:
                    raise forms.ValidationError("Age is not valid! Valid Age: 5 to 90")
                elif age > 90:
                    raise forms.ValidationError("Age is not valid! Valid Age: 5 to 90")
                else:
                    return self.cleaned_data

    class Meta:
        model = Users
        fields = ["Username", "Password", "Re_Password", "Age"]
        verbose_name_plural = "registration_form"


