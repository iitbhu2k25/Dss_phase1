from django.shortcuts import render
from django.http import JsonResponse
from .models import RasterVisual
from django.conf import settings
import os
import rasterio
import mimetypes
import rasterio.features
import rasterio.warp
from django.http import FileResponse, HttpResponseNotFound, HttpResponseBadRequest,JsonResponse
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

def get_raster_file(request, category, file_name):
    raster = RasterVisual.objects.filter(name=file_name, organisations=category).values('file_location').first()
    if not raster:
        return JsonResponse({"error": "File not found in the database"}, status=404)
    
    file_location = raster["file_location"]
    file_path = os.path.join(settings.MEDIA_ROOT, file_location)
    
    if not os.path.exists(file_path):
        return JsonResponse({"error": "File not found on disk"}, status=404)
    content_type, _ = mimetypes.guess_type(file_path)
    
    # Default to application/octet-stream if content type can't be determined
    if not content_type:
        # Check common raster formats
        if file_name.lower().endswith('.tif') or file_name.lower().endswith('.tiff'):
            content_type = 'image/tiff'
        elif file_name.lower().endswith('.asc') or file_name.lower().endswith('.ascii'):
            content_type = 'text/plain'
        else:
            content_type = 'application/octet-stream'
    
    # Open the file and create a response
    response = FileResponse(
        open(file_path, 'rb'),
        content_type=content_type,
        as_attachment=False,
        filename=file_name
    )
    
    # Add CORS headers if needed
    response["Access-Control-Allow-Origin"] = "*"
    
    # Add Content-Disposition header to prevent browsers from trying to display the file
    response["Content-Disposition"] = f"inline; filename={file_name}"
    
    return response