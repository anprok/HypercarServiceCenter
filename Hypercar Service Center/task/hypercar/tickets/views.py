from collections import deque

from django.views import View
from django.shortcuts import render, redirect
from django.http.response import HttpResponse


ticket = 1
next_ticket = 0
line_of_cars = {
    'change_oil': deque(),
    'inflate_tires': deque(),
    'diagnostic': deque(),
}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html')


class TicketView(View):
    def get(self, request, link,  *args, **kwargs):
        global ticket

        if link == 'change_oil':
            time = len(line_of_cars['change_oil']) * 2
        elif link == 'inflate_tires':
            time = len(line_of_cars['change_oil']) * 2 + len(line_of_cars['inflate_tires']) * 5
        else:
            time = len(line_of_cars['change_oil']) * 2 + len(line_of_cars['inflate_tires']) * 5 + len(line_of_cars['diagnostic']) * 30
        line_of_cars[link].append(ticket)

        context = {
            'time': time,
            'ticket': ticket,
        }
        ticket += 1
        return render(request, 'ticket.html', context)


class ProcessingView(View):
    def get(self, request,  *args, **kwargs):
        context = {
            'oil': len(line_of_cars['change_oil']),
            'tires': len(line_of_cars['inflate_tires']),
            'diag': len(line_of_cars['diagnostic'])
        }
        return render(request, 'form.html', context)

    def post(self, request,  *args, **kwargs):
        global next_ticket
        if len(line_of_cars['change_oil']):
            next_ticket = line_of_cars['change_oil'].popleft()
        elif len(line_of_cars['inflate_tires']):
            next_ticket = line_of_cars['inflate_tires'].popleft()
        elif len(line_of_cars['diagnostic']):
            next_ticket = line_of_cars['diagnostic'].popleft()
        else:
            next_ticket = 0

        return redirect('/next')


class NextView(View):
    def get(self, request,  *args, **kwargs):
        global next_ticket
        context = {
            'next': next_ticket
        }
        return render(request, 'next.html', context)