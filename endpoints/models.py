from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Dealer(models.Model):
    
    dealerId = models.CharField(primary_key = True, max_length=120)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=80, null = True, blank=True)
    point = models.PointField(null=True, spatial_index=True, geography=True)

    def fill(dealer_dic):
        
        try:
            Dealer.objects.get(dealerId = dealer_dic['id'])
        except:
            try:
                d =  Dealer(
                            dealerId=dealer_dic['id'],
                            name=dealer_dic['name'],
                            email=dealer_dic['email'],
                            point=Point(float(dealer_dic['lon']),float(dealer_dic['lat']))
                            )
                d.save()
                return (d,True)
            except:
                print("Bad Data",dealer_dic)

class Engine(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            float(name)
        except:
            return Engine.objects.get_or_create(name=name)
        return (None,False)

class Body(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            float(name)
        except:
            return Body.objects.get_or_create(name=name)
        return (None,False)


class Color(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            float(name)
        except:
            return Color.objects.get_or_create(name=name)
        return (None,False)

class Make(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            float(name)
        except:
            return Make.objects.get_or_create(name=name)
        return (None,False)

class Car_Model(models.Model):

    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    def fill(make, name):
        try:
            m = Make.objects.get(name=make)
            return Car_Model.objects.get_or_create(name=name,make=m)
        except:
            return (None,False)

class Transmission(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            float(name)
        except:
            return Transmission.objects.get_or_create(name=name)
        return (None,False)

class Year(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            int(name)
            return Year.objects.get_or_create(name=name)
        except:
            return (None,False)


class Car(models.Model):

    vin = models.CharField(max_length=120, primary_key = True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_model = models.ForeignKey(Car_Model, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    body = models.ForeignKey(Body, on_delete=models.CASCADE)
    price = models.IntegerField() 
