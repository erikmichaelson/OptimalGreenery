import geopandas as gpd
import pandas as pd
from collections import Counter
from shapely.geometry import Point
import rasterio as rio
import random as rnd
import matplotlib.pyplot as plt

def genPoints(num, mask_adr):
	"""
  	Generate random points inside of a given region 

	Uses python's random functions and shapely's Point object
	to find random points that lie within a shapefile mask.

    Parameters
    ----------
    num : int
        the number of points to generate
    mask_adr : str
        address to a shapefile where the first geometry will be used as a mask

    Returns
    -------
    [(int, int)]
        a list of points (int, int) tuples

    """
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

	for p in points:
		assert bnds[0] <= base0 <= bnds[2]
		assert bnds[1] <= base1 <= bnds[3]

	savePointsToFile(points, 'points')

	return points



def avgGrndCover(points, rast_adr):
	rast = rio.open('../data/MSP/trees/tcma_clip.tif', masked=False)

	bnds = rast.bounds
	print(bnds)

	band1 = rast.read(1)
	print(band1)
	gridpoints = []
	toReturn = []
	
	print(bnds[2]-bnds[0], len(band1[0]))
	print(bnds[3]-bnds[1], len(band1))

	enum = [i for i in range(1,13)]
	print(enum)

	for p in points:
		base0 = p[0]
		base1 = p[1]
		print(p)
		assert bnds[0] <= base0 <= bnds[2]
		assert bnds[1] <= base1 <= bnds[3]
		results = []
		for i in range(30):
			gridpoint0 = base0 - bnds[0] - i*10 + 150 
			for j in range(30):
				gridpoint1 = base1 - bnds[1] - j*10 + 150
				a = int(gridpoint0)
				b = int(gridpoint1)
				output = band1[b][a]
				gridpoint = (gridpoint0+bnds[0], gridpoint1+bnds[1])
				gridpoints.append(gridpoint)
				results.append(output)
		cover = Counter(results)
		print(cover)
		toReturn.append(cover)

	#savePointsToFile(gridpoints, 'grids')

	rast.close()

	print(len(toReturn))
	assert len(toReturn) == len(points)

	return toReturn
	

def savePointsToFile(array, filename):
	print('here')
	Points = [Point(p) for p in array]
	geoPts = gpd.GeoSeries(Points)
	print(geoPts)
	geoPts.columns=['geometry']
	geoPts.to_file(filename+ '.shp')

if __name__ == '__main__':
	mask = '~/Documents/AdvEconometrics/ResearchProject/code/data/MSP/mask/CountyMask.shp'
	points = genPoints(10, mask)
	groundCover = avgGrndCover(points, 'PASS')
