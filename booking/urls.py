from django.urls import path
# from booking import views
from booking.views import (HomePageView, BookingListView,
                           OrderView, SucessView, RegisterView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    # path('register', BookingListView.as_view(), name='register'),
    path('booking', BookingListView.as_view(), name='booking'),
    path('booking/<slug:slug>/', OrderView.as_view(), name='orderview'),
    path('success', SucessView.as_view(), name='success'),
]
