from django.shortcuts import render
from django.http import JsonResponse
from .models import raster_visual
import os
import tempfile
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.gis.gdal import GDALRaster

# Create your views here.
def visual_home(request):
    return render(request,'visuall/base.html')
    

def get_raster(request):
    cate = list(raster_visual.objects.order_by('name').distinct('name').values_list('name', flat=True))
    print("cate is ", cate)
    return JsonResponse(cate,safe=False)


def get_raster_lists(request,category):
        print("inside the gget")
        raster_data = list(raster_visual.objects.filter(name=category)  
        .order_by('phase_year') 
        .distinct('phase_year') 
        .values_list('phase_year', flat=True) 
        )
        return JsonResponse(raster_data,safe=False)

# def get_raster_tile(request, category, value, z, x, y):

#     try:
#         # Convert tile coordinates to integers
#         z, x, y = int(z), int(x), int(y)
        
#         # Find the raster in the database
#         raster_data = list(
#             raster_visual.objects
#             .filter(name=category, phase_year=value).values_list('rast', flat=True).all()
#         )
        
#         if not raster_data:
#             return JsonResponse({"error": "Raster not found"}, status=404)
        
#         # Use the first raster if multiple are returned
#         raster_path = raster_data[0].name
#         if not os.path.exists(raster_path):
#             raster_path = os.path.join(settings.MEDIA_ROOT, raster_path)
        
#         # Set GDAL performance options
#         gdal.SetConfigOption('GDAL_CACHEMAX', '512')
#         gdal.SetConfigOption('VSI_CACHE', 'TRUE')
        
#         # Open the raster dataset
#         ds = gdal.Open(raster_path, gdal.GA_ReadOnly)
#         if not ds:
#             return JsonResponse({"error": "Could not open raster"}, status=500)
        
#         # Get tile bounds in Web Mercator (EPSG:3857)
#         tile_bounds = mercantile.bounds(x, y, z)
        
#         # Create a temporary file for the output tile
#         with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
#             tmp_filename = tmp_file.name
        
#         # Create options for gdal.Translate
#         translate_options = gdal.TranslateOptions(
#             format='PNG',
#             outputType=gdal.GDT_Byte,
#             width=256,
#             height=256,
#             projWin=[
#                 tile_bounds.west,   # left
#                 tile_bounds.north,  # top 
#                 tile_bounds.east,   # right
#                 tile_bounds.south   # bottom
#             ],
#             projWinSRS='EPSG:3857',  # Web Mercator
#             resampleAlg=gdal.GRA_Bilinear,  # Bilinear resampling
#             noData='none'
#         )
        
#         # Generate the tile
#         gdal.Translate(tmp_filename, ds, options=translate_options)
        
#         # Open the generated tile with PIL for post-processing
#         img = Image.open(tmp_filename)
        
#         # Save the processed image
#         img.save(tmp_filename)
        
#         # Read the file and return it as an HTTP response
#         with open(tmp_filename, 'rb') as f:
#             tile_data = f.read()
        
#         # Clean up the temporary file
#         os.unlink(tmp_filename)
        
#         # Return the tile with appropriate content type
#         response = HttpResponse(tile_data, content_type='image/png')
#         response['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
#         return response
        
#     except Exception as e:
#         import traceback
#         print(traceback.format_exc())
#         return JsonResponse({"error": str(e)}, status=500)
