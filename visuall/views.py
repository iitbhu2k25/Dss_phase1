from django.shortcuts import render
from django.http import JsonResponse
from .models import RasterVisual
from django.conf import settings
import os
import rasterio
import rasterio.features
import rasterio.warp
from django.http import HttpResponse, JsonResponse
from django.conf import settings

# Create your views here.
def visual_home(request):
    return render(request,'visuall/base.html')
    

# to get the organozations
def get_raster(request):
    organize = list(RasterVisual.objects.distinct('organisations').values_list('organisations', flat=True))
    print("the organisations is ",organize)
    return JsonResponse(organize,safe=False)


# to get the name of rater file base on organisations
def get_raster_lists(request,category):
        raster_data = list(RasterVisual.objects.filter(organisations=category)  
        .order_by('name') 
        .distinct('name') 
        .values_list('name', flat=True) 
        )
        print("list of file is",raster_data)
        return JsonResponse(raster_data,safe=False)

# to get the raster file based on the file name 
def get_raster_file(request, category, file_name):
    raster = RasterVisual.objects.filter(name=file_name, organisations=category).values('file_location').first()
    if not raster:
        return JsonResponse({"error": "File not found in the database"}, status=404)
    
    file_location = raster["file_location"]
    file_path = os.path.join(settings.MEDIA_ROOT, file_location)
    
    if not os.path.exists(file_path):
        return JsonResponse({"error": "File not found on disk"}, status=404)
    
    try:
        with rasterio.open(file_path) as dataset:
            # Get basic metadata
            bounds = dataset.bounds
            width = dataset.width
            height = dataset.height
            
            # Convert bounds to the format Leaflet expects (if needed)
            leaflet_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]
            
            # Read the actual data (for smaller rasters)
            band_data = dataset.read(1).tolist()  # Reading first band as an example
            
            # Return metadata and possibly data
            return JsonResponse({
                "bounds": leaflet_bounds,
                "width": width,
                "height": height,
                "crs": dataset.crs.to_string(),
                "data": band_data,  # Only include for smaller rasters
                "file_url": request.build_absolute_uri(settings.MEDIA_URL + file_location)
            })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)