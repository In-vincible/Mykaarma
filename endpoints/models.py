from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

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
            return Engine.objects.get_or_create(name=name)
        except:
            return (None,False)

class Body(models.Model):

    name = models.CharField(max_length=120)

    def fill(name):
        try:
            return Body.objects.get_or_create(name=name)
        except:
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
    min_price = models.IntegerField(default = 0)
    max_price = models.IntegerField(default = 0)
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

    def fill(dic):
        try:
            Car.objects.get(vin = dic['VIN'])
        except:
            try:
                dealer = Dealer.objects.get(dealerId=dic['DealerID'])
                car_make = Make.objects.get(name=dic['Make'])
                car_model = Car_Model.objects.get(name=dic['Model'], make=car_make)
                year = Year.objects.get(name=dic['Year'])
                transmission = Transmission.objects.get(name=dic['Transmission'])
                color = Color.objects.get(name=dic['Color'])
                engine = Engine.objects.get(name=dic['Engine'])
                body = Body.objects.get(name=dic['Body'])
                price = int(dic['PriceInINR'])
                c =  Car(
                            vin=dic['VIN'],
                            dealer=dealer,
                            car_model=car_model,
                            year=year,
                            transmission=transmission,
                            color=color,
                            engine=engine,
                            body=body,
                            price=price
                        )
                c.save()
                return (c,True)
            except:
                print("Bad Data",dic)

class Rating(models.Model):

    value = models.FloatField(default=0)
    dealer = models.OneToOneField(Dealer, on_delete=models.CASCADE)
    people_rated = models.IntegerField(default=0)

    def fill(dic):
        try:
            dealer = Dealer.objects.get(dealerId=dic['dealerId'])
            r = Rating.objects.create(value=dic['value'], dealer=dealer, people_rated=dic['people_rated'])
        except:
            print("Bad Data: ",dic)

class Visits(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

class Searches(models.Model):
    car = models.ForeignKey(Car_Model, on_delete=models.CASCADE)
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE)    