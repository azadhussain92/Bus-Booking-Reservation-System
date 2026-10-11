from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from booking.models import Booking
from tickets.models import Ticket

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
width, height = A4
from reportlab.lib.units import mm
import io

# Create your views here.

@login_required
def ticket_page(request, booking_id):
    bookings = Booking.objects.select_related(
        'schedule__bus',
        'schedule__route'
    ).prefetch_related(
        'passengers__seat'
    )

    if not request.user.is_superuser:
        bookings = bookings.filter(user=request.user)
    booking = get_object_or_404(
        bookings,
        booking_id=booking_id
    )
    # Ticket only for confirmed booking
    if booking.status != 'CONFIRMED':
        return render(request,'ticket/not_conform.html',{'booking': booking})
    # Create ticket if it does not exist
    ticket, created = Ticket.objects.get_or_create(
        booking=booking,
        defaults={
            'ticket_number': 'TKT' + get_random_string(
                10,
                allowed_chars='0123456789'
            )
        }
    )
    return render(request,'ticket/ticket_page.html',{'booking': booking,'ticket': ticket})

@login_required
def download_ticket(request,booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related(
            'schedule__bus',
            'schedule__route'
        ).prefetch_related(
            'passengers__seat'
        ),booking_id=booking_id,
        user=request.user
    )
    #only conformed booking
    if booking.status != 'CONFIRMED':
        return render(request,'ticket/not_conform.html',{'booking':booking})
    #get or create ticket
    ticket,crated = Ticket.objects.get_or_create(
        booking=booking,
        defaults={
            'ticket_number':
            'TKT'+
            get_random_string(
                10,
                allowed_chars='0123456789'
            )
        }
    )
    #if pdf alredy exist, download
    if ticket.pdf_file:
        return FileResponse(
            ticket.pdf_file.open('rb'),
            as_attachment=True,
            filename=f"{ticket.ticket_number}.pdf"
        )
    #create pdf
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer,pagesize=A4)
    #with,hight =a4
    pdf.setFont('Helvetica-Bold',22)
    pdf.drawCentredString(
        width / 2,
        275*mm,
        'REDBUS TICKET'
    )
    # pdf.setFont('Helvetica-Bold',12)
    # pdf.drawString(20 * mm, 255 * mm , f"Ticket Number:{ticket.ticket_number}")
    # pdf.drawString(20 * mm, 245 * mm ,f'Booking ID: {booking.booking_id}')
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(
        20 * mm,
        255 * mm,
        f"Ticket Number: {ticket.ticket_number}"
    )
    pdf.drawString(
        20 * mm,
        245 * mm,
        f"Booking ID: {booking.booking_id}"
    )
    # Bus details
    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(
        20 * mm,
        230 * mm,
        'Bus Details'
    )
    pdf.setFont(
        'Helvetica-Bold',
        11
    )
    pdf.drawString(
    20 * mm,
    215 * mm,
    f"Bus Number: {booking.schedule.bus.bus_number}"
    )
    #journey details
    pdf.setFont(
        'Helvetica-Bold',
        13
    )
    pdf.drawString(
        20 *mm,
        185 * mm,
        'Journey details'
    )
    pdf.setFont(
        'Helvetica-Bold',
        13
    )
    pdf.drawString(
        20 *mm,
        175 * mm,
        f"From :{ booking.schedule.route.source}"
    )
    pdf.drawString(
        20 *mm,
        165*mm,
        f"To:{booking.schedule.route.destination}"
    )
    pdf.drawString(
        20 * mm,
        155 * mm,
        f"Date:{booking.schedule.journey_date}"
    )
    pdf.drawString(
        20 * mm,
        145 * mm,
        f"Departure:{booking.schedule.departure_time}"
    )
    pdf.drawString(
        20 * mm,
        135 *mm,
        f"Arrival: {booking.schedule.arrival_time}"
    )
   # passenger details
    pdf.setFont(
        'Helvetica-Bold',
        13
    )
    pdf.drawString(
        20 * mm,
        115 * mm,
        'Passenger Details'
    )
    y = 103 * mm
    pdf.setFont(
        'Helvetica',
        10
    )
    for passenger in booking.passengers.all():
        pdf.drawString(
            20 * mm,
            y,
            f'Seat: {passenger.seat.seat_number}'
        )
        pdf.drawString(
            50 * mm,
            y,
            f'Name: {passenger.name}'
        )
        pdf.drawString(
            115 * mm,
            y,
            f'Age: {passenger.age}'
        )
        y -= 8 * mm
        pdf.drawString(
            20 * mm,
            y,
            f'Gender: {passenger.get_gender_display()}'
        )
        pdf.drawString(
            65 * mm,
            y,
            f'Phone: {passenger.phone}'
        )
        y -= 12 * mm
    # Payment Details
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(
        20 * mm,
        y - 5 * mm,
        f'Total Amount: Rs. {booking.total_amount}'
    )
    pdf.drawString(
        20 * mm,
        y - 17 * mm,
        'Payment Status: CONFIRMED'
    )
    # Footer
    pdf.setFont('Helvetica', 9)
    pdf.drawString(
        20 * mm,
        20 * mm,
        'Thank you for booking with RedBus Clone.'
    )
    pdf.save()
    # Move buffer position to beginning
    buffer.seek(0)
    # Save PDF into database
    ticket.pdf_file.save(
        f'{ticket.ticket_number}.pdf',
        ContentFile(
            buffer.getvalue()
        ),
        save=True
    )
    # Download PDF
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f'{ticket.ticket_number}.pdf'
    )