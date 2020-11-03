import shapefile as shp
import matplotlib.pyplot as plt

listx=[]
listy=[]
sf = shp.Reader("../data/MSP/parks/shp_bdry_admin_boundary_data/bdry_park.shp")

plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y, color="green", fillstyle="full")
plt.show()
