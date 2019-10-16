from django.shortcuts import render
from django.http import HttpResponse
import geo.api as api
import geo.data as data
import geo.typeform as tform
import geo.clusters as clusters


def index(request):
    #return HttpResponse("Hello, world. You're at the geo index.")
    return render(request, 'geo/home.html')

def results(request):
    #search = request.POST['searchbox']

    dictio = clusters.cleandictionary(tform.getDataDict())
    
    
    search = dictio['located']
    role = dictio['role']
    geo = api.getGeoloc(search)
    if geo != None:
        lat = geo["lat"]
        lon = geo["lng"]
        radio = 2500
        companies_df = data.getDf(role,lat,lon,radio)
        center_companies = api.getCenter(companies_df)
        center = center_companies
        near = {}
        for e in dictio['near']:
            near[e] = api.nearby(e,center)
            center = api.updateCenter(near[e],center_companies)


        '''
        zomatodict = api.getZomatoCityID(search)
        rests = api.getVeganRestaurants(zomatodict["id"])
        starbucks = api.getStarbucks(zomatodict["id"])

        center_companies = api.getCenter(companies_df)
        center_rests = api.getCenter(rests)
        center_starbucks = api.getCenter(starbucks)
        center = api.getCenterPonderate(center_companies,center_rests,center_starbucks)
        '''

        compan_order = data.orderdf(companies_df,center)
        #rests_order = data.orderdf(rests,center)
        #star_order = data.orderdf(starbucks,center)
        #airport_order = data.loadDataAirports(lat,lon,center)

        #rest_near = api.getDirCar(center,rests_order[["lat","lon"]].values[0])
        #star_near = api.getDirWalk(center,star_order[["lat","lon"]].values[0])
        addresscenter = api.getAddress(center)

        center_img = api.getCenterMap(center)
        companies_img = api.getMap(search,compan_order,center)
        near_img = api.getNearMap(search,near,dictio['near'],center)
        zomatodict = api.getZomatoGeocode(center)
        location_title = zomatodict['location_title']
        popularity = zomatodict['popularity']
        nightlife = zomatodict['nightlife']
        restaurantlist = zomatodict['restaurants']
        #rest_img = api.getMap(search,rests_order,center)
        #starbucks_img = api.getMap(search,star_order,center)
        #airport_img = api.getMap(search,airport_order,center)
        schools = api.getSchools(search,lat,lon)

        return render(request, 'geo/results.html', {
                'searchbox': search,
                'center_img': center_img,
                'lat': lat,
                'lon': lon,
                #'airport_img': airport_img,
                #'rest_near': rest_near,
                #'star_near': star_near,
                'addresscenter': addresscenter,
                'companies_img': companies_img,
                'near_img': near_img,
                'near': near,
                #'rest_img': rest_img,
                'center': center,
                #'starbucks_img': starbucks_img,
                'location_title': location_title,
                'popularity': popularity,
                'nightlife': nightlife,
                'restaurantlist': restaurantlist,
                'schools': schools,
                'search': search,
                'tables': compan_order.to_html(classes='data',columns=("name","description_x","category_code","homepage_url","distance"), header="true"),
                #'airports': airport_order.to_html(classes='data',columns=("Airport","City","Country","distance"),header="True"),
            })
    else:
        return render(request, 'geo/noresults.html')