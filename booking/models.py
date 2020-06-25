from django.db import models
from django.contrib.postgres.fields import HStoreField
# Create your models here.

class CustomerLogin(models.Model):

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    customer_email = models.EmailField(max_length=150, null=False, blank=False, unique=True)
    phone_number = models.IntegerField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=150, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    pincode = models.IntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_email


class VehicalDetail(models.Model):

    vehicle_name = models.CharField(max_length=150, null=False, blank=False)
    vehicle_registration_number = models.IntegerField(null=False, blank=False)
    engine_number = models.IntegerField(null=False, blank=False)
    mfg_date = models.DateField(null=False, blank=False)
    number_of_seats = models.CharField(max_length=20, null=False, blank=False)
    fuel_capacity = models.IntegerField(null=False, blank=False)
    owner_name = models.CharField(max_length=150, null=False, blank=False)
    ac = models.BooleanField()
    non_ac = models.BooleanField()

    def __str__(self):
        return self.vehicle_name


class DriverDetail(models.Model):

    driver_name = models.CharField(max_length=150, null=False, blank=False)
    driver_email = models.EmailField(max_length=150, null=False, blank=False)
    driver_phone_no = models.IntegerField()
    driver_adress = models.CharField(max_length=150, null=False, blank=False)
    driver_licence = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.driver_email


class BusService(models.Model):

    vehicle = models.ForeignKey(VehicalDetail, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, null=False, blank=False)
    destination = models.CharField(max_length=150, null=False, blank=False)
    souce_bus_stand_location = models.CharField(max_length=150, null=False, blank=False)
    destination_bus_stand_location = models.CharField(max_length=150, null=False, blank=False)
    passanger_capacity = models.CharField(max_length=150, null=False, blank=False)
    per_passanger_price = models.CharField(max_length=50, null=False, blank=False)
    driver_email = models.ForeignKey(DriverDetail, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class BusTiming(models.Model):

    service = models.ForeignKey(BusService, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    desstination_time = models.TimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Query(models.Model):

    attrs = HStoreField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
