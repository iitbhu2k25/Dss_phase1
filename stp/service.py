from .models import Weight
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union
import geopandas as gpd
def weight_redisturb(headings):
   weights=Weight.objects.values(*headings)
   weights=list(weights)
   print('weights',weights)
   weights=weights[0]
   sum:float=0.0
   for i in weights:
      sum+=weights[i]
   for i in weights:
      weights[i]=weights[i]/sum
   return weights

def normalize_data(data):
   numerical_columns = [key for key in data[0].keys() if isinstance(data[0][key], (int, float)) and key != 'name']
   numerical_data = [[entry[col] for col in numerical_columns] for entry in data]
   scaler = MinMaxScaler()
   normalized_values = scaler.fit_transform(numerical_data)
   normalized_data = []
   for i, entry in enumerate(data):
        normalized_entry = {'name': entry['name']}  # Keep the 'name' column unchanged
        for j, col in enumerate(numerical_columns):
            normalized_entry[col] = normalized_values[i][j]
        normalized_data.append(normalized_entry)
   return normalized_data

def rank_process(data,weight_key,headings):
    df = pd.DataFrame(data, columns=headings)
    ranks=df.rank(method='min', ascending=False)
    weightted_rank=ranks*pd.Series(weight_key)
    df['rank']=weightted_rank.sum(axis=1)
    # for find the rank probability
    # scaler = MinMaxScaler()
    # df['rank'] = scaler.fit_transform(df[['rank']])
    df['name'] = [entry['name'] for entry in data]
    final_results = df[['name', 'rank']]
    final_results=final_results.to_dict(orient='records')
    return final_results

def fix_geometry(geometry):
    """
    Fix and validate geometry objects from shapefile, handling both single geometries
    and pandas Series of geometries.
    Args:
        geometry: A shapely geometry object or a GeoSeries
    Returns:
        Fixed geometry object or None if geometry cannot be fixed
    """
    try:
        # Handle None or empty geometries
        if pd.isna(geometry) or geometry is None:
            print("geometry is None or NA")
            return None
        
        # Get the actual geometry object if it's a Series
        if hasattr(geometry, 'geometry'):
            geometry = geometry.geometry
        
        # Try to make geometry valid if it isn't
        try:
            if not geometry.is_valid:
                geometry = make_valid(geometry)
        except Exception as e:
            print(f"Error in make_valid: {str(e)}")
            return None
        
        # Check if geometry is empty
        try:
            if geometry.is_empty:
                print("geometry is empty")
                return None
        except Exception as e:
            print(f"Error checking if empty: {str(e)}")
            return None
        
        # Handle Polygon or MultiPolygon
        if isinstance(geometry, (Polygon, MultiPolygon)):
            print('geometry is valid Polygon/MultiPolygon')
            return geometry
        
        # Try to convert other geometry types
        try:
            unified = ops.unary_union(geometry)
            if isinstance(unified, (Polygon, MultiPolygon)):
                return unified
            else:
                print(f"Unexpected geometry type after unary_union: {type(unified)}")
                return None
        except Exception as e:
            print(f"Error in unary_union: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error in fix_geometry: {str(e)}")
        return None

def process_geometries(filtered_gdf):
    """
    Process all geometries in the filtered GeoDataFrame.
    Returns a list of coordinate lists.
    """
    coordinates = []
    
    try:
        # Dissolve geometries if multiple features exist
        if len(filtered_gdf) > 1:
            try:
                filtered_gdf = filtered_gdf.dissolve()
            except Exception as e:
                print(f"Error during dissolve operation: {str(e)}")
                # Continue with undissolved geometries
                pass

        # Process the geometries
        for geometry in filtered_gdf.geometry:
            if geometry is None:
                continue
                
            fixed_geometry = fix_geometry(geometry)
            if fixed_geometry is None:
                continue

            try:
                if isinstance(fixed_geometry, Polygon):
                    print("Processing Polygon")
                    # Get coordinates from the exterior ring
                    coords = fixed_geometry.exterior.coords
                    # Convert coordinates to list of [lat, lon] pairs
                    coord_list = []
                    for coord in coords:
                        # coord[0] is x (longitude), coord[1] is y (latitude)
                        coord_list.append([float(coord[1]), float(coord[0])])
                    coordinates.append(coord_list)
                
                elif isinstance(fixed_geometry, MultiPolygon):
                    print("Processing MultiPolygon")
                    for polygon in fixed_geometry.geoms:
                        # Get coordinates from each polygon's exterior ring
                        coords = polygon.exterior.coords
                        # Convert coordinates to list of [lat, lon] pairs
                        coord_list = []
                        for coord in coords:
                            # coord[0] is x (longitude), coord[1] is y (latitude)
                            coord_list.append([float(coord[1]), float(coord[0])])
                        print("Appending polygon coordinates")
                        coordinates.append(coord_list)
                else:
                    print(f"Unexpected geometry type: {type(fixed_geometry)}")

            except Exception as e:
                print(f"Error processing single geometry: {str(e)}")
                print(f"Geometry type: {type(fixed_geometry)}")
                continue

    except Exception as e:
        print(f"Error processing geometries: {str(e)}")
        return []

    print(f"Total coordinates processed: {len(coordinates)}")
    return coordinates