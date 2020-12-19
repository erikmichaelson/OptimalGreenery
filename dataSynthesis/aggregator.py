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
			if(pt.within(poly)):
				break
			print('outside the TC')
		points.append(base)

	for p in points:
		assert bnds[0] <= base0 <= bnds[2]
		assert bnds[1] <= base1 <= bnds[3]

	savePointsToFile(points, 'points')

	return points

def matchPolys(points, polys):
	"""
  	Selects polygons that intersect with points

	Uses python's random functions and shapely's Point object
	to find random points that lie within a shapefile mask.

    Parameters
    ----------
    points : GeoSeries
        the number of points to generate
    polys : GeoSeries
        address to a shapefile where the first geometry will be used as a mask

    Returns
    -------
    [(int, int)]
        a list of points (int, int) tuples

    """
	geopandas.sjoin(cities, countries, how="inner", op='intersects')



def rastValAtPoints(points, rast_adr):
	rast = rio.open(rast_adr, masked=False)

	bnds = rast.bounds

	band1 = rast.read(1)
	toReturn = []

	for p in points:
		assert bnds[0] <= p[0] <= bnds[2]
		assert bnds[1] <= p[1] <= bnds[3]

		x, y = ( p[0] , p[1] )
		row, col = rast.index(x, y)
		output = band1[row, col]

		'''
		a = p[0]-bnds[0]
		b = p[1]-bnds[1]
		print(a, b)
		output = band1[ p[0] ][ p[1] ]
		'''
		toReturn.append(output)

	rast.close()
	assert len(toReturn) == len(points)
	return toReturn



def avgGrndCover(points, rast_adr):
	rast = rio.open(rast_adr, masked=False)

	bnds = rast.bounds

	band1 = rast.read(1)
	range0 = len(band1)
	range1 = len(band1[0])
	gridpoints = []
	toReturn = []
	

	fails = 0
	for p in points:
		base0 = p[0]
		base1 = p[1]
		assert bnds[0] <= base0 <= bnds[2]
		assert bnds[1] <= base1 <= bnds[3]
		results = []
		for i in range(30):
			gridpoint0 = base0 - i*10 + 150 
			for j in range(30):
				gridpoint1 = base1 - j*10 + 150
				x, y = (gridpoint0, gridpoint1)
				row, col = rast.index(x, y)


				"""
				a = int(bnds[2]-gridpoint0)
				b = int(gridpoint1)
				"""
				if(row < range0 and col < range1):
					output = band1[row, col]
					gridpoint = (gridpoint0+bnds[0], gridpoint1+bnds[1])
					gridpoints.append(gridpoint)
					results.append(output)
				else:
					fails+=1;
		covCounter = Counter(results)
		cover = []
		for i in range(12):
			cover.append((i+1, covCounter[i+1]))
		toReturn.append(cover)

	print(str(fails/(900*len(points))) + '% of points fell outside bounds')

	rast.close()

	assert len(toReturn) == len(points)

	return toReturn
	

def savePointsToFile(array, filename):
	Points = [Point(p) for p in array]
	geoPts = gpd.GeoSeries(Points)
	geoPts.columns=['geometry']
	geoPts.to_file(filename+ '.shp')




