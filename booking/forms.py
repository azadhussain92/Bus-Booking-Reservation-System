from django import forms 
from booking.models import Passenger

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'name',
            'age',
            'gender',
            'phone',
        ]
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Passenger Name'
            }),
            'age':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Age',
                'min': '1',
                'max':'120'
            }),
            'gender':forms.Select(attrs={
                'class':'form-control'
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Phone Number'
            }),
        }

        