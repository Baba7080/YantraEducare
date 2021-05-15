from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer, AccountDetails,Profile
from django.forms import TextInput
from quiz.models import schoo_dashbored



class SchoolForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Principal','manager','city_of_school']
class school_dashbored_form(forms.ModelForm):
    class Meta:
        model = schoo_dashbored
        fields = "__all__"
#Registration Form
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        label = {'email':'Email'}
        widget = {'username':forms.TextInput(attrs={'class':'form-control'})}

#Vendors Registration form



#Login Form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs=
        {'autocomplete':'current-password', 'class':'form-control'}))


#Change Password Form
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=('Old Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))

    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.
        password_validators_help_text_html())

    new_password2 = forms.CharField(label=('Confirm New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}))


# Reset Password Form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=('Email'),max_length=255, widget=forms.EmailInput
        (attrs={'autocomplete':'email','class':'form-control'}))



#Confirm Reset Password Form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.
        password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}))




class CustomerProfileform(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode','code']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                'locality':forms.TextInput(attrs={'class':'form-control'}),
                'city':forms.TextInput(attrs={'class':'form-control'}),
                'state':forms.Select(attrs={'class':'form-control'}),
                'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
                'code':forms.NumberInput(attrs={'class':'form-control'}),

        }

class UserUpdateForms(forms.ModelForm):
    class Meta:
        model = User
        fields = []

class ProfileUpdateForm(forms.ModelForm):
    # Category = forms.CharField(max_length=100)
    # bio = forms.CharField(max_length=100)
    # image = forms.ImageField()
    class Meta:

        model = Profile
        fields = ['Category','image']
class Accountform(forms.ModelForm):
    class Meta:
        model = AccountDetails
        fields = ['id','Bank_Name','Beneficially_Name','Account_Number','Re_Enter_Account_Number',
        'IFSC_Code','Branch_Name','Branch_Address','UPI_ID','Paytm_Number', 'PhonePe_Number', 'Google_Pay_Number']
        
   

        widgets = {'Bank_Name':forms.TextInput(attrs={'class':'form-control'}),
                'Beneficially_Name':forms.TextInput(attrs={'class':'form-control'}),
                'Account_No':forms.TextInput(attrs={'class':'form-control'}),
                'Re_Enter_Account_Number':forms.TextInput(attrs={'class':'form-control'}),
                'IFSC_Code':forms.TextInput(attrs={'class':'form-control'}),
                'Branch_Name':forms.TextInput(attrs={'class':'form-control'}),
                'Branch_Address':forms.TextInput(attrs={'class':'form-control'}),
                'UPI_ID':forms.EmailInput(attrs={'class':'form-control'}),
                'Paytm_Number':forms.TextInput(attrs={'class':'form-control'}),
                'PhonePe_Number.':forms.TextInput(attrs={'class':'form-control'}),
                'Google_Pay_number':forms.TextInput(attrs={'class':'form-control'}),
                

        }

# class UserUpdateForms(forms.ModelForm):
#     email= forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username','email']

# class ProfileUpdateForm(forms.ModelForm):
#     Cotegory = forms.CharField(max_length=100)
#     bio = forms.CharField(max_length=100)
#     class Meta:

#         model = Profile
#         fields = ['Cotegory','bio']

CATEGORY_CHOICE = (
    ('Student','Student'),
    ('Teacher','Teacher'),
    ('Affiliate Partner','Affiliate Partner')
)

class Categoryselection(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Category']
        widgets = {
            'Category':forms.RadioSelect(choices=CATEGORY_CHOICE)
        }
        