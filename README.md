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
- SQLite / MySQL

## Project Structure

```text
Bus-Booking-System/
│
├── accounts/
├── buses/
├── booking/
├── payment/
├── ticket/
├── templates/
├── static/
├── media/
├── manage.py
└── README.md
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/azadhussain92/Django-Bus-Booking-System.git
```

**2. Open the project folder**

```bash
cd Django-Bus-Booking-System
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment (Windows)**

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Apply migrations**

```bash
python manage.py migrate
```

**7. Create an admin account**

```bash
python manage.py createsuperuser
```

**8. Run the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

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

## Author

**Azad Hussain**

GitHub: [@azadhussain92](https://github.com/azadhussain92)

---

*This project was developed for learning and demonstrating full-stack web development with Django.*
