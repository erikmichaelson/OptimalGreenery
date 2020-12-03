import geopandas as gpd
import pandas as pd
from collections import Counter
from shapely.geometry import Point
import rasterio as rio
import random as rnd
import matplotlib.pyplot as plt

def genPoints(num, mask_adr):
	mask = gpd.read_file('../data/MSP/mask/CountyMask.shp')
	bnds = mask['geometry'].total_bounds
	print(bnds)
	
	points = []
	for k in range(num):
		while(1):
			base0 = rnd.randrange(int(bnds[0]), int(bnds[2]))
			base1 = rnd.randrange(int(bnds[1]), int(bnds[3]))
			base = (base0, base1)
			pt = Point(base)
			poly = mask['geometry'].values[0]
		#	print(pt, poly)
			if(pt.within(poly)):
				break
			print('outside the TC')
		points.append(base)

	return points



def avgGrndCover(points):
	rast = rio.open('../data/MSP/trees/tcma_clip.tif', masked=False)

	bnds = rast.bounds

	band1 = rast.read(1)
	print(band1)
	gridpoints = []
	results = []

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
			gridpoints.append(point)
			results.append(output)

	print(len(gridpoints))
	
	Points = [Point(p) for p in gridpoints]
	geoPts = gpd.GeoSeries(Points)

	print(geoPts)
	geoPts.columns=['geometry']
	geoPts.to_file('points.shp')

	print(Counter(results))

if __name__ == '__main__':
	mask = '~/Documents/AdvEconometrics/ResearchProject/code/data/MSP/mask/CountyMask.shp'
	points = genPoints(10, mask)
