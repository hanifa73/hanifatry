from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    username=forms.CharField(max_length=30,label='الاسم',help_text='اسم المستخدم لا يجب ان يحتوي على مسافات')
    email=forms.EmailField(label='الايميل')
    first_name=forms.CharField(label='الاسم الاول')
    last_name=forms.CharField(label='الاسم الاخير')
    password1=forms.CharField(label='كلمة المرور',widget=forms.PasswordInput(),min_length=8)
    password2=forms.CharField(label=' تاكيد كلمةالمرور',widget=forms.PasswordInput(),min_length=8)
   
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','password1','password2')

    def clean_password(self):
        cd=self.cleaned_data
        if cd['password1'] !=['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقه')
        return cd['password2']

    def clean_username(self):
        cd=self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('الاسم موجود سابقا') 
        return cd['username'] 

class LoginForm(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم',help_text='اسم المستخدم لا يجب ان يحتوي على مسافات')
    password=forms.CharField(label='كلمة المرور',widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password')

    