import requests
from concurrent.futures import ThreadPoolExecutor
import geopandas as gpd
import pandas as pd

key = 'b9ff9c9d59bd6d7ed76973dc6b5859cc644a46e6'
url = 'https://api.census.gov/data/2018/acs/acs5'

def blockDataAtCoords(points, threaded):
	
	blockfile = gpd.read_file('../data/MSP/census/block/tl_2019_27_bg.shp')
	print(blockfile.crs)
	geoPts = points.set_crs('epsg:26915')
	geoPts = geoPts.to_crs(blockfile.crs)
	print(geoPts.crs)
	blocks = gpd.sjoin(geoPts, blockfile, how='left', op='intersects')
	blocks['FID'] = blocks.index
	#print(blocks['FID'])
	state = blocks['STATEFP']
	county = blocks['COUNTYFP']
	tract = blocks['TRACTCE']
	group = blocks['BLKGRPCE']
	loc = zip(blocks['FID'], state, county, tract, group)
	#print(loc)

	#print(blocks)
	og = 'https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:2&in=state:01%20county:025%20tract:957602&key='+key

	results = []
	#blocks['blockpop'] = 0
	#blocks['avgAge'] = 0.0

	if(threaded==True):
		denials = 0
		with ThreadPoolExecutor(max_workers=50) as executor:
			for l in executor.map(queryAPI, blocks['FID'], state, county, tract, group):
				#print(l)
				if(l == None): 
					denials += 1
				else:
					blocks.at[l[0], 'blockpop'] = int(l[1])
					blocks.at[l[0],  'avgAge' ] = float(l[2])
			print(denials)

	else:
		for i in range(10):
			step = int(len(state)/100)
			for j in range(i*step,i*step+step):
				l = queryAPI(blocks.at[j, 'FID'], state[j], county[j], tract[j], group[j])
				blocks.at[l[0], 'blockpop'] = int(l[1])
				blocks.at[l[0],  'avgAge' ] = float(l[2])

	return blocks


def queryAPI(FID, state, county, tract, blockgroup):
	j = FID
	print(j, state, county, tract, blockgroup)
	loc = 'state:',state,' county:',county,' tract:',tract
	bgroup = 'block group:'+blockgroup
	#print(bgroup)
	payload = {'get':'B01003_001E,B01002_001E', 'for':bgroup, 'in':loc, 'key':key}
	full='https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:*&in=state:27%20county:053&key='+key
	try:
		r = requests.get(url, params=payload)
		fjk = pd.read_json(r.text, orient='records')
		row = fjk.iloc[1]
	except requests.exceptions.ConnectionError:
		requests.status_code = "Connection refused"
		return None

	return j, row[0], row[1]


if __name__ == '__main__':
	Points = gpd.read_file('Points.shp')
	blocks0 = blockDataAtCoords(Points, True)
	print(blocks0)
	blocks1 = blockDataAtCoords(Points, False)
	print(blocks1)

	for b0, b1 in zip(blocks0, blocks1):
		assert b0[-1] == b1[-1]
		assert b0[-2] == b1[-2]
