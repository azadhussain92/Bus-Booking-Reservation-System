from django import forms
from buses.models import Buses,BusSeat,BusRoute,BusSchedule

#busform
class BussForm(forms.ModelForm):
    class Meta:
        model = Buses
        fields = [
            'bus_number',
            'bus_name',
            'bus_type',
            'total_seats',
            'fare',
            'is_active'
        ]
        widgets = {
            'bus_number':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter bus number'
            }),
            'bus_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter bus name'
            }),
            'bus_type':forms.Select(attrs={
                'class':'form-control'
            }),
            'total_seats':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter total seats'
            }),
            'fare':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter bus fare',
                'step': '0.01'
            }),
            'is_active':forms.CheckboxInput(attrs={
                'class':'form-check-input'
            })
        }

#bus route
class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = [
            'source',
            'destination',
            'distance',
            'duration'
        ]
        widgets = {
            'source':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter sourse'
            }),
            'destination':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter destination'
            }),
            'distance':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter distance'
            }),
            'duration':forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

#bus schedule 
class BusScheduleForm(forms.ModelForm):
    class Meta:
        model = BusSchedule
        fields = [
            'bus',
            'route',
            'journey_date',
            'departure_time',
            'arrival_time',
            'boarding_point',
            'dropping_point',
            'is_daily'
        ]
        widgets = {
            'bus':forms.Select(attrs={
                'class': 'form-control'
            }),
            'route':forms.Select(attrs={
                'class': 'form-control'
            }),
            'journey_date':forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'departure_time':forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'arrival_time':forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'boarding_point':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter boarding point'
            }),
            'dropping_point': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter dropping point'
            }),
            'is_daily': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

#bus seats
class BusSeatForm(forms.ModelForm):
    class Meta:
        model = BusSeat
        fields = [
            'bus',
            'seat_number',
            'seat_type',
            'price',
            'is_active'
        ]
        widgets = {
            'bus':forms.Select(attrs={
                'class': 'form-control'
            }),
            'seat_number':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Example: A1'
            }),
            'seat_type':forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter seat price',
                'seat': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': ' form-check-input'
            })
        }