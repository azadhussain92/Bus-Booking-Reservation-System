from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.utils import timezone
from booking.models import Booking
from payments.models import Payment 
from payments.forms import PaymentForm


# Create your views here.
@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related(
            'schedule__bus',
            'schedule__route',
        ),
        booking_id=booking_id,
        user=request.user
    )

    # Check already paid
    try:
        payment = booking.payments
        if payment.status == 'SUCCESS':
            messages.info(request, 'This booking is already paid.')
            return redirect('booking_detail', id=booking.id)
    except Payment.DoesNotExist:
        pass
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            transaction_id = (
                'TXN' + get_random_string(
                    12,
                    allowed_chars='0123456789'
                )
            )
            # Create Payment
            Payment.objects.create(
                booking=booking,
                transaction_id=transaction_id,
                amount=booking.total_amount,
                payment_method=payment_method,
                status='SUCCESS',
                paid_at=timezone.now(),
            )
            # Confirm booking
            booking.status = 'CONFIRMED'
            booking.save()
            messages.success(request,'Payment successful! Your booking is confirmed.')
            return redirect('booking_detail',id=booking.id)
    else:
        form = PaymentForm()

    return render(request,'payment/payment_page.html',{'booking': booking,'form': form})

@login_required
def payment_list(request):
    if request.user.is_superuser:
        payments = Payment.objects.select_related(
            'booking',
            'booking__user',
            'booking__schedule__bus',
            'booking__schedule__route'
        ).order_by('-id')

    elif hasattr(request.user, 'account') and request.user.account.role == 'BUS_OPERATOR':
        payments = Payment.objects.filter(
            booking__schedule__bus__operator=request.user
        ).select_related(
            'booking',
            'booking__user',
            'booking__schedule__bus',
            'booking__schedule__route'
        ).order_by('-id')

    else:
        payments = Payment.objects.filter(
            booking__user=request.user
        ).select_related(
            'booking'
        ).order_by('-id')

    return render(request, 'payment/payment_list.html', {'payments': payments})