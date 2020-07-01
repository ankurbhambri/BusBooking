from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
# from django.views.generic.edit import FormView
from booking.models import *
# from booking.forms import QueryForm


class HomePageView(TemplateView):

    template_name = "booking/index.html"
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

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = dict()
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        passenger = request.POST.get('passenger')
        date = request.POST.get('date')
        context['date'] = date
        query = BusTiming.objects.filter(
            service__source=choice1, service__destination=choice2,
            service__passanger_capacity__gte=passenger)
        context['query'] = query
        return render(request, self.template_name, {"context": context})

    # def get_ajax_context_data(self, request):

    # def get(self, request, *args, **kwargs):
    #     context = 'Hello'
    #     if request.GET.get('action') == 'query':
    #         return render(request, self.template_name, {'context': context})
    #     else:
    #         return render(request, self.template_name, {'context': context})


# clas
