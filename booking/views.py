from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from booking.models import *


class HomePageView(TemplateView):

    template_name = "booking/base.html"
    model = BusService

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values = BusService.objects.values_list('source', 'destination')
        chain_dict = {} 
        for key, value in values:
            if key not in chain_dict.keys(): 
                chain_dict[key] = [value] 
            else: 
                chain_dict[key].append(value)
        context['chain_dict'] = chain_dict
        return context

class BookingListView(ListView):
    model = BusTiming
    template_name = "booking/bookinglist.html"

    def get_queryset(self, *args, **kwargs): 
        qs = super(BookingListView, self).get_queryset(*args, **kwargs) 
        qs = qs.order_by("-id") 
        return qs 