from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from accounts.models import Account
from accounts.forms import RegisterForm ,LoginForm
from buses.models import Buses
from booking.models import Booking
from payments.models import Payment

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Account.objects.create(
                user=user,
                phone = form.cleaned_data['phone'],
                role = form.cleaned_data['role'],
                profile_image= form.cleaned_data.get('profile_image')
            )
            login(request,user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request,'accounts/register.html',{'form':form})

#user login 
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            form.add_error(None,'invalid user or password')
    else:
        form = LoginForm()
    return render(request,'accounts/login.html',{'form':form})

#logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return admin_dashboard(request)

    account = request.user.account

    if account.role == 'ADMIN':
        return admin_dashboard(request)

    elif account.role == 'BUS_OPERATOR':
        return operator_dashboard(request)

    else:
        return render(request, 'accounts/customer_dasboard.html')


def admin_dashboard(request):
    total_users = User.objects.count()
    total_buses = Buses.objects.count()
    total_bookings = Booking.objects.count()

    total_payments = Payment.objects.filter(
        status='SUCCESS'
    ).count()

     # Revenue excludes cancelled bookings
    total_revenue = Payment.objects.filter(
        status='SUCCESS',
        booking__status='CONFIRMED'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    recent_bookings = Booking.objects.order_by('-id')[:10]
    total_cancelled = Booking.objects.filter(
    status='CANCELLED').count()
    recent_cancelled = Booking.objects.filter(
        status='CANCELLED').select_related(
        'user', 'schedule__bus').order_by('-booked_at')[:10]

    context = {
        'total_users': total_users,
        'total_buses': total_buses,
        'total_bookings': total_bookings,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'total_cancelled': total_cancelled,
        'recent_cancelled': recent_cancelled,

    }

    return render(request, 'accounts/admin_dashboard.html', context)



@login_required
def operator_dashboard(request):
    operator_buses = Buses.objects.filter(operator=request.user)

    operator_bookings = Booking.objects.filter(
        schedule__bus__operator=request.user
    ).select_related(
        'user', 'schedule__bus'
    ).order_by('-id')

    total_buses = operator_buses.count()
    total_bookings = operator_bookings.count()

    total_payments = Payment.objects.filter(
        booking__in=operator_bookings,
        status='SUCCESS'
    ).count()

    total_revenue = Payment.objects.filter(
        booking__in=operator_bookings,
        status='SUCCESS',
        booking__status='CONFIRMED'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_cancelled = operator_bookings.filter(
    status='CANCELLED').count()
    recent_cancelled = Booking.objects.filter(
    status='CANCELLED').select_related(
    'user', 'schedule__bus').order_by('-booked_at')[:10]
    context = {
        'total_buses': total_buses,
        'total_bookings': total_bookings,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'recent_bookings': operator_bookings[:10],
        'total_cancelled': total_cancelled,
        'recent_cancelled': recent_cancelled,
    }

    return render(
        request,
        'accounts/operator_dashboard.html',
        context
    )
