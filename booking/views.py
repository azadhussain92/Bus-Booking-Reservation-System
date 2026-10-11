from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.utils.crypto import get_random_string
from buses.models import BusSchedule,BusSeat
from booking.models import Booking,Passenger
from booking.forms import PassengerForm

# Create your views here.
@login_required
def select_seats(request,id):
    schedule = get_object_or_404(
        BusSchedule.objects.select_related('bus','route'),id=id)
    seats = BusSeat.objects.filter(bus=schedule.bus,is_active=True).order_by('id')

    #seat already booked for this particular journey
    booked_seat_ids = Passenger.objects.filter(
        booking__schedule = schedule,
        booking__status__in = ['PENDING','CONFIRMED']
    ).values_list('seat_id',flat=True)

    if request.method == 'POST':
        select_seats = request.POST.getlist('seats')
        if not select_seats:
            messages.error(request,'Please Select at Last One Seat..')
            return redirect('seat_select', id=id)
        select_seat_object= BusSeat.objects.filter(
            id__in = select_seats,
            bus = schedule.bus,
            is_active = True
        )

        #check whether the selected seat are alredy booked
        already_booked = select_seat_object.filter(id__in=booked_seat_ids).exists()
        if already_booked:
            messages.error(request,'One or More selected seats are already booked')
            return redirect('seat_select', id=id)
        request.session['selected_seats'] = select_seats
        request.session['schedule_id'] = schedule.id
        return redirect('passenger_detail')
    return render(request,'booking/select_seat.html',{'schedule':schedule,'seats':seats,'booked_seat_ids': list(booked_seat_ids)})


#passenger details
@login_required
def passenger_details(request):
    schedule_id = request.session.get('schedule_id')
    selected_seats = request.session.get('selected_seats')

    if not schedule_id or not selected_seats:
        messages.error(request, 'Please select your seat first.')
        return redirect('home')

    schedule = get_object_or_404(BusSchedule.objects.select_related('bus', 'route'),id=schedule_id)
    seats = BusSeat.objects.filter(id__in=selected_seats,bus=schedule.bus,is_active=True).order_by('id')
    passenger_forms = []

    for seat in seats:
        prefix = f"seat_{seat.id}"
        form = PassengerForm(request.POST or None,prefix=prefix)
        passenger_forms.append((seat, form))

    if request.method == 'POST':
        all_valid = all(form.is_valid()for seat, form in passenger_forms)
        print("ALL VALID:", all_valid)

        for seat, form in passenger_forms:
            print(seat.seat_number, form.errors)
        if all_valid:
            with transaction.atomic():
                booked_now = Passenger.objects.filter(
                    booking__schedule=schedule,
                    booking__status__in=['PENDING', 'CONFIRMED'],
                    seat__id__in=selected_seats
                ).exists()

                if booked_now:
                    messages.error(request,'One or more seats were just booked.')
                    return redirect('seat_select',id=schedule.id)

                total_amount = sum(
                    seat.price
                    for seat, form in passenger_forms
                )
                booking_id = (
                    'RB' +
                    get_random_string(
                        10,
                        allowed_chars='0123456789'
                    )
                )
                booking = Booking.objects.create(
                    user=request.user,
                    schedule=schedule,
                    booking_id=booking_id,
                    total_amount=total_amount,
                    status='PENDING'
                )

                for seat, form in passenger_forms:
                    Passenger.objects.create(
                        booking=booking,
                        seat=seat,
                        name=form.cleaned_data['name'],
                        age=form.cleaned_data['age'],
                        gender=form.cleaned_data['gender'],
                        phone=form.cleaned_data['phone']
                    )

            request.session.pop('selected_seats', None)
            request.session.pop('schedule_id', None)
            messages.success(request,'Booking created successfully!')
            return redirect('booking_detail',id=booking.id)

    return render(request,'booking/passenger_detail.html',{'schedule': schedule,'seats': seats,'passenger_forms': passenger_forms})

@login_required
def booking_detail(request, id):

    if request.user.is_superuser:
        booking = get_object_or_404(Booking, id=id)
    else:
        booking = get_object_or_404(Booking,id=id,user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
def my_booking(request):

    bookings = Booking.objects.filter(user=request.user).select_related(
        'schedule__bus',
        'schedule__route'
    ).order_by('-booked_at')
    return render(request, 'booking/my_booking.html', {'bookings': bookings})

@login_required
def booking_list(request):
    if request.user.is_superuser:
        bookings = Booking.objects.select_related(
            'user',
            'schedule__bus',
            'schedule__route'
        ).order_by('-booked_at')

    elif hasattr(request.user, 'account') and request.user.account.role == 'BUS_OPERATOR':
        bookings = Booking.objects.filter(
            schedule__bus__operator=request.user
        ).select_related(
            'user',
            'schedule__bus',
            'schedule__route'
        ).order_by('-booked_at')

    else:
        bookings = Booking.objects.filter(
            user=request.user
        ).select_related(
            'schedule__bus',
            'schedule__route'
        ).order_by('-booked_at')

    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def passenger_list(request):

    if request.user.is_superuser:
        passengers = Passenger.objects.select_related(
            'booking',
            'booking__user',
            'booking__schedule__bus',
            'booking__schedule__route',
            'seat'
        ).order_by('-booking__booked_at')

    elif hasattr(request.user, 'account') and request.user.account.role == 'BUS_OPERATOR':
        passengers = Passenger.objects.filter(
            booking__schedule__bus__operator=request.user
        ).select_related(
            'booking',
            'booking__user',
            'booking__schedule__bus',
            'booking__schedule__route',
            'seat'
        ).order_by('-booking__booked_at')

    else:
        passengers = Passenger.objects.filter(
            booking__user=request.user
        ).select_related(
            'booking',
            'seat'
        ).order_by('-booking__booked_at')

    return render(request, 'booking/passenger_list.html', {'passengers': passengers})

#ticket cancelletion function
# @login_required
# @require_POST
# def cancel_booking(request,booking_id):
#     with transaction.atomic():
#         booking = get_object_or_404(Booking,booking_id=booking_id,user=request.user)
#         if booking.status == 'CANCELLED':
#             messages.warning(request,'This ticket is cancelled..')
#         elif booking.status == 'CONFIRMED':
#             booking.status = 'CANCELLED'
#             booking.save(update_fields=['status'])
#             messages.success(request,'Your ticket has been cancelled..')
#         else:
#             messages.warning(request,'Only confirmed booking can be cancelled..')
#     return redirect('my_booking')

@login_required
@require_POST
def cancel_booking(request, booking_id):
    with transaction.atomic():
        booking = get_object_or_404(
            Booking.objects.select_related(
                'user', 'schedule__bus__operator'
            ),
            booking_id=booking_id
        )

        # Admin permission
        is_admin = (
            request.user.is_superuser
            or (
                hasattr(request.user, 'account')
                and request.user.account.role == 'ADMIN'
            )
        )

        # Customer: only their own booking
        is_customer = booking.user_id == request.user.id

        # Bus Operator: only bookings for their own buses
        is_operator = (
            hasattr(request.user, 'account')
            and request.user.account.role == 'BUS_OPERATOR'
            and booking.schedule.bus.operator_id == request.user.id
        )

        if not (is_admin or is_customer or is_operator):
            messages.error(
                request,
                'You do not have permission to cancel this ticket.'
            )
            return redirect('my_booking')

        if booking.status == 'CANCELLED':
            messages.warning(request, 'This ticket is already cancelled.')

        elif booking.status == 'CONFIRMED':
            booking.status = 'CANCELLED'
            booking.save(update_fields=['status'])
            messages.success(request, 'Your ticket has been cancelled.')

        else:
            messages.warning(
                request,
                'Only confirmed bookings can be cancelled.'
            )

    return redirect('my_booking')
