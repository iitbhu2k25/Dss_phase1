# mapplot/views.py
from django.shortcuts import render
from django.http import JsonResponse
import geopandas as gpd
import os
import uuid
from django.conf import settings
import logging
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)

# Set GDAL configuration
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

ALLOWED_EXTENSIONS = {'shp', 'dbf', 'shx', 'prj'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def shapefile_viewer(request):
    return render(request, 'shapefile_viewer.html')

def upload_shapefile(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        logger.info("Starting file upload process")
        
        if not request.FILES.getlist('files'):
            logger.error("No files in request")
            return JsonResponse({'error': 'No files provided'}, status=400)
        
        files = request.FILES.getlist('files')
        category = request.POST.get('category', '')
        subcategory = request.POST.get('subcategory', '')
        
        # Create upload directory structure
        upload_path = os.path.join('shapefile', category, subcategory)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, upload_path))
        
        # Track uploaded files
        uploaded_files = []
        file_extensions = set()
        base_filename = None
        
        # Find the .shp file first
        for file in files:
            if file.name.lower().endswith('.shp'):
                base_filename = os.path.splitext(file.name)[0]
                break
        
        if not base_filename:
            return JsonResponse({'error': 'No .shp file found'}, status=400)
        
        # Save all files
        for file in files:
            if file and allowed_file(file.name):
                ext = os.path.splitext(file.name)[1].lower()
                new_filename = f"{base_filename}{ext}"
                filepath = fs.save(new_filename, file)
                uploaded_files.append(fs.path(filepath))
                file_extensions.add(ext[1:])
        
        # Verify required files
        required_extensions = {'shp', 'dbf', 'shx'}
        missing_extensions = required_extensions - file_extensions
        
        if missing_extensions:
            return JsonResponse({
                'error': f"Missing required files: {', '.join(missing_extensions)}"
            }, status=400)
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def get_shapefile_data(request):
    try:
        category = request.GET.get('category', '')
        subcategory = request.GET.get('subcategory', '')
        
        logger.info(f"Requested category: {category}, subcategory: {subcategory}")

        shapefile_paths = {
            'administrative': {
                'district': os.path.join('shapefile', 'Administrative', 'District', 'Districts.shp'),
                'villages': os.path.join('shapefile', 'Administrative', 'Villages', 'Villages_PCS.shp')
            },
            'watershed': {
                'varuna': os.path.join('shapefile', 'Watershed', 'Varuna', 'Varuna_Watershed.shp'),
                'basuhi': os.path.join('shapefile', 'Watershed', 'Basuhi', 'Basuhi_Watershed.shp'),
                'morwa': os.path.join('shapefile', 'Watershed', 'Morwa', 'Morwa_Watershed.shp'),
                'all': os.path.join('shapefile', 'Watershed', 'All', 'Watershed.shp')
            },
            'drains': {
                'varuna': os.path.join('shapefile', 'DrainsOutlet', 'Varuna_Drain', 'Varuna_Drain.shp'),
                'basuhi': os.path.join('shapefile', 'DrainsOutlet', 'Basuhi_Drain', 'Basuhi_Drain.shp'),
                'morwa': os.path.join('shapefile', 'DrainsOutlet', 'Morwa_Drain', 'Morwa_Drain.shp')
            },
            'canals': {
                'all': os.path.join('shapefile', 'Canals', 'Canals.shp')
            },
            'household': {
                'All': os.path.join('shapefile', 'Households', 'All', 'Households.shp'),
                'Bhadohi': os.path.join('shapefile', 'Households', 'Bhadohi','Bhadohi', 'Households_Bhadohi.shp'),
                'Jaunpur': os.path.join('shapefile', 'Households', 'Jaunpur', 'Jaunpur', 'Households_Jaunpur.shp'),
                'Pratapgarh': os.path.join('shapefile', 'Households', 'Pratapgarh', 'Pratapgarh', 'Households_Pratapgarh.shp'),
                'Prayajraj': os.path.join('shapefile', 'Households', 'Prayajraj', 'Prayajraj', 'Households_Prayagraj.shp'),
                'Varanasi': os.path.join('shapefile', 'Households', 'Varanasi', 'Varanasi', 'Households_varanasi.shp')
            },
            'railways': {
                'all': os.path.join('shapefile', 'Railways', 'Railways.shp')
            },
            'industries': {
                'all': os.path.join('shapefile', 'Industries', 'Industries.shp')
            },
            'rivers': {
                'varuna': os.path.join('shapefile', 'Rivers', 'Varuna', 'Varuna_River.shp'),
                'basuhi': os.path.join('shapefile', 'Rivers', 'Basuhi', 'Basuhi_River.shp'),
                'morwa': os.path.join('shapefile', 'Rivers', 'Morwa', 'Morwa_River.shp')
            },
            'roads': {
                'all': os.path.join('shapefile', 'Roads', 'Roads.shp')
            },
            'stps': {
                'all': os.path.join('shapefile', 'STPs', 'STP.shp')
            }
        }

        if category in shapefile_paths and subcategory in shapefile_paths[category]:
            shapefile_path = os.path.join(settings.MEDIA_ROOT, shapefile_paths[category][subcategory])
            
            # Check if file exists
            if not os.path.exists(shapefile_path):
                logger.error(f"Shapefile not found at path: {shapefile_path}")
                return JsonResponse({
                    'error': f'Shapefile not found: {shapefile_paths[category][subcategory]}'
                }, status=404)
            
            logger.info(f"Reading shapefile from: {shapefile_path}")

            # Read the shapefile
            gdf = gpd.read_file(shapefile_path)
            
            # Add this to see coordinates in your console
            # print("Sample of coordinates:")
            # for idx, row in gdf.head().iterrows():
            #  print(f"Feature {idx} coordinates:")
            # print(row.geometry)
            
            # Convert to WGS84 if needed
            if gdf.crs and gdf.crs != 'EPSG:4326':
                logger.info("Converting CRS to EPSG:4326")
                gdf = gdf.to_crs('EPSG:4326')

            features = []
            for idx, row in gdf.iterrows():
                try:
                    geometry = row.geometry
                    if geometry is None or geometry.is_empty:
                        continue
                    
                    properties = row.drop('geometry').to_dict()
                    
                    # Process different geometry types
                    if geometry.geom_type == 'Polygon':
                        coords = []
                        exterior_coords = geometry.exterior.coords.xy
                        for x, y in zip(exterior_coords[0], exterior_coords[1]):
                            coords.append([float(x), float(y)])
                        
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Polygon',
                                'coordinates': [coords]
                            },
                            'properties': properties
                        })
                    
                    elif geometry.geom_type == 'MultiPolygon':
                        multi_coords = []
                        for polygon in geometry.geoms:
                            coords = []
                            exterior_coords = polygon.exterior.coords.xy
                            for x, y in zip(exterior_coords[0], exterior_coords[1]):
                                coords.append([float(x), float(y)])
                            multi_coords.append(coords)
                            
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'MultiPolygon',
                                'coordinates': [multi_coords]
                            },
                            'properties': properties
                        })
                    
                    elif geometry.geom_type == 'LineString':
                        coords = []
                        line_coords = geometry.coords.xy
                        for x, y in zip(line_coords[0], line_coords[1]):
                            coords.append([float(x), float(y)])
                            
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'LineString',
                                'coordinates': coords
                            },
                            'properties': properties
                        })
                    
                    elif geometry.geom_type == 'MultiLineString':
                        multi_coords = []
                        for line in geometry.geoms:
                            coords = []
                            line_coords = line.coords.xy
                            for x, y in zip(line_coords[0], line_coords[1]):
                                coords.append([float(x), float(y)])
                            multi_coords.append(coords)
                            
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'MultiLineString',
                                'coordinates': multi_coords
                            },
                            'properties': properties
                        })
                    
                    elif geometry.geom_type == 'Point':
                        x, y = geometry.x, geometry.y
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [float(x), float(y)]
                            },
                            'properties': properties
                        })
                    
                    elif geometry.geom_type == 'MultiPoint':
                        multi_coords = []
                        for point in geometry.geoms:
                            x, y = point.x, point.y
                            multi_coords.append([float(x), float(y)])
                            
                        features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'MultiPoint',
                                'coordinates': multi_coords
                            },
                            'properties': properties
                        })
                    
                    # Additional handling for complex Polygon geometries
                    elif geometry.geom_type == 'GeometryCollection':
                        for subgeom in geometry.geoms:
                            if subgeom.geom_type == 'Polygon':
                                coords = []
                                exterior_coords = subgeom.exterior.coords.xy
                                for x, y in zip(exterior_coords[0], exterior_coords[1]):
                                    coords.append([float(x), float(y)])
                                
                                features.append({
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Polygon',
                                        'coordinates': [coords]
                                    },
                                    'properties': properties
                                })
                            
                            elif subgeom.geom_type == 'Point':
                                x, y = subgeom.x, subgeom.y
                                features.append({
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [float(x), float(y)]
                                    },
                                    'properties': properties
                                })
                    
                    logger.info(f"Successfully processed feature {idx}")
                    
                except Exception as e:
                    logger.error(f"Error processing feature {idx}: {str(e)}")
                    continue
                    
            if not features:
                logger.error("No valid features were processed")
                return JsonResponse({'error': 'No valid features found in shapefile'}, status=400)
                
            logger.info(f"Successfully processed {len(features)} features")
            
            geojson = {
                'type': 'FeatureCollection',
                'features': features
            }
                
            return JsonResponse(geojson)
            
        else:
            logger.error(f"Invalid category ({category}) or subcategory ({subcategory})")
            return JsonResponse({'error': 'Invalid category or subcategory'}, status=400)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
    
    # Add this to your view
        print(f"Processing shapefile for {category}/{subcategory}")
        print(f"Coordinate sample: {gdf.geometry.iloc[0]}")