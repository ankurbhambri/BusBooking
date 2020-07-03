from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from booking.models import BusService, BusTiming, Query, CustomerLogin


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
        query_dict = dict()
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        passenger = request.POST.get('passenger')
        date = request.POST.get('date')

        one_side_query = BusTiming.objects.filter(
            service__source=choice1, service__destination=choice2,
            service__passanger_capacity__gte=passenger)

        query_dict['one_side'] = {
            'source': choice1,
            'destination': choice2,
            'passenger': int(passenger),
            'journey_date': date,
            'departure_location': one_side_query[0].service.souce_bus_stand_location,
            'arival_location': one_side_query[0].service.destination_bus_stand_location,
            'departure_time': one_side_query[0].departure_time.strftime("%m/%d/%Y"),
            'desstination_time': one_side_query[0].desstination_time.strftime("%m/%d/%Y"),
            'total_price': int(passenger) * int(one_side_query[0].service.per_passanger_price)}

        return_query = BusTiming.objects.filter(
            service__source=choice2, service__destination=choice1,
            service__passanger_capacity__gte=passenger)

        if return_query:
            query_dict['return_query'] = {
                'source': choice2,
                'destination': choice1,
                'passenger': int(passenger),
                'journey_date': date,
                'departure_location': return_query[0].service.souce_bus_stand_location,
                'arival_location': return_query[0].service.destination_bus_stand_location,
                'departure_time': return_query[0].departure_time.strftime("%m/%d/%Y"),
                'desstination_time': return_query[0].desstination_time.strftime("%m/%d/%Y"),
                'total_price': int(passenger) * int(return_query[0].service.per_passanger_price)}

        query_dict['amt'] = int(passenger) * int(one_side_query[0].service.per_passanger_price) + \
            int(passenger) * int(return_query[0].service.per_passanger_price)

        query_id = Query.objects.create(attrs=query_dict)
        context['one_side_query'] = one_side_query
        context['return_query'] = return_query
        context['query_id'] = query_id.id
        return render(request, self.template_name, {"context": context})


class OrderView(DetailView):
    model = Query
    template_name = 'booking/checkout_page.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = dict()
        query_response = Query.objects.filter(id=int(request.POST['query_id']))
        context = query_response[0].attrs
        return render(request, self.template_name, {'context': context})


class SucessView(ListView):
    # model = Query
    template_name = 'booking/success_page.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class RegisterView(ListView):

    model = CustomerLogin
    template_name = 'booking/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     return redirect(reverse('login'))

        return render(request, self.template_name, {})
