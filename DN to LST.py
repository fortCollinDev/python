import arcpy
arcpy.CheckOutExtension("spatial")
workplace = arcpy.env.workspace = r"C:\\Users\\nreluser\\Desktop\\Evapotranspiration data\\"
import math
import glob
from arcpy.sa import *
arcpy.env.overwriteOutput = True


#this can be used to gather the raster you need
rasterList = (glob.glob(workspace + "\\*.tif"))
band_list = ['B10','B4','B5']

rastDict = {}#this is an empty dictionary
# a dictionary is an object that stores values based on a key
# the structure is ['key', object]
# it's nice because you can then select features based on a logical key
# in this case band 10 will be selected by rastDict["B10"]
# this will return the path to the raster, no more chasing path names
for i in band_list:
	for j in rasterList:
		if i in j:
			rastDict[str(i)] = j
			print('The band ', i, ' have been added to rastDict')

Band_10 = rastDict["B10"]
Band_4 = rastDict["B4"]
Band_5 = rastDict["B5"]

tnb = 0.866 # narrow band transmissivity of air
rp = 0.91 # path radiance
rsky = 1.32 # narrow band downward thermal radiation from a clear sky
sunelev = 64.76874296
sun = 90 - sunelev
zenith = Cos(sun)

K1_Band_10 = 774.8853
K2_Band_10 = 1321.0789
K1_Band_11 = 480.8883 # thermal conversion contstant from the metadata
K2_Band_11 = 1201.1442
RADIANCE_ADD_BAND_4 = -48.36300
RADIANCE_MULT_BAND_4 = 9.6726e-03
RADIANCE_ADD_BAND_5 = -29.59575
RADIANCE_MULT_BAND_5 = 5.9191e-03
RADIANCE_ADD_BAND_10 = 0.10000
RADIANCE_MULT_BAND_10 = 3.3420e-04

workspace1= "this is path to putput folder"

#convert to radiance
Band_4_Radiance = (Raster(Band_4) * RADIANCE_MULT_BAND_4) + RADIANCE_ADD_BAND_4 # TOA reflectance w/o correction for solar angle
Band_4_Radiance.save(workspace1 + "\\Band_4_Radiance.tif")
Band_4_Final = Raster("Band_4_Radiance.tif") / zenith # TOA planetary reflectance
Band_4_Final.save(workspace1 + "\\Band_4_Final.tif")

Band_5_Radiance = (Raster(Band_5) * RADIANCE_MULT_BAND_5) + RADIANCE_ADD_BAND_5
Band_5_Radiance.save(workspace1 + "\\Band_5_Radiance.tif")
Band_5_Final = Raster("Band_5_Radiance.tif") / zenith
Band_5_Final.save(workspace1 + "\\Band_5_Final.tif")

#Band 10
Band_10_Radiance = (Raster(Band_10) * RADIANCE_MULT_BAND_10) + RADIANCE_ADD_BAND_10
Band_10_Radiance.save(workspace1 + "\\Band_10_Radiance.tif")
Band_10_Final = Raster("Band_10_Radiance.tif") / zenith
Band_10_Final.save(workspace1 + "\\Band_10_Final.tif")

#NDVI calculation
NDVI = (Raster("Band_5_Final.tif") - Raster("Band_4_Final.tif"))/(Raster("Band_5_Final.tif") + Raster("Band_4_Final.tif"))
NDVI.save(workspace1 + "\\NDVI_Rad.tif")


# Emissivity Calculation
NDVI_filtered = (Raster("NDVI_Rad.tif") >= 0.2) & (Raster("NDVI_Rad.tif")<=0.5)
NDVI_filtered.save(workspace1 + "\\NDVI_filtered.tif")
Pv = (Raster("NDVI_filtered.tif") - 0.2) / 0.3 * 2
Pv.save(workspace1 + "\\Pv.tif")

dE = ((1- 0.97) * (1- Raster("Pv.tif")) * (0.55) * (0.99))
dE.save(workspace + "\\dE.tif")
RangeEmiss = (0.99 * (Raster("Pv.tif"))) + (0.97 * (1 - (Raster("Pv.tif")))) + (Raster("dE.tif"))
RangeEmiss.save(workspace1 + "\\RangeEmiss.tif")
Emissivity = Con(Raster("NDVI_Rad.tif") <0 , 0.985, Con ((Raster("NDVI_Rad.tif") >=0) & (Raster("NDVI_Rad.tif")<0.2), 0.977, Con(Raster("NDVI_Rad.tif") > 0.5, 0.99, Con((Raster("NDVI_Rad.tif") >= 0.2) & (Raster("NDVI_Rad.tif") <= 0.5), RangeEmiss))))
Emissivity.save(workspace1 + "\\Emissivity.tif")

#Band 10 Radiance to LST
rc10 = ((Raster("Band_10_Radiance.tif") - rp)/tnb) - ((rsky) * (1 - Raster("Emissivity.tif")))
rc10.save(workspace1 + "\\rc10.tif")
Final_LST = K2_Band_10 / (Ln((K1_Band_10 * Raster("Emissivity.tif") / rc10) + 1))
Final_LST.save(workspace1 + "\\Final_LST.tif")


"""
Everything below here works
Above is just changes that I made to reduce the amount of path names that are needed to be manually entered
"""


#variables

Band_10 = r"C:\Users\nreluser\Desktop\Evapotranspiration data\Landsat thermal\LC08_L1TP_035034_20170717_20170727_01_T1_B10.TIF"
Band_11 = r"C:\Users\nreluser\Desktop\Evapotranspiration data\Landsat thermal\LC08_L1TP_035034_20170717_20170727_01_T1_B11.TIF"
Band_4 = r"C:\Users\nreluser\Desktop\Evapotranspiration data\Landsat thermal\LC08_L1TP_035034_20170717_20170727_01_T1_B4.TIF"
Band_5 = r"C:\Users\nreluser\Desktop\Evapotranspiration data\Landsat thermal\LC08_L1TP_035034_20170717_20170727_01_T1_B5.TIF"
#MP4value = 0.00002 # aka RADIANCE_MULT_BAND_4
#APAvalue = -0.1 # aka RADIANCE_ADD_BAND_4
#MP5value = 0.00002
#MP5value = -0.1
#MP10value = 0.00002
#MP10value = -0.1
tnb = 0.866 # narrow band transmissivity of air
rp = 0.91 # path radiance
rsky = 1.32 # narrow band downward thermal radiation from a clear sky
sunelev = 64.76874296
sun = 90 - sunelev
zenith = Cos(sun)

K1_Band_10 = 774.8853
K2_Band_10 = 1321.0789
K1_Band_11 = 480.8883 # thermal conversion contstant from the metadata
K2_Band_11 = 1201.1442
RADIANCE_ADD_BAND_4 = -48.36300
RADIANCE_MULT_BAND_4 = 9.6726e-03
RADIANCE_ADD_BAND_5 = -29.59575
RADIANCE_MULT_BAND_5 = 5.9191e-03
RADIANCE_ADD_BAND_10 = 0.10000
RADIANCE_MULT_BAND_10 = 3.3420e-04

#convert to radiance
Band_4_Radiance = (Raster(Band_4) * RADIANCE_MULT_BAND_4) + RADIANCE_ADD_BAND_4 # TOA reflectance w/o correction for solar angle
Band_4_Radiance.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_4_Radiance.tif")
Band_4_Final = Raster("Band_4_Radiance.tif") / zenith # TOA planetary reflectance
Band_4_Final.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_4_Final.tif")

Band_5_Radiance = (Raster(Band_5) * RADIANCE_MULT_BAND_5) + RADIANCE_ADD_BAND_5
Band_5_Radiance.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_5_Radiance.tif")
Band_5_Final = Raster("Band_5_Radiance.tif") / zenith
Band_5_Final.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_5_Final.tif")

#Band 10
Band_10_Radiance = (Raster(Band_10) * RADIANCE_MULT_BAND_10) + RADIANCE_ADD_BAND_10
Band_10_Radiance.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_10_Radiance.tif")
Band_10_Final = Raster("Band_10_Radiance.tif") / zenith
Band_10_Final.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Band_10_Final.tif")

#NDVI calculation
NDVI = (Raster("Band_5_Final.tif") - Raster("Band_4_Final.tif"))/(Raster("Band_5_Final.tif") + Raster("Band_4_Final.tif"))
NDVI.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\NDVI_Rad.tif")


# Emissivity Calculation
NDVI_filtered = (Raster("NDVI_Rad.tif") >= 0.2) & (Raster("NDVI_Rad.tif")<=0.5)
NDVI_filtered.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\NDVI_filtered.tif")
Pv = (Raster("NDVI_filtered.tif") - 0.2) / 0.3 * 2
Pv.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Pv.tif")

dE = ((1- 0.97) * (1- Raster("Pv.tif")) * (0.55) * (0.99))
dE.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\dE.tif")
RangeEmiss = (0.99 * (Raster("Pv.tif"))) + (0.97 * (1 - (Raster("Pv.tif")))) + (Raster("dE.tif"))
RangeEmiss.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\RangeEmiss.tif")
Emissivity = Con(Raster("NDVI_Rad.tif") <0 , 0.985, Con ((Raster("NDVI_Rad.tif") >=0) & (Raster("NDVI_Rad.tif")<0.2), 0.977, Con(Raster("NDVI_Rad.tif") > 0.5, 0.99, Con((Raster("NDVI_Rad.tif") >= 0.2) & (Raster("NDVI_Rad.tif") <= 0.5), RangeEmiss))))
Emissivity.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Emissivity.tif")

#Band 10 Radiance to LST
rc10 = ((Raster("Band_10_Radiance.tif") - rp)/tnb) - ((rsky) * (1 - Raster("Emissivity.tif")))
rc10.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\rc10.tif")
Final_LST = K2_Band_10 / (Ln((K1_Band_10 * Raster("Emissivity.tif") / rc10) + 1))
Final_LST.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\Final_LST.tif")
