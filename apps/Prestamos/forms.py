from multiprocessing.sharedctypes import Value
from webbrowser import get
from django import forms
from apps.Users.models import LenderProfile, BorrowerProfile

from .models import Prestamos

class PrestamosForm(forms.ModelForm):
    
    amount_lent = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "$ 0",                
                "class": "form-control",
            }
        ))
    
    def save(self, request,pk,commit=True):

        lenderProfile =LenderProfile(id=request.user.lenderprofile.id)
        borrowerProfile =BorrowerProfile(id=pk)

        
        data = self.cleaned_data

        prestamos = Prestamos( 
            borrowerProfile = borrowerProfile,
            lenderProfile = lenderProfile,
            amount_lent =data['amount_lent']
            
            )
        prestamos.save()
        
        return prestamos

    def amount(self):

        amount_lent = None
        data = self.cleaned_data

        amount_lent = data['amount_lent']

        return amount_lent

    class Meta:
        model = Prestamos
        fields = ['amount_lent']

