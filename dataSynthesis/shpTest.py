import warnings; warnings.filterwarnings(action='ignore')
import matplotlib.pyplot as plt
import geopandas as gpd
from /longsgis.py import voronoiDiagram4plg
gpd.options.use_pygeos = True

dataPath = "../data/MSP/parks/"

fig, ax = plt.subplots(figsize = (10,6))

mask = gpd.read_file("../data/MSP/CountyMask.shp")
sp = gpd.read_file(dataPath + "shp_bdry_admin_boundary_data/bdry_park.shp")
mpls = gpd.read_file("../data/MSP/parks/Hennepin_County_Parks-shp/Hennepin_County_Parks.shp")

'''
sp.loc[:, 'geometry'].plot(ax=ax)
mpls.loc[:, 'geometry'].plot(ax=ax)
mask.loc[:, 'geometry'].plot(ax=ax)
'''

print(type(mpls), type(mask))
mask = mask.loc[:, 'geometry']
print(mpls)
print(mask)
voronoiDiagram4plg(mpls, mask)

plt.show()
