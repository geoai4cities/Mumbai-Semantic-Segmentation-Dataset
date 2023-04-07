import os
from tqdm import tqdm
from osgeo import ogr
import numpy as np
import pandas as pd
import geopandas as gpd
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

folder = Path("/home/internship/.Ayush_Dabra/Mumbai_Data/jp22/jp22_shape_file/jp22")
shapefiles = folder.glob("jp22.*.shp")

# gdf = pd.concat([gpd.read_file(shp) for shp in shapefiles]).pipe(gpd.GeoDataFrame)
gdf = pd.concat([gpd.read_file(shp) for shp in tqdm(shapefiles, desc="[Merging…]", ascii=False, ncols=75)]).pipe(gpd.GeoDataFrame)
gdf.to_file(f'/home/internship/.Ayush_Dabra/Mumbai_Data/jp22/jp22_shape_file/merged_shapefile/green_idx_map.shp')