from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Ticket, Booking
from django.contrib import messages

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'event_detail.html', {'event': event, 'tickets': tickets})


def book_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > ticket.event.available_tickets:
            messages.error(request, 'Not enough tickets available')
        else:
            booking = Booking.objects.create(user=request.user, ticket=ticket, quantity=quantity)
            ticket.event.available_tickets -= quantity
            ticket.event.save()
            messages.success(request, 'Booking successful')
            return redirect('app:my_bookings')
    return render(request, 'book_ticket.html', {'ticket': ticket})


def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

# Create your views here.
