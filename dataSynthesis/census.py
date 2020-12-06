import requests
import geopandas as gpd
import pandas as pd

def blockDataAtCoords(points):
	
	blockfile = gpd.read_file('../data/MSP/census/tl_2019_27_bg.shp')
	print(blockfile.crs)
	geoPts = points.set_crs('epsg:26915')
	geoPts = geoPts.to_crs(blockfile.crs)
	print(geoPts.crs)
	blocks = gpd.sjoin(geoPts, blockfile, how='left', op='intersects')
	state = blocks['STATEFP']
	county = blocks['COUNTYFP']
	tract = blocks['TRACTCE']
	group = blocks['BLKGRPCE']
	print(group)

	print(blocks)
	key = 'b9ff9c9d59bd6d7ed76973dc6b5859cc644a46e6'
	og = 'https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:2&in=state:01%20county:025%20tract:957602&key='+key

	url = 'https://api.census.gov/data/2018/acs/acs5'

	results = []
	toReturn = gpd.GeoDataFrame(columns=['geometry','B01003_001E','B01002_001E','state','county','tract','block group'])
	for i in range(100):
		step = int(len(state)/100)
		for j in range(i*step,i*step+step):
			print(j)
			loc = 'state:',state[j],' county:',county[j],' tract:',tract[j]
			bgroup = 'block group:'+group[j]
			#print(bgroup)
			payload = {'get':'B01003_001E,B01002_001E', 'for':bgroup, 'in':loc, 'key':key}
			full='https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:*&in=state:27%20county:053&key='+key
			r = requests.get(url, params=payload)
			fjk = pd.read_json(r.text, orient='records')
			row = fjk.iloc[1]
			print(row[0], row[1])

			blocks.at[j, 'blockpop'] = row[0]
			blocks.at[j,  'avgAge' ] = row[1]

		print(blocks)

	print(blocks)

	return toReturn



if __name__ == '__main__':
	Points = gpd.read_file('Points.shp')
	blocks = blockDataAtCoords(Points)
