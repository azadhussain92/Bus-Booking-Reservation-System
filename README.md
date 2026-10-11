# Django Bus Booking System

A full-stack Bus Booking Web Application developed using Python and Django, inspired by online bus reservation platforms like RedBus.

## Features

- **User Authentication:** Registration, Login and Logout
- **Admin Dashboard:** Manage users, buses, bookings, payments and revenue
- **Bus Operator Dashboard:** Manage bus-related bookings and view cancellation details
- **Customer Dashboard:** View bookings and cancelled booking history
- **Bus Management:** Manage buses, routes, schedules and seat details
- **Bus Search:** Search buses by source, destination and journey date
- **Seat Selection:** View and select available seats
- **Booking Management:** Book tickets and view booking status
- **Payment System:** Payment processing with success and failure status
- **Ticket Management:** View booking and ticket details
- **Booking Cancellation:** Cancel eligible bookings and track cancellation status
- **Revenue Tracking:** View successful payments and confirmed-booking revenue

## Technologies Used

- Python
- Django
- Django ORM
- HTML5
- CSS3
- JavaScript
- Bootstrap
-  MySQL

## Project Structure

```text
LOGIN / REGISTER
       |
       v
   DASHBOARD
       |
       v
 BUS BOOKING SYSTEM
       |
       +------------------------+
       |                        |
       v                        v
     BUSES                   ACCOUNTS
       |                        |
       ├── Bus Details          ├── Customer
       ├── Bus Routes           ├── Bus Operator
       ├── Bus Schedules        └── Admin
       └── Seat Details
              |
              v
        SEARCH BUSES
              |
              v
        SELECT SEATS
              |
              v
      PASSENGER DETAILS
              |
              v
           BOOKING
              |
              ├── Booking ID
              ├── Booking Status
              └── Cancellation
              |
              v
           PAYMENT
              |
              ├── Payment Success
              ├── Payment Failed
              └── Payment Status
              |
              v
            TICKET
              |
              ├── Ticket Details
              └── Download Ticket

DASHBOARDS
    |
    ├── Admin Dashboard
    │     ├── Total Users
    │     ├── Total Buses
    │     ├── Total Bookings
    │     ├── Cancelled Bookings
    │     ├── Total Payments
    │     └── Total Revenue
    |
    ├── Bus Operator Dashboard
    │     ├── My Buses
    │     ├── Total Bookings
    │     ├── Cancelled Bookings
    │     └── Revenue
    |
    └── Customer Dashboard
          ├── Search Buses
          ├── My Bookings
          ├── Cancelled Bookings
          └── My Tickets
```

## Installation and Setup


**1. Open the project folder**

```bash
cd Django-Bus-Booking-System
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the virtual environment (Windows)**

```bash
venv\Scripts\activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create an admin account**

```bash
python manage.py createsuperuser
```

**7. Run the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.
### 🗄️ Database Setup

This project uses MySQL as its database.

1. Install MySQL Server.
2. Create a database in MySQL.
3. Update the database credentials in `settings.py`.
4. Run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Note:** The database itself is not included in this repository. Tables are created using Django migrations.

## User Roles

| Role | Responsibilities |
|---|---|
| Admin | Manage the system and monitor bookings, payments and revenue |
| Bus Operator | View bookings and cancellations for their buses |
| Customer | Search buses, book seats, manage tickets and cancel eligible bookings |

## Booking Workflow

```text
Register / Login
       ↓
Search Buses
       ↓
Select Bus and Seats
       ↓
Enter Passenger Details
       ↓
Complete Payment
       ↓
Booking Confirmation
       ↓
View / Download Ticket
       ↓
Cancel Booking (if eligible)
```

## Important Notes

- Configure database settings in `settings.py` before running the project.
- Install the dependencies listed in `requirements.txt`.
- Payment functionality may use demo payments unless a real payment gateway has been integrated.
- Do not upload passwords, secret keys, database credentials or the virtual environment to GitHub.

## Future Enhancements

- Payment gateway integration
- Email and SMS booking notifications
- PDF ticket generation
- Advanced booking reports and analytics
