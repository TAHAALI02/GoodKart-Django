from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        # 'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm Password',
        
    }))
    class Meta:
       model = Account
       fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Mobile Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    
    # backend Validation
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if Account.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exists")
    #     return email

    def clean(self):
        data = super(RegistrationForm, self).clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Enter Same Password for both")
        number = data.get("phone_number")
        # if len(number)<9 and len(number)>12:
        #     raise forms.ValidationError(
        #     "Number shoukd be contains more than 10 digits or less 12"
        #     )
        # if Account.objects.filter(phone_number=number).exists():
        #     raise forms.ValidationError("Phone number already exists")
        # return data
        

    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")
    #     return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if Account.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             "Email already exixts in our DB use Another email"
    #             )