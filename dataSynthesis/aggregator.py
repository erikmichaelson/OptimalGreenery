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
	mask = gpd.read_file(mask_adr)
	bnds = mask['geometry'].total_bounds
	
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
	rast = rio.open(rast_adr, masked=False)

	bnds = rast.bounds

	band1 = rast.read(1)
	gridpoints = []
	toReturn = []
	

	for p in points:
		base0 = p[0]
		base1 = p[1]
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
		covCounter = Counter(results)
		cover = []
		for i in range(12):
			cover.append((i+1, covCounter[i+1]))
		toReturn.append(cover)

	rast.close()

	assert len(toReturn) == len(points)

	return toReturn
	

def savePointsToFile(array, filename):
	Points = [Point(p) for p in array]
	geoPts = gpd.GeoSeries(Points)
	geoPts.columns=['geometry']
	geoPts.to_file(filename+ '.shp')




if __name__ == '__main__':
	basePath = '../data/MSP/'
	mask = 'mask/CountyMask.shp'
	tcma = 'trees/tcma_clip.tif'
	park = 'parks/DistFromPark.tif'
	enum = { 
		1:	'Grass/Shrub',
		2:	'Bare Soil',
		3:	'Buildings',
		4:	'Roads/Paved Surfaces',
		5:	'Lakes/Ponds',
		6:	'Deciduous Tree Canopy',
		7:	'Coniferous Tree Canopy',
		8:	'Agriculture',
		9:	'Emergent Wetland',
		10:	'Forested/Shrub Wetland',
		11:	'River',
		12:	'Extraction'	}

	points = genPoints(10, basePath+mask)
	groundCover = avgGrndCover(points, basePath+tcma)

	test = [[t[1] for t in row] for row in groundCover]
	print(test)

	pointsAndCover = zip(points, test)
	print(pointsAndCover)
	df = pd.DataFrame.from_records(pointsAndCover)
	print(df)
