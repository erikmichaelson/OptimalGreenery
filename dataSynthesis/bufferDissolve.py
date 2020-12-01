import geopandas as gpd
def bufferDissolve(gdf, distance, join_style=3):	
	'''Create buffer and dissolve thoese intersects.
	
	Parameters:
		gdf: 
			Type: geopandas.GeoDataFrame
		distance: radius of the buffer
			Type: float
	Returns:
		gdf_bf: buffered and dissolved GeoDataFrame
			Type: geopandas.GeoDataFrame
	'''
	#create buffer and dissolve by invoking `unary_union`
	smp = gdf.buffer(distance, join_style).unary_union
	#convert to GeoSeries and explode to single polygons
	gs = gpd.GeoSeries([smp]).explode()
	#convert to GeoDataFrame
	gdf_bf = gpd.GeoDataFrame(geometry=gs, crs=gdf.crs).reset_index(drop=True)
	return gdf_bf
