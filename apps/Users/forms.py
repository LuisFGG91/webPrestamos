
from django import forms
from .models import User,LenderProfile,BorrowerProfile

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control",
                "value": "Admin"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control",
                "value": "ApS12_ZZs8"
            }
        ))

class SignUpFormBorrower(forms.Form):
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Last name",                
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "First_name",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    need_money_for = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "for",                
                "class": "form-control",
            }
        ))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder" : "Description",                
                "class": "form-control",
                "placeholder":"Descripcion..." ,
                "id":"textarea" ,
                "rows":"4"
            }
        ))
    amount_need = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Amount_need",                
                "class": "form-control",
            }
        ))
    
    def save(self, request,commit=True):
        
        data = self.cleaned_data
        user = User(
            email=data['email'], 
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_borrower=True)
        user.set_password(data['password'])
        user.save()
        
        userProfile = BorrowerProfile(user=user,
                                      need_money_for=data['need_money_for'],
                                      description=data['description'],
                                      amount_need=data['amount_need'])
        userProfile.save()
        return user
    

class SignUpFormLander(forms.Form):

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Last name",                
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "First name",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    money = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Money",                
                "class": "form-control",
            }
        ))
    def save(self, request,commit=True):
        
        data = self.cleaned_data
        user = User(
            email=data['email'], 
            first_name=data['first_name'],
            last_name=data['last_name'], 
            is_lander=True)
        user.set_password(data['password'])
        user.save()
        
        userProfile = LenderProfile(user=user,money=data['money'])
        userProfile.save()
        return user

