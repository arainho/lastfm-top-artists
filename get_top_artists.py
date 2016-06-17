import requests
import pprint
import json
import sqlite3

'''
 Import my settings
'''
settings = dict()
with open("config/settings.json") as f:
    settings = json.load(f)

user = settings["USER"]
api_key = settings["API_KEY"]
api_url = settings["API_ROOT_URL"]
json_url = api_url + '?' + 'method=user.gettopartists&user=' + user + '&api_key=' + api_key + '&format=json'


'''
 Let's do the request to last.fm
'''
params = {'period': "overall", 'limit': 100, 'page': 1}
r = requests.get(json_url,params=params)


'''
 Check response code
'''
print(r.status_code)


'''
 Check the json output
'''
my_data=r.json()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(my_data)


'''
 Create or open a 'sqlite' file
'''
conn = sqlite3.connect("./db/lastfm.sqlite")
cur = conn.cursor()


'''
 Drop table TopArtists
'''
cur.execute('''DROP TABLE IF EXISTS TopArtists''')
conn.commit()


'''
 Create last.fm database
'''
cur.execute('''CREATE TABLE IF NOT EXISTS TopArtists
          (id INTEGER  PRIMARY KEY, artist TEXT UNIQUE, playcount INTEGER, url TEXT)''')


'''
 Iterate over "my_data" to get artist, playcount and url
'''
for topartists in my_data:
  for artist, value in my_data[topartists].iteritems():
    my_list = my_data[topartists][artist]
    for my_dict in my_list:
        if isinstance(my_dict, dict):
            # print the values
            #print my_dict['@attr']['rank'], my_dict['name'], my_dict['playcount'], my_dict['url']

            # Insert values to Database 'lastfm.sqlite'
            cur.execute('INSERT OR IGNORE INTO TopArtists (id, artist, playcount, url) VALUES (?, ?, ?,?)', (my_dict['@attr']['rank'], my_dict['name'], my_dict['playcount'], my_dict['url']))
            conn.commit()

'''
 Close DB Connection
'''
conn.close()



