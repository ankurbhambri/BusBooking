import re
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from booking.models import BusService, BusTiming, Query
from orders.models import OrderTable


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
        context['login_user'] = self.request.user.username
        return context


class BookingListView(ListView):

    model = BusTiming
    template_name = "booking/bookinglist.html"

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        response_data = dict()
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
        response_data['one_side_query'] = one_side_query
        response_data['return_query'] = return_query
        response_data['query_id'] = query_id.id
        response_data['login_user'] = self.request.user.username
        return render(request, self.template_name, {"response_data": response_data})


class CheckoutView(DetailView):
    model = Query
    template_name = 'booking/checkout_page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckoutView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = dict()
        path = self.request.get_full_path()
        query_id = re.findall('\d+', path)
        query_response = Query.objects.filter(id=int(query_id[0]))
        context = query_response[0].attrs
        context['login_user'] = self.request.user.username
        return render(request, self.template_name, {'context': context})

    def post(self, request, *args, **kwargs):
        context = dict()
        query_response = Query.objects.filter(id=int(request.POST['query_id']))
        context = query_response[0].attrs
        context['query_id'] = query_response[0].id
        context['login_user'] = self.request.user.username
        return render(request, self.template_name, {'context': context})


class SucessView(ListView):
    model = OrderTable
    template_name = 'booking/success_page.html'

    def get_context_data(self, **kwargs):
        context = super(SucessView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        query_id = int(request.POST['query_id'])
        query_obj = Query.objects.filter(id=query_id)
        order = OrderTable.objects.create(user=self.request.user,
                                          query=query_obj[0])
        return render(request, self.template_name, {"order": order})
