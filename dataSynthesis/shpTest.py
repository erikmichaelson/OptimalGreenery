import warnings; warnings.filterwarnings(action='ignore')
import matplotlib.pyplot as plt
import geopandas as gpd

dataPath = "../data/MSP/parks/"

fig, ax = plt.subplots(figsize = (10,6))

sp = gpd.read_file(dataPath + "/shp_bdry_admin_boundary_data/bdry_park.shp")
mpls = gpd.read_file("../data/MSP/parks/Hennepin_County_Parks-shp/Hennepin_County_Parks.shp")

sp.loc[:, 'geometry'].plot(ax=ax)
mpls.loc[:, 'geometry'].plot(ax=ax)

plt.show()
