import requests

key = 'b9ff9c9d59bd6d7ed76973dc6b5859cc644a46e6'

mn = '024'
og = 'https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:2&in=state:01%20county:025%20tract:957602&key='+key

url = 'https://api.census.gov/data/2018/acs/acs5'
payload = {'get':'B00001_001E', 'for':'block group:2', 'key':key}
full='https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:*&in=state:27%20county:053&key='+key
print(full)
r = requests.get(full)

print(r.json)
print(r.text)
