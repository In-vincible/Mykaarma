from django.shortcuts import render
import csv
from .models import *
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.http import JsonResponse

def read_csv(filename):
    csv_file = open(filename)
    reader = csv.DictReader(csv_file)
    return list(reader)


def create_modals(filename):
    reader = read_csv(filename)
    engine_no = Engine.objects.all().count()
    body_no = Body.objects.all().count()
    transmission_no = Transmission.objects.all().count()
    make_no = Make.objects.all().count()
    model_no = Car_Model.objects.all().count()
    year_no = Year.objects.all().count()
    color_no = Color.objects.all().count()
    dealer_no = Dealer.objects.all().count()
    colors = set()
    transmission = set()
    body = set()
    engine = set()
    make = set()
    car_model = set()
    year = set()
    dealers = {}
    for row in reader:
        colors.add(row['Color'])
        transmission.add(row['Transmission'])
        body.add(row['Body'])
        engine.add(row['Engine'])
        make.add(row['Make'])
        year.add(row['Year'])
        car_model.add((row['Make'], row['Model']))
        dealer_dic = {}
        dealer_dic['id'] = row['DealerID']
        dealer_dic['name'] = row['DealerName']
        dealer_dic['email'] = row['DealerEmail']
        dealer_dic['lon'] = row['DealerLongitude']
        dealer_dic['lat'] = row['DealerLatitude']
        dealers[dealer_dic['id']] = dealer_dic

    # Automatic is in the colors column
    colors.remove('Automatic')
    for name in colors:
        Color.fill(name)
    for name in transmission:
        Transmission.fill(name)
    for name in body:
        Body.fill(name)
    for name in engine:
        Engine.fill(name)
    for name in make:
        Make.fill(name)
    for name in year:
        Year.fill(name)
    for m,name in car_model:
        Car_Model.fill(m,name)
    for dealer in dealers.values():
        Dealer.fill(dealer)
    
    post_engine_no = Engine.objects.all().count()
    post_body_no = Body.objects.all().count()
    post_transmission_no = Transmission.objects.all().count()
    post_make_no = Make.objects.all().count()
    post_model_no = Car_Model.objects.all().count()
    post_year_no = Year.objects.all().count()
    post_color_no = Color.objects.all().count()
    post_dealer_no = Dealer.objects.all().count()
    print("Colors Created: ",post_color_no-color_no)
    print("Year Created: ",post_year_no-year_no)
    print("Engine Created: ",post_engine_no-engine_no)
    print("Body Created: ",post_body_no-body_no)
    print("Make Created: ",post_make_no-make_no)
    print("Car Models Created: ",post_model_no-model_no)
    print("Transmission Created: ",post_transmission_no-transmission_no)
    print("Dealers Created: ", post_dealer_no-dealer_no)

def get_dealer(request):

    response = {}
    response['status'] = 0
    if request.method == 'GET':
        post = request.GET
        distance = post['distance']
        ref_location = Point(float(post['lon']),float(post['lat']))
        # dealers = Dealer.objects.filter(point__distance_lte=(ref_location, D(m=distance))).distance(ref_location).order_by('distance')
        dealers = Dealer.objects.filter(point__distance_lte=(ref_location, D(m=distance))).annotate(distance=Distance('point', ref_location)).order_by('distance')
        dealers_json = []
        for dealer in dealers:
            dealer_object = {}
            dealer_object['dealerId'] = dealer.dealerId
            dealer_object['name'] = dealer.name
            dealer_object['email'] = dealer.email
            dealer_object['lat'] = dealer.point[1]
            dealer_object['lon'] = dealer.point[0]
            dealers_json.append(dealer_object)
        
        response['data'] = dealers_json
        response['status'] = 1
        return JsonResponse(response)
    else:
        return JsonResponse(response)