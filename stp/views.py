from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
import geopandas as gpd
from .models import Villages,District,Sub_district,State,Stp_subdis
from shapely.geometry import mapping
from .service import weight_redisturb,normalize_data,rank_process,process_geometries
def stp_home(request):
    return render(request, 'stp/prediction.html')

@csrf_exempt
def GetStatesView(request):
    states=State.objects.values('state_id','state_name')
    states=[{'id': state['state_id'],'name':state['state_name']} for state in states]
    return JsonResponse(list(states),safe=False)

@csrf_exempt
def GetDistrictView(request):
    if request.method == 'POST':
        state_id=int(json.loads(request.body).get('state'))
        print("state id is ",state_id)
        districts=District.objects.values('district_id','district_name').filter(state_id=state_id)
        districts=[{'id': district['district_id'],'name':district['district_name']} for district in districts]
        return JsonResponse(list(districts),safe=False)

@csrf_exempt
def GetSubDistrictView(request):
    if request.method == 'POST':
        district_id=(json.loads(request.body).get('districts'))
        sub_districts=list(Sub_district.objects.values('subdistrict_id','subdistrict_name').filter(district_id__in=district_id))
        sub_districts=[{'id': sub_district['subdistrict_id'],'name':sub_district['subdistrict_name']} for sub_district in sub_districts]
        return JsonResponse(list(sub_districts),safe=False)

@csrf_exempt
def  GetVillageView(request):
    if request.method == 'POST':
        sub_district_id=(json.loads(request.body).get('subDistricts'))
        villages=list(Villages.objects.values('village_id','village_name').filter(subdistrict_id_id__in=sub_district_id))
        villages=[{'id': village['village_id'],'name':village['village_name']} for village in villages]
        return JsonResponse(list(villages),safe=False)

@csrf_exempt
def GetTableView(request):
    if request.method == 'POST':
        request=json.loads(request.body)
        main_data=request.get('main_data')
        vig_data=main_data['villages']
        table_id=[]
        for i in vig_data:
            table_id.append(int(i[8:]))
        categories=request.get('categories')
        ans=Data.objects.values('name',*categories).filter(id__in=table_id)
        ans=list(ans)
        for i in ans:
            print(i)
        return JsonResponse(ans,safe=False)
    
@csrf_exempt
def GetRankView(request):
    if request.method == 'POST':
        request=json.loads(request.body)
        table_data=request.get('tableData')
        headings=[]
        for i in table_data[0]:
            headings.append(i)        
        headings.remove('name')
        weight_key=weight_redisturb(headings)
        table_data=normalize_data(table_data)
        ans=rank_process(table_data,weight_key,headings)
        print('main ans',ans)
        return JsonResponse(ans,safe=False)

@csrf_exempt
def GetVillage_UP(request):
    try:
        try:
            request_data = json.loads(request.body)
            villages_list=request_data.get('village_name')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        try:
            gdf = gpd.read_file('media/shapefile/villages/Basin_Villages.shp')

        except Exception as e:
            print('erris is ',str(e))
            return JsonResponse({'error': 'Error reading geographic data'}, status=500)

        # Filter geodataframe
        print("village_list",villages_list)
        filtered_gdf = gdf[gdf['NAME_1'].isin(villages_list)]
        print("filtered_gdf",filtered_gdf)
        coordinates = process_geometries(filtered_gdf)
        print("coor",coordinates)
        if not coordinates:
            return JsonResponse({'error': 'Failed to extract valid coordinates'}, status=500)

        if len(coordinates) > 1:
            coordinates = [coordinates]

        return JsonResponse({'coordinates': coordinates})

    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
def GetBoundry(request):
    if request.method == 'GET':
        try:
            print("try to get all the polygon")
            states_polygon= Stp_subdis.objects.all()
            features = []
            for poly in states_polygon:
                feature = {
                    'type': 'Feature',
                    'geometry': eval(poly.geometry.json),
                    'properties': {
                        'state_name': poly.state_name,
                    }
                }
                features.append(feature)
            
            geojson_data = {
                'type': 'FeatureCollection',
                'features': features
            }
            print("asdasdasdasd")
            return JsonResponse(geojson_data, safe=False)

        except Exception as e:
            print("error is",str(e))
            return JsonResponse({'error': str(e)}, status=500)
        
    if request.method == 'POST':
        try:
            # Read the shapefile
            request_data = json.loads(request.body)
            print(request_data)
            try:
                if request_data.get('subDistricts'):
                    subDistrict_Id=request_data.get('subDistricts')
                    subdistrict_polygon=Stp_subdis.objects.all().filter(subdis_cod__in=subDistrict_Id)
                    features = []
                    for poly in subdistrict_polygon:
                        feature = {
                            'type': 'Feature',
                            'geometry': eval(poly.geometry.json),
                            'properties': {
                                'name': poly.subdis_nam,
                            }
                        }
                        features.append(feature)
                    geojson_data = {
                        'type': 'FeatureCollection',
                        'features': features
                    }
                    return JsonResponse(geojson_data, safe=False)
                elif request_data.get('districts'):
                    District_Id=request_data.get('districts')
                    district_polygon=Stp_subdis.objects.all().filter(dist_code__in=District_Id)
                    features = []
                    for poly in district_polygon:
                        feature = {
                            'type': 'Feature',
                            'geometry': eval(poly.geometry.json),
                            'properties': {
                                'name': poly.subdis_nam,
                            }
                        }
                        features.append(feature)
                    geojson_data = {
                        'type': 'FeatureCollection',
                        'features': features
                    }
                    return JsonResponse(geojson_data, safe=False)
                
                else :
                    stateId=request_data.get('stateId')
                    state_polygon=Stp_subdis.objects.all().filter(state_code=stateId)
                    features = []
                    for poly in state_polygon:
                        feature = {
                            'type': 'Feature',
                            'geometry': eval(poly.geometry.json),
                            'properties': {
                                'district_name': poly.dist_name,
                            }
                        }
                        features.append(feature)
                    geojson_data = {
                        'type': 'FeatureCollection',
                        'features': features
                    }
                    return JsonResponse(geojson_data, safe=False)


            #     print("request data is ",request_data)
            #     if request_data.get('villages'):
            #         # village_list = request_data['villages']
            #         # filtered_gdf = gdf[gdf['NAME'].isin(village_list)]
            #         # print(filtered_gdf)
            #         pass
                
            #     elif request_data.get('subDistricts'):
            #         # subdistrict = request_data['subDistricts']
            #         # subdistrict=list(map(int,subdistrict))
            #         # filtered_gdf = gdf[(gdf['Subdistric'].isin(subdistrict))]
            #         # print(filtered_gdf)
            #         pass
                
            #     elif request_data.get('districts'):
            #         # district = request_data['districts']
            #         # print("district_data ",district)
            #         # district= list(map(int, district))
            #         # filtered_gdf = gdf[(gdf['District_1'].isin(district))]
            #         # print("filtered_gdf is",filtered_gdf)
            #         pass
               
                
            #     else:
            #         return JsonResponse({'error': 'No valid geographic criteria provided'}, status=400)
                
            except Exception as e:
                print(f"Error filtering or processing data: {str(e)}")
                return JsonResponse({'error': 'Error processing geographic data'}, status=500)
                
        except Exception as e:
            print(f"Error reading shapefile or processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)