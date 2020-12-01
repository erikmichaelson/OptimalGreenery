import geopandas as gpd
from collections import Counter
from shapely.geometry import Point
import rasterio as rio
import subprocess
import random as rnd
import matplotlib.pyplot as plt

rast = rio.open('../data/MSP/trees/tcma_clip.tif', masked=False)
mask = gpd.read_file('../data/MSP/CountyMask.shp')

bnds = rast.bounds
center = ((bnds[0]+bnds[2])/2 , (bnds[1]+bnds[3])/2)

band1 = rast.read(1)
print(band1)
points = []
results = []

for k in range(300):
	while(1):
		base0 = rnd.randrange(0, len(band1))
		base1 = rnd.randrange(0, len(band1[0]))
		base = (base0+bnds[0], base1+bnds[1])
		pt = Point(base)
		poly = mask['geometry'].values[0]
	#	print(pt, poly)
		if(pt.within(poly)):
			break
		print('outside the TC')


	for i in range(30):
		'''
		point0 = rnd.randrange(base[0]-100, base[0]+100, 2)
		point1 = rnd.randrange(base[1]-100, base[1]+100, 2)
		'''
		point0 = base0 - i*10 + 150
		for j in range(30):
			point1 = base1 - j*10 + 150
			'''
			cmd=f'rio sample tcma_clip.tif [{str(point0)},{str(point1)}]'
			process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			'''
			output = band1[point0, point1]
			point = (point0+bnds[0], point1+bnds[1])
			#print(point)
			points.append(point)
			results.append(output)

	print(len(points))
	
#fig, ax = plt.subplots()
#mask.loc[:, 'geometry'].plot(ax=ax)

Points = [Point(p) for p in points]
geoPts = gpd.GeoSeries(Points)

print(geoPts)
geoPts.columns=['geometry']
geoPts.to_file('points.shp')

#points0 = zip(*points)
#ax.scatter(*zip(points0), color='red')

#plt.show()
print(Counter(results))
