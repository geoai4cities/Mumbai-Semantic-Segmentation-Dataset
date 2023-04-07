import os
from tqdm import tqdm
from osgeo import ogr
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def calc_gos_idx(pred_img_dir, pred_img_file):
    total_pixels = 128*128
    img = plt.imread(f'{pred_img_dir}{pred_img_file}')
    # plt.imshow(img)
    # plt.show()
    colors, counts = np.unique(img.reshape(-1, 3), axis=0, return_counts=True)
    colors *= 255
    green_rgb_idx = np.where(colors==[ 80., 140.,  50.]) #RGB code for vegetation
    open_rgb_idx = np.where(colors==[ 200., 160., 40.]) #RGB code for barren

    # print(np.size(green_rgb_idx))
    if np.size(green_rgb_idx) == 0:
        green_idx = 0
        # print(green_idx)
    else: 
        green_rgb_count = counts[green_rgb_idx[0][0]]
        green_idx = round(green_rgb_count/total_pixels, 3)
        # print(green_idx)

    # print(np.size(open_rgb_idx))
    if np.size(open_rgb_idx) == 0:
        open_idx = 0
        # print(open_idx)
    else: 
        open_rgb_count = counts[open_rgb_idx[0][0]]
        open_idx = round(open_rgb_count/total_pixels, 3)
        # print(open_idx)

    gos_idx = green_idx + open_idx
    return green_idx, open_idx, gos_idx

def polygonize(raster_dir, shapefile_dir, pred_img_dir):
    rasters = np.array(os.listdir(raster_dir))
    rasters = np.sort(rasters)
    print(rasters)
    driver = ogr.GetDriverByName('ESRI Shapefile')

    for tile in tqdm(rasters, desc="[Polygonizing…]", ascii=False, ncols=75):
        tile = str(tile) 
        os.system(f'gdal_polygonize.py {raster_dir}{tile} -f "ESRI Shapefile" {shapefile_dir}{tile.split(".tif")[0]}.shp -q')
        dataSource = driver.Open(f"{shapefile_dir}{tile.split('.tif')[0]}.shp", 1) #1 is read/write
        
        green_fldDef = ogr.FieldDefn('green_idx', ogr.OFTReal)
        layer = dataSource.GetLayer()
        layer.CreateField(green_fldDef)

        open_fldDef = ogr.FieldDefn('open_idx', ogr.OFTReal)
        layer = dataSource.GetLayer()
        layer.CreateField(open_fldDef)

        gos_fldDef = ogr.FieldDefn('gos_idx', ogr.OFTReal)
        layer = dataSource.GetLayer()
        layer.CreateField(gos_fldDef)

        green_idx, open_idx, gos_idx = calc_gos_idx(pred_img_dir=f'{pred_img_dir}', pred_img_file = f"{tile.split('.tif')[0]}.png")
        for feature in layer:
            # print(feature)
            feature.SetField('green_idx', green_idx)
            feature.SetField('open_idx', open_idx)
            feature.SetField('gos_idx', gos_idx)
            layer.SetFeature(feature)
        

raster_dir = '/home/internship/.Ayush_Dabra/Mumbai_Data/jp22/jp22/'
shapefile_dir = '/DATA/.Ayush_Dabra/Mumbai_Data/jp22_shape_file/jp22_gos/'
pred_img_dir='/DATA/.Ayush_Dabra/Mumbai_Data/vgg16_unet_pred_tiles/'

if __name__ == "__main__":
    polygonize(raster_dir=raster_dir, shapefile_dir=shapefile_dir, pred_img_dir=pred_img_dir)
