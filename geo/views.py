from django.shortcuts import render
from django.http import HttpResponse
import geo.api as api
import geo.data as data


def index(request):
    #return HttpResponse("Hello, world. You're at the geo index.")
    return render(request, 'geo/home.html')

def results(request):
    search = request.POST['searchbox']
    test = api.test(search)

    geo = api.getGeoloc(search)
    lat = geo["lat"]
    lon = geo["lng"]
    radio = 2500
    companies_df = data.getDf(lat,lon,radio)
    zomatodict = api.getZomatoCityID(search)
    rests = api.getVeganRestaurants(zomatodict["id"])
    starbucks = api.getStarbucks(zomatodict["id"])

    center_companies = api.getCenter(companies_df)
    center_rests = api.getCenter(rests)
    center_starbucks = api.getCenter(starbucks)
    center = api.getCenterPonderate(center_companies,center_rests,center_starbucks)

    compan_order = data.orderdf(companies_df,center)
    rests_order = data.orderdf(rests,center)
    star_order = data.orderdf(starbucks,center)
    airport_order = data.loadDataAirports(lat,lon,center)

    rest_near = api.getDirCar(center,rests_order[["lat","lon"]].values[0])
    star_near = api.getDirWalk(center,star_order[["lat","lon"]].values[0])
    addresscenter = api.getAddress(center)

    center_img = api.getCenterMap(center)
    companies_img = api.getMap(search,compan_order,center)
    rest_img = api.getMap(search,rests_order,center)
    starbucks_img = api.getMap(search,star_order,center)
    #airport_img = api.getMap(search,airport_order,center)
    schools = api.getSchools(search,lat,lon)

    return render(request, 'geo/results.html', {
            'searchbox': test,
            'center_img': center_img,
            'lat': lat,
            'lon': lon,
            #'airport_img': airport_img,
            'rest_near': rest_near,
            'star_near': star_near,
            'addresscenter': addresscenter,
            'companies_img': companies_img,
            'rest_img': rest_img,
            'center': center,
            'starbucks_img': starbucks_img,
            'schools': schools,
            'search': search,
            'tables': compan_order.to_html(classes='data',columns=("name","description","category_code","homepage_url","distance"), header="true"),
            'airports': airport_order.to_html(classes='data',columns=("Airport","City","Country","distance"),header="True"),
        })
