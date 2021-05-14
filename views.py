from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CustomerForm, CreateUserForm, FilterForm, NearMeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
# from .forms import NearMeForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q, QuerySet
from django.contrib.gis.db.models import Q
import json
# from .models import Place
from django.http import JsonResponse
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.db.models import Q  # new
from django.contrib.gis.db.models.functions import GeometryDistance

from .models import School_info
from .utils import get_geo, get_ip_address
import json
from ip2geotools.databases.noncommercial import DbIpCity
import urllib3

from django.conf import settings


# from django.contrib.gis.utils import GeoIP


# from django.contrib.gis.measure import Distance


#
# class AddPlaceView(CreateView):
#     model = Place
#     template_name = "sch/place_form.html"
#     success_url = "/index_location/"
#     fields = ("location", "address")


# class ChangePlaceView(UpdateView):
#     model = Place
#     template_name = "sch/place_form.html"
#     success_url = "/index_location/"
#     fields = ("location", "address")

#
# class PlacesView(ListView):
#     model = Place
#     template_name = "sch/index_location.html"
#     ordering = ["-created_at", ]
def home(request):
    return render(request, 'sch/index.html')


def contact(request):
    return render(request, 'sch/contact.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, )
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form': form}
    return render(request, 'sch/register.html', context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Customer':
                return redirect('home')
        # if group=='Doctor':
        # 	return redirect('doc')
        # if group=='Receptionist':
        # 	return redirect('reception')
        # if group=='human_resource':
        # 	return redirect('human_resource')
        # if group=='admin':
        # 	return redirect('#')

        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'sch/login.html')


def about(request):
    return render(request, 'sch/about.html')


def category(request):
    return render(request, 'sch/category.html')


query2 = ""

def SearchResultsView(request):

    global query2
    gens = gender.objects.all()
    boards = Board_allowed.objects.all()
    items = School_info.objects.all()
    facs = Facility.objects.all()
    dists = Distance.objects.all()
    query = request.GET.get('q')
    query2 = query

    gend = request.GET.get('ty')
    object_list = Area.objects.filter(
        Q(area__icontains=query))
    print(object_list)
    ref_location = (object_list.values()[0].get('location'))

    res = School_info.objects.annotate(distance=GeometryDistance("location", ref_location)) \
              .order_by("distance")[:100]

    return render(request, 'sch/locationwise.html',
                  {'items': res, 'gens': gens, 'boards': boards, 'facs': facs, 'dists': dists})


def category_gender(request, gender_name):
    gens = gender.objects.all()
    boards = Board_allowed.objects.all()
    items = School_info.objects.all()
    facs = Facility.objects.all()
    print(request.GET)
    gend = request.GET.get('ty')

    if gend == "Co-Ed School" or gend == "Only Boys School" or gend == "Only Girls School":
        tys = items.filter(gender_allowed=gend)
        return render(request, 'sch/category.html', {'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs})
    elif gend == "CBSE" or gend == "IGCSE" or gend == "IB" or gend == "State Board" or gend == "ICSE":
        tys = items.filter(board=gend)
        return render(request, 'sch/category.html', {'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs})
    elif gend == "AC Classrooms" or gend == "Transportation" or gend == "Swimming Pool":
        if (gend == "AC Classrooms"):
            tys = items.filter(ac_classes="Yes ")
            print(tys)
        elif gend == "Transportation":
            tys = items.filter(transportation="Yes ")
        elif gend == "Swimming Pool":
            tys = items.filter(swimming_pool="Yes ")
        return render(request, 'sch/category.html', {'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs})

    return render(request, 'sch/category.html', {'items': items, 'gens': gens, 'boards': boards, 'facs': facs})

    # gens = gender.objects.all()
    # boards = Board_allowed.objects.all()
    # items = School_info.objects.all()
    # facs = Facility.objects.all()
    # dists = Distance.objects.all()
    #
    # gend = request.GET.get('ty')
    # object_list = Area.objects.filter(
    # Q(area__icontains=query2))
    # print("query2")
    # print(query2)
    # print(object_list)
    # ref_location = (object_list.values()[0].get('location'))
    # res = School_info.objects.annotate(distance=GeometryDistance("location", ref_location)).order_by("distance")[:100]
    #
    # if gend == "Co-Ed School" or gend == "Only Boys School" or gend == "Only Girls School":
    #     tys = items.filter(gender_allowed=gend)
    #     return render(request, 'sch/category.html', {'items': res, 'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs, })
    # elif gend == "CBSE" or gend == "IGCSE" or gend == "IB" or gend == "State Board" or gend == "ICSE":
    #     tys = items.filter(board=gend)
    #     return render(request, 'sch/category.html', {'items': res, 'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs})
    #
    # elif gend == "AC Classrooms" or gend == "Transportation" or gend == "Swimming Pool":
    #      if gend == "AC Classrooms":
    #          tys = items.filter(ac_classes="Yes ")
    #          print(tys)
    #      elif gend == "Transportation":
    #          tys = items.filter(transportation="Yes ")
    #      elif gend == "Swimming Pool":
    #          tys = items.filter(swimming_pool="Yes ")
    #      return render(request, 'sch/category.html', {'items': res, 'gens': gens, 'tys': tys, 'boards': boards, 'facs': facs})
    #
    # return render(request, 'sch/category.html',
    #                       {'items': filter11, 'gens': gens, 'boards': boards, 'facs': facs})


    # print(request.GET)
    # ty1 = request.GET.get('ty1')
    # ty2 = request.GET.get('ty2')
    # ty3 = request.GET.get('ty3')
    # ty4 = request.GET.get('ty4')
    # ty5 = request.GET.get('ty5')
    # ty6 = request.GET.get('ty6')
    # ty7 = request.GET.get('ty7')
    # ty8 = request.GET.get('ty8')
    # ty9 = request.GET.get('ty9')
    # ty10 = request.GET.get('ty10')
    # ty11 = request.GET.get('ty11')



def category(request):
    gens = gender.objects.all()
    items = School_info.objects.all()
    boards = Board_allowed.objects.all()
    facs = Facility.objects.all()

    return render(request, 'sch/category.html', {'items': items, 'gens': gens, 'boards': boards, 'facs': facs})


# class SearchResultsView(ListView):
#     model = Area
#     template_name = 'search_results.html'
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Area.objects.filter(
#             Q(area__icontains=query))
#         return object_list
#
#


def autocomplete(request):
    qs = Area.objects.filter(area__istartswith=request.GET.get('term'))
    print(qs)
    titles = list()
    for product in qs:
        titles.append(product.area)
        print(titles)
    return JsonResponse(titles, safe=False)
    # return render(request, 'sch/index.html')


def search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        ans = Area.objects.filter(area__icontains=search_str) | School_info.objects.filter(
            school_name__icontains=search_str) | School_info.objects.filter(address__icontains=search_str)

        data = ans.values()
        return JsonResponse(list(data), safe=False)


def school_page(request, pk):
    item = School_info.objects.get(id=pk)

    return render(request, 'sch/school_page.html', {'item': item})


def add_details(request):
    context = {}

    # create object of form
    form = CustomerForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, 'sch/add_details.html', context)


def near_me(request):
    gens = gender.objects.all()
    boards = Board_allowed.objects.all()
    items = School_info.objects.all()
    facs = Facility.objects.all()
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')
    latitude = float(latitude)
    longitude = float(longitude)
    # latitude = 19.242439
    # longitude = 73.120193
    ref_location = Point(longitude, latitude, srid=4326)

    res = School_info.objects.annotate(distance=GeometryDistance("location", ref_location)) \
              .order_by("distance")[:100]

    return render(request, 'sch/locationwise.html',
                  {'items': res, 'gens': gens, 'boards': boards, 'facs': facs})

    # # return HttpResponse("<html><head></head>,body>"+ str(latitude) + " " + str(longitude)+ "  </body></html>")
    # # dists = Distance.objects.all()
    # # if request.method == 'POST':
    # #     latitude = request.POST['lat']
    # #     longitude = request.POST['long']
    # # g = GeoIP()
    # # lat, lng = g.lat_lon(user_ip)
    # #
    # ip = get_ip_address(request)
    # # if ip == '127.0.0.1':
    # #     ref_location = Point(-97.8220, 37.7510)
    # #
    # #     #ref_location = Point(72.862358, 19.116625)
    # #     ref_location = Point(0.0, 0.0)
    # # else:
    # #     # response = DbIpCity.get(ip, api_key='free')
    # #     # longitude = response.longitude
    # #     # latitude = response.latitude
    # #     ref_location = get_geo(ip)
    # #
    # for service in settings.IPCOUNTRY_APYKEY:
    #     url = service["url"].format(ip=ip, **service["params"])
    #     headers = {'Type': 'django', 'Ver': '1.1.1', 'Connection': 'Close'}
    #     urllib3.disable_warnings()
    #     http_call = urllib3.PoolManager()
    #     try:
    #         r = http_call.request('GET', url, headers=headers, timeout=1.0)
    #         if r.status == 200:
    #             json_response = json.loads(r.data.decode("utf-8"))
    #             print("HII ISKE NICHE KUC HTOH AYEGA")
    #             print(json_response)
    #     except Exception as e:
    #         pass
    #
    # return None

    # g = GeoIP()
    # ip = request.META.get('REMOTE_ADDR', None)
    # if ip:
    #     city = g.city(ip)['city']
    # else:
    #     city = 'Rome'  # default city
    # ip = get_ip_address(request)
    # ref_location = Point(longitude, latitude)

    # form = NearMeForm()
    # if request.method == 'POST':
    #     form = NearMeForm(request.POST)
    #     if form.is_valid():
    #
    #         user = form.save()
    #         Customer.objects.update(user=user, )
    #         group = Group.objects.get(name='Customer')
    #         user.groups.add(group)
    #         username = form.cleaned_data.get('location')
    #         messages.success(request, 'location is collected for' + username)
    #
    #         html = "<html><body>Yayyyyyyyyyyyy.</body></html>"
    #         return HttpResponse(html)
    #
    #     context = {'form': form}
    #     html1 = "<html><body>Nooooooooooooo.</body></html>"
    #     return HttpResponse(html1)


# def location(request):
#     context = {}
#
#     # create object of form
#     form = LocationForm(request.POST or None, request.FILES or None)
#
#     # check if form data is valid
#     if form.is_valid():
#         # save the form data to model
#         form.save()
#
#     context['form'] = form
#     return render(request, 'sch/location.html')


def searchmap(request):
    return render(request, 'sch/gmapsapi.html')


def registered(request):
    return render(request, 'sch/registered.html')


def get_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = School_info.objects.filter(
            Q(address__icontains=q) |
            Q(school_name__icontains=q)

        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def register_school(request):
    # count = 0
    if request.method == "POST":
        # count = count + 1
        school_name = request.POST.get('school_name', '')
        gender_allowed = request.POST.get('gender_allowed', '')
        type_school = request.POST.get('type_school', '')
        board = request.POST.get('board', '')
        fees = request.POST.get('fees', '')
        grade = request.POST.get('grade', '')
        min_age = request.POST.get('min_age', '')
        medium = request.POST.get('medium', '')
        avg_class_strength = request.POST.get('avg_class_strength', '')
        estd = request.POST.get('estd', '')
        school_strength = request.POST.get('school_strength', '')
        swimming_pool = request.POST.get('swimming_pool', '')
        indoor_sports = request.POST.get('indoor_sports', '')
        ac_classes = request.POST.get('ac_classes', '')
        transportation = request.POST.get('transportation', '')
        outdoor_sports = request.POST.get('outdoor_sports', '')
        annual_fees = request.POST.get('annual_fees', '')
        admission_fees = request.POST.get('admission_fees', '')
        phone1 = request.POST.get('phone1', '')
        phone2 = request.POST.get('phone2', '')
        phone3 = request.POST.get('phone3', '')
        phone4 = request.POST.get('phone4', '')
        address = request.POST.get('address', '')
        latitude = float(request.POST.get('lat', ''))
        longitude = float(request.POST.get('long', ''))
        location = Point(longitude, latitude)

        school = School_info(school_name=school_name, gender_allowed=gender_allowed,
                             type_school=type_school,
                             board=board, fees=fees, grade=grade, min_age=min_age,
                             medium=medium, avg_class_strength=avg_class_strength, estd=estd,
                             school_strength=school_strength, swimming_pool=swimming_pool,
                             indoor_sports=indoor_sports, ac_classes=ac_classes, transportation=transportation,
                             outdoor_sports=outdoor_sports, annual_fees=annual_fees,
                             admission_fees=admission_fees, phone1=phone1, phone2=phone2, phone3=phone3, phone4=phone4,
                             address=address, location=location)
        school.save()
        return redirect('home')
    return render(request, "sch/register_school.html")
    
    
    
    # def category_temp(request):
    # if request.method == 'POST':
    #     print("idhartakhi")
    #     form = FilterForm(request.POST)
    #     if form.is_valid():
    #
    #         print("aaayaaaaaa")
    #         ty1 = form.cleaned_data['ty1']
    #         ty2 = form.cleaned_data['ty2']
    #         ty3 = form.cleaned_data['ty3']
    #         ty4 = form.cleaned_data['ty4']
    #         ty5 = form.cleaned_data['ty5']
    #         ty6 = form.cleaned_data['ty6']
    #         ty7 = form.cleaned_data['ty7']
    #         ty8 = form.cleaned_data['ty8']
    #         ty9 = form.cleaned_data['ty9']
    #         ty10 = form.cleaned_data['ty10']
    #         ty11 = form.cleaned_data['ty11']
    #         print(ty1)
    #         print(ty2)
    #         print(ty3)
    #         print(ty4)
    #         print(ty5)
    #         print(ty6)
    #         print(ty7)
    #         print(ty8)
    #         print(ty9)
    #         print(ty10)
    #         print(ty11)
    #         if ty1 != "":
    #             filter1 = items.filter(gender_allowed=ty1)
    #         else:
    #             filter1 = items
    #         if ty2 != "":
    #             filter2 = filter1.filter(gender_allowed=ty2)
    #         else:
    #             filter2 = filter1
    #         if ty3 != "":
    #             filter3 = filter2.filter(gender_allowed=ty3)
    #         else:
    #             filter3 = filter2
    #         if ty4 != "":
    #             filter4 = filter3.filter(board=ty4)
    #         else:
    #             filter4 = filter3
    #         if ty5 != "":
    #             filter5 = filter4.filter(board=ty5)
    #         else:
    #             filter5 = filter4
    #         if ty6 != "":
    #             filter6 = filter5.filter(board=ty6)
    #         else:
    #             filter6 = filter5
    #         if ty7 != "":
    #             filter7 = filter6.filter(board=ty7)
    #         else:
    #             filter7 = filter6
    #         if ty8 != "":
    #             filter8 = filter7.filter(board=ty8)
    #         else:
    #             filter8 = filter7
    #         if ty9 != "":
    #             filter9 = filter8.filter(ac_classes="Yes ")
    #         else:
    #             filter9 = filter8
    #         if ty10 != "":
    #             filter10 = filter9.filter(transportation="Yes ")
    #         else:
    #             filter10 = filter9
    #         if ty11 != "":
    #             filter11 = filter10.filter(swimming_pool="Yes ")
    #         else:
    #             filter11 = filter10

