from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from booking.models import *
from booking.forms import QueryForm


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

    # def get(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         return redirect("/booking")
    #     else:
    #         return super(HomePageView, self).dispatch(request, *args, **kwargs)
# def redirect(self, *args, **kwargs):
#     if request.GET.get('action') == 'query':
#         import ipdb; ipdb.set_trace()

# def queryform(request):
#     if request.method == 'GET':
#         import ipdb; ipdb.set_trace()
#         return redirect('1/booking')

        # import ipdb; ipdb.set_trace()
        # return HttpResponse('Hello')
        # if request.method == 'GET':
        # else:
    # def dispatch(self, *args, **kwargs):
    #     return super(HomePageView, self).dispatch(*args, **kwargs)



# class GeeksFormView(FormView): 
#     # specify the Form you want to use 
#     # sepcify name of template 
#     template_name = "booking/base.html"
  
#     # can specify success url 
#     # url to redirect after sucessfully 
#     # updating details 

class BookingListView(ListView):

    model = BusTiming
    template_name = "booking/bookinglist.html"

    # def get_ajax(self, *args, **kwargs):

    # def get_queryset(self, *args, **kwargs):
    #     qs = super(BookingListView, self).get_queryset(*args, **kwargs) 
    #     qs = qs.order_by("-id") 
    #     return qs
    # def render_to_response(self, context):
    #     return redirect(template_name)

        # if not self.videos:

            # return super(VideosView, self).render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = 'hello'
        if request.GET.get('action') == 'query':
            return render(request, self.template_name, {'context': context})
        else:
            return render(request, self.template_name, {'context': context})
