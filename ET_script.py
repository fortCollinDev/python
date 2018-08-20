import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("spatial")
workspace = arcpy.env.workspace = r"C:\\Users\\nreluser\\Desktop\\Evapotranspiration data\\"
arcpy.env.overwriteOutput = True
arcpy.env.cellSize = 30

# Local variables:
ta_2017_fin = workspace + r"\GRIDmat\ta_2017_fin"
dt198_utm = workspace + r"\dt198_utm_fin"
Ts = (workspace + r"\Final_LST.tif")
pet_2017 = workspace + r"\GRIDmat\pet_2017_fin"
NDVI = workspace + r"\NDVI_0717"
pet_2017_fin = workspace + r"\GRIDmat\pet_2017_fin"

# Process: get NDVI values for greater than 0.66
NDVI_66 = Raster(NDVI) >= 0.66
NDVI_66.save(workspace + r"\NDVI_66.tif")

# Process: Extract Ta from NDVI values greater than 0.66
Ta_extract_66 = Raster(ta_2017_fin) * Raster("NDVI_66.tif")
Ta_extract_66.save("Ta_extract_66.tif")

# Process: Extract Ts from NDVI values greater than 0.66
Ts_extract_66 = Raster(Ts) * Raster("NDVI_66.tif")
Ts_extract_66.save("Ts_extract_66.tif")

# Process: calculate c from Ts and Ta
c_values_66 = Raster("Ts_extract_66.tif") / Raster("Ta_extract_66.tif")
c_values_66.save("c_values_66.tif")

# Process: get the mean from all c values
c_mean = arcpy.GetRasterProperties_management("c_values_66.tif","mean")
c_mean_final = float(c_mean[0])

# Process: get the std from all c values
c_std = arcpy.GetRasterProperties_management("c_values_66.tif","std")
c_std_final = float(c_std[0])

# Process: calculate final c value
c_final = c_mean_final - (2 * (c_std_final))
#c_final.save("c_final.tif")

#calculate Tc
Tc = Raster(ta_2017_fin) * c_final
Tc.save("Tc.tif")

#calculate Th
Th = Raster("Tc.tif") + Raster(dt198_utm)
Th.save("Th.tif")


#calculate ETf
ETf = (Raster("Th.tif") - Raster(Ts))/ Raster(dt198_utm)
ETf.save("ETf.tif")

#final! calculate ETa
ETa = Raster("ETf.tif") *1.2 * Raster(pet_2017_fin)
ETa.save("ETa.tif")



"""
Everything below here works
"""



# Local variables:
ta_2017_fin = r"C:\Users\nreluser\Desktop\Evapotranspiration data\GRIDmat\ta_2017_fin"
dt198_utm = r"C:\Users\nreluser\Desktop\Evapotranspiration data\dt198_utm_fin"
Ts = (r"C:\Users\nreluser\Desktop\Evapotranspiration data\Final_LST.tif")
pet_2017 = r"C:\Users\nreluser\Desktop\Evapotranspiration data\GRIDmat\pet_2017_fin"
NDVI = r"C:\Users\nreluser\Desktop\Evapotranspiration data\NDVI_0717"
pet_2017_fin = r"C:\Users\nreluser\Desktop\Evapotranspiration data\GRIDmat\pet_2017_fin"

# Process: get NDVI values for greater than 0.66
NDVI_66 = Raster(NDVI) >= 0.66
NDVI_66.save(r"C:\Users\nreluser\Desktop\Evapotranspiration data\NDVI_66.tif")

# Process: Extract Ta from NDVI values greater than 0.66
Ta_extract_66 = Raster(ta_2017_fin) * Raster("NDVI_66.tif")
Ta_extract_66.save("Ta_extract_66.tif")

# Process: Extract Ts from NDVI values greater than 0.66
Ts_extract_66 = Raster(Ts) * Raster("NDVI_66.tif")
Ts_extract_66.save("Ts_extract_66.tif")

# Process: calculate c from Ts and Ta
c_values_66 = Raster("Ts_extract_66.tif") / Raster("Ta_extract_66.tif")
c_values_66.save("c_values_66.tif")

# Process: get the mean from all c values
c_mean = arcpy.GetRasterProperties_management("c_values_66.tif","mean")
c_mean_final = float(c_mean[0])

# Process: get the std from all c values
c_std = arcpy.GetRasterProperties_management("c_values_66.tif","std")
c_std_final = float(c_std[0])

# Process: calculate final c value
c_final = c_mean_final - (2 * (c_std_final))
#c_final.save("c_final.tif")

#calculate Tc
Tc = Raster(ta_2017_fin) * c_final
Tc.save("Tc.tif")

#calculate Th
Th = Raster("Tc.tif") + Raster(dt198_utm)
Th.save("Th.tif")


#calculate ETf
ETf = (Raster("Th.tif") - Raster(Ts))/ Raster(dt198_utm)
ETf.save("ETf.tif")

#final! calculate ETa
ETa = Raster("ETf.tif") *1.2 * Raster(pet_2017_fin)
ETa.save("ETa.tif")



# Process: Raster Calculator
#arcpy.gp.RasterCalculator("\"%ETf%\" * 1.2* \"%pet_2017_fin%\"", ETa)

#from decimal import *
#c = Decimal(c_mean)
#print c
#c_mean_final = float(int("c_mean"))
#print int(float(c_mean.getOutput(0)))
#print int((c_mean.getOutput(0)))
#c_mean_final = c_mean.getOutput(0)
