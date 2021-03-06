from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import csv
from .models import *
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
import time
from django.utils import timezone
from datetime import datetime

def read_csv(filename):
    csv_file = open(filename)
    reader = csv.DictReader(csv_file)
    return list(reader)

def set_price_range():
    makes = Make.objects.all()
    for make in makes:
        cars = Car.objects.filter(car_model__make=make).order_by('price')
        make.min_price = cars[0].price
        make.max_price = cars[cars.count()-1].price
        make.save()

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
    car_no = Car.objects.all().count()
    rating_no = Rating.objects.all().count()
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
        rating_dic = {}
        rating_dic['value'] = row['DealerAvgRatingOutOf5']
        rating_dic['people_rated'] = row['NumberOfPeopleRated']
        rating_dic['dealerId'] = dealer_dic['id']
        dealer_dic['rating'] = rating_dic
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
        Rating.fill(dealer['rating'])
    for row in reader:
        Car.fill(row)
    set_price_range()
    post_engine_no = Engine.objects.all().count()
    post_body_no = Body.objects.all().count()
    post_transmission_no = Transmission.objects.all().count()
    post_make_no = Make.objects.all().count()
    post_model_no = Car_Model.objects.all().count()
    post_year_no = Year.objects.all().count()
    post_color_no = Color.objects.all().count()
    post_dealer_no = Dealer.objects.all().count()
    post_car_no = Car.objects.all().count()
    post_rating_no = Rating.objects.all().count()
    print("Colors Created: ",post_color_no-color_no)
    print("Year Created: ",post_year_no-year_no)
    print("Engine Created: ",post_engine_no-engine_no)
    print("Body Created: ",post_body_no-body_no)
    print("Make Created: ",post_make_no-make_no)
    print("Car Models Created: ",post_model_no-model_no)
    print("Transmission Created: ",post_transmission_no-transmission_no)
    print("Dealers Created: ", post_dealer_no-dealer_no)
    print("Cars Created: ", post_car_no-car_no)
    print("Rating Created: ",post_rating_no-rating_no)


def get_dealer(request):

    response = {}
    print(request.META['REMOTE_ADDR'])
    response['status'] = 0
    try:
        start = time.time()
        current = start
        post = request.GET
        if 'distance' in post:
            distance = post['distance']
        else:
            distance = 200000000
        
        ref_location = Point(float(post['lon']),float(post['lat']))

        dealers = Dealer.objects
        if 'model' in post:
            dealers = dealers.filter(car__car_model__make__name=post['model']).distinct()
            tm = time.time()
            print("Time Taken to filter with models %f"%(tm-current))
            current = tm

        if 'min_price' in post:
            dealer_ids = Car.objects.filter(price__gte = post['min_price']).values("dealer").distinct()
            dealer_ids = [d['dealer'] for d in dealer_ids]
            dealers = dealers.filter(dealerId__in=dealer_ids)
            tm = time.time()
            print("Time Taken to filter with min_price %f"%(tm-current))
            current = tm

        if 'max_price' in post:
            dealer_ids = Car.objects.filter(price__lte = post['max_price']).values("dealer").distinct()
            dealer_ids = [d['dealer'] for d in dealer_ids]
            dealers = dealers.filter(dealerId__in=dealer_ids)
            tm = time.time()
            print("Time Taken to filter with max_price %f"%(tm-current))
            current = tm

        # Filtering by distance
        dealers = dealers.filter(point__distance_lte=(ref_location, D(m=distance))).annotate(distance=Distance('point', ref_location)).order_by('distance')
         
        dealers_json = []
        for dealer in dealers:
            c_m_s = Car_Model.objects.filter(car__dealer=dealer).distinct()
            makes = Make.objects.filter(car_model__in=c_m_s).distinct()
            
            dealer_object = {}
            dealer_object['dealerId'] = dealer.dealerId
            dealer_object['name'] = dealer.name
            dealer_object['email'] = dealer.email
            dealer_object['lat'] = dealer.point[1]
            dealer_object['lon'] = dealer.point[0]
            dealer_object['rating_value'] = dealer.rating.value
            dealer_object['people_rated'] = dealer.rating.people_rated
            makes_response = []
            for make in makes:
                make_object = {}
                make_object['name'] = make.name
                make_object['min_price'] = make.min_price
                make_object['max_price'] = make.max_price
                makes_response.append(make_object)
            dealer_object['makes'] = makes_response
            dealers_json.append(dealer_object)
        print("Time Taken in final for loop %f, Total Time %f"%(time.time()-current,time.time()-start))
        response['data'] = dealers_json
        response['status'] = 1
        return JsonResponse(response)
    except Exception as e:
        response['error'] = str(e)
        return JsonResponse(response)


def sign_in(request):
    if request.POST:
        print(1)
        cred = request.POST
        u = authenticate(username=cred['username'],password=cred['password'])
        if u is not None:
            login(request, u)
            return redirect('/')
        else:
            messages.warning(request, 'username or password dont match.')
            return render(request, 'login.html')
    else:
        print(2)
        return render(request, 'login.html')


def sign_up(request):
    if request.POST:
        info = request.POST
        try:    
            u = User.objects.get(username = info['username'])
            messages.warning(request, 'Username already exists! Please choose different username.')
            return render(request, 'signup.html')
        except:
            u = User.objects.create_user(username=info['username'],password=info['password'],email=info['email'])
            u.save()
            return redirect('/login/')
    else:
        return render(request,'signup.html')

@csrf_exempt
def reset_pass(request):
    if request.POST:  
        u = authenticate(username=request.POST['username'],password=request.POST['old_password'])
        if u is not None:
            u.set_password(request.POST['new_password'])
            u.save()
            return redirect('/login/')
        else:
            messages.warning(request, 'Please enter correct old password!')
            return render(request, 'reset_pass.html')
    else:
        return render(request,'reset_pass.html')

def index(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'products.html', {'user' : user, 'status' : True})
    else:
        return render(request, 'products.html', {'status' : False})

@login_required(login_url='/login/')
def sign_out(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def send_email(request):
    r =  requests.post(
    "https://api.mailgun.net/v3/mg.technex.in/messages",
    auth=("api", "key-cf7f06e72c36031b0097128c90ee896a"),
    data={"from": "Mykaarma<mykaarma@appathon.in>",
          "to": request.POST['recipient'],
          "subject": "mail from customer",
          "text": request.POST['body']})
    r = r.json()
    return JsonResponse(r)

def search_car(request):
    response = {}
    response['status'] = 0
    if request.GET:
        info = request.GET
        param = info['type']
        results = None
        ip = request.META['REMOTE_ADDR']
        car_array = []
        
        if param == 'make':
            results = Make.objects.filter(name__icontains=info['value']).distinct()
            
            for result in results:
                
                car_object = {}
                car_object['Make'] = result.name
                dealers = Dealer.objects.filter(car__car_model__make=result).distinct()
                dealer_array  = []
                
                for dealer in dealers:
                    dealer_object = {}
                    dealer_object['dealerId'] = dealer.dealerId
                    dealer_object['name'] = dealer.name
                    dealer_object['email'] = dealer.email
                    dealer_object['lat'] = dealer.point[1]
                    dealer_object['lon'] = dealer.point[0]
                    dealer_object['rating_value'] = dealer.rating.value
                    dealer_object['people_rated'] = dealer.rating.people_rated
                    dealer_array.append(dealer_object)
                
                car_object['dealers'] = dealer_array
                car_array.append(car_object)
        
        elif param == 'model':
            results = Car_Model.objects.filter(name__icontains=info['value']).distinct()
            
            for result in results:
                car_object = {}
                car_object['Model'] = result.name
                dealers = Dealer.objects.filter(car__car_model=result).distinct()
                dealer_array  = []
                
                for dealer in dealers:
                    dealer_object = {}
                    dealer_object['dealerId'] = dealer.dealerId
                    dealer_object['name'] = dealer.name
                    dealer_object['email'] = dealer.email
                    dealer_object['lat'] = dealer.point[1]
                    dealer_object['lon'] = dealer.point[0]
                    dealer_object['rating_value'] = dealer.rating.value
                    dealer_object['people_rated'] = dealer.rating.people_rated
                    dealer_array.append(dealer_object)
                car_object['dealers'] = dealer_array
                car_array.append(car_object)
        
        response['data'] = car_array
        
        visit = None
        try:
            visit = Visits.objects.get(ip=ip)
            if request.user.is_authenticated:
                visit.user = request.user
                visit.save()
        except:
            visit = Visits(ip=ip)
            if request.user.is_authenticated:
                visit.user = request.user
            visit.save()
        
        for car in results:    
            search = Searches.objects.create(content_object=car, visit=visit)
        
        response['status'] = 1
    else:
        response['status'] = 0
        response['message'] = "Invalid Request."
    
    return JsonResponse(response)


def past_searches(request):
    response = {}
    response['status'] = 0
    print("reached")
    if request.method == 'GET':
        info = request.GET
        ip = request.META['REMOTE_ADDR']
        start = info.get('start', "2018-01-01")
        end = info.get('end', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(start,end)
        searches = []
        if 1:# try:
            if request.user.is_authenticated:
                searches = Searches.objects.filter(time__range=[start,end], visit__user=request.user) 
            else:
                searches = Searches.objects.filter(time__range=[start,end], visit__ip=ip)
        else:# except:
            response['message'] = "Invlid date format"
            return JsonResponse(response)
        results_array=[]
        for search in searches:
            result_object = {}
            result_object['type'] = search.content_type.model
            result_object['name'] = search.content_object.name
            result_object['time'] = search.time.strftime("%Y-%m-%d %H:%M")
            results_array.append(result_object)
        response['data'] = results_array
        response['status'] = 1
    else:
        response['status'] = 0
        response['message'] = "Invalid Request."
    
    return JsonResponse(response)

