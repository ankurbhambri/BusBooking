from django.urls import path
# from booking import views
from booking.views import HomePageView, BookingListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('booking', BookingListView.as_view(), name='booking'),
]
