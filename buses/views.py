from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from buses.models import Buses ,BusRoute,BusSchedule,BusSeat
from buses.forms import BussForm,BusRouteForm,BusScheduleForm,BusSeatForm
import string
from booking.models import Passenger
from django.db import models

# Create your views here.

def home(request):
    return render(request,'home.html')
#bus list 
@login_required
def bus_list(request):

    if request.user.is_superuser:
        buses = Buses.objects.all()
    elif request.user.account.role == 'ADMIN':
        buses = Buses.objects.all()
    else:
        buses = Buses.objects.filter(operator=request.user)
    return render(request, 'buses/bus_list.html', {'buses': buses})

@login_required
def bus_add(request):
    if request.method == 'POST':
        form = BussForm(request.POST)

        if form.is_valid():
            bus = form.save(commit=False)
            bus.operator = request.user
            bus.save()

            # Automatically create seats
            bus_count = Buses.objects.count()
            prefix = string.ascii_uppercase[bus_count - 1]

            for i in range(1, bus.total_seats + 1):
                BusSeat.objects.create(
                bus=bus,
                seat_number=f'{prefix}{i}',
                seat_type='SEATER',
                price=bus.fare,
                is_active=True
            )

            messages.success(request, 'Bus added Successfully')
            return redirect('bus_list')
        else:
            print(form.errors)
    else:
        form = BussForm()
    return render(request,'buses/bus_form.html',{'form': form, 'title': 'Add Bus'})

#update buss
@login_required
def bus_update(request,id):
    if request.user.is_superuser or request.user.account.role == "ADMIN":
        bus = get_object_or_404(Buses, id=id)
    else:
        bus = get_object_or_404(Buses,id=id,operator=request.user)
    if request.method == 'POST':
        form = BussForm(request.POST,instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request,'Bus update seccessfully..')
            return redirect('bus_list')
    else:
        form = BussForm(instance=bus)
    return render(request,'buses/bus_form.html',{'form': form,'title':'update bus'})

#bus delete 
@login_required
def bus_delete(request,id):
    if request.user.is_superuser or request.user.account.role == "ADMIN":
        bus = get_object_or_404(Buses, id=id)
    else:
        bus = get_object_or_404(Buses,id=id,operator=request.user)
    if request.method == 'POST':
        bus.delete()
        messages.success(request,'Bues delete succssfully')
        return redirect('bus_list')
    return render(request,'buses/bus_delete.html',{'bus':bus})


#route management
@login_required
def route_list(request):
    routes = BusRoute.objects.all()
    return render(request,'buses/route_list.html',{'routes':routes})

#route add
@login_required
def route_add(request):
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'route added successfully')
            return redirect('route_list')
    else:
        form = BusRouteForm()
    return render(request,'buses/route_form.html',{'form':form,'title':'add route'})

#route update
@login_required
def route_update(request,id):
    route = get_object_or_404(BusRoute,id=id)
    if request.method == 'POST':
        form = BusRouteForm(request.POST,instance=route)
        if form.is_valid():
            form.save()
            messages.success(request,'route update successfully..')
    else:
        form = BusRouteForm(instance=route)
    return render(request,'buses/route_form.html',{'form':form,'title':'update route'})

#route delete
@login_required
def route_delete(request,id):
    route = get_object_or_404(BusRoute,id=id)
    if request.method == 'POST':
        route.delete()
        messages.success(request,'route delete successfully..')
        return redirect('route_list')
    return render(request,'buses/route_delete.html',{'route':route})

#schedule management
@login_required
def sechedule_list(request):

    if request.user.is_superuser:
        schedules = BusSchedule.objects.all()
    elif request.user.account.role == 'ADMIN':
        schedules = BusSchedule.objects.all()
    else:
        schedules = BusSchedule.objects.filter(bus__operator=request.user)
    schedules = schedules.select_related('bus', 'route')
    return render(request, 'buses/schedule_list.html', {'schedules': schedules})

#add schedule
@login_required
def schedule_add(request):
    if request.method =='POST':
        form = BusScheduleForm(request.POST)
        if form.is_valid():
            schedule= form.save(commit=False)
            if schedule.bus.operator !=request.user:
                messages.error(request,'You can create schedule for your own buses..')
            else:
                schedule.save()
                messages.success(request,'schedule add successfully..')
                return redirect('schedule_list')
    else:
        form = BusScheduleForm()
        form.fields['bus'].queryset = Buses.objects.filter(operator = request.user)
    return render(request,'buses/schedule_form.html',{'form':form,'title':'add schedule'})

#seat management
@login_required
def seat_list(request):

    if request.user.is_superuser:
        seats = BusSeat.objects.all()
    elif request.user.account.role == 'ADMIN':
        seats = BusSeat.objects.all()
    else:
        seats = BusSeat.objects.filter(bus__operator=request.user)
    seats = seats.select_related('bus').order_by('bus_id', 'id')

    # Confirmed bookings ki seats
    booked_seat_ids = set(
        Passenger.objects.filter(booking__status='CONFIRMED').values_list('seat_id', flat=True))
    return render(request, 'buses/seat_list.html', {'seats': seats,'booked_seat_ids': booked_seat_ids,})


@login_required
def seat_add(request):
    if request.method == 'POST':
        form = BusSeatForm(request.POST)
        if form.is_valid():
            seat = form.save(commit=False)
            if seat.bus.operator != request.user:
                messages.error(request,'You can add seat to ypur own buses..')
            else:
                seat.save()
                messages.success(request,'seat add successfully..')
                return redirect('seat_list')
    else:
        form = BusSeatForm()
        form.fields['bus'].queryset = Buses.objects.filter(operator=request.user)
        return render(request,'buses/seat_form.html',{'form':form,'title':'add seat'})

#bus search
@login_required
def search_buses(request):

    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()
    journey_date = request.GET.get('journey_date', '')
    schedules = BusSchedule.objects.select_related('bus','route').filter(
        route__source__iexact=source,
        route__destination__iexact=destination,
        bus__is_active=True
    )

    # Specific date OR Daily bus
    if journey_date:
        schedules = schedules.filter(
            models.Q(journey_date=journey_date) |
            models.Q(is_daily=True)
        )

    return render(request,'buses/search_results.html',{
            'schedules': schedules,
            'source': source,
            'destination': destination,
            'journey_date': journey_date,
        }
    )