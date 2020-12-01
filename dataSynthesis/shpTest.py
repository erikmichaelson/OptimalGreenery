import warnings; warnings.filterwarnings(action='ignore')
import matplotlib.pyplot as plt
import geopandas as gpd
from longsgis import voronoiDiagram4plg
from bufferDissolve import bufferDissolve
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

mask = mask.loc[:, 'geometry']
minimpls = mpls[292:342]
#mplsClean = bufferDissolve(minimpls, 10)
#mplsClean.loc[:, 'geometry'].plot(ax=ax)
#print("minifilt: ", mplsClean, type(mplsClean))
print("mask: ", mask)
minisp = sp[:50]
print("mpls: ", minimpls)
vd = voronoiDiagram4plg(minimpls, mask)
print(vd)
vd.loc[:, 'geometry'].plot(ax=ax)
#minimpls.loc[:, 'geometry'].plot(ax=ax, color="black")
minimpls.loc[:, 'geometry'].plot(ax=ax, color="black")

plt.show()
