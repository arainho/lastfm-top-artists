# lastfm-top-artists
Genrerate a word cloud of Last.fm top 100 Artists

### Create and Fill config/settings.json
Copy settings.json.sample to settings.json

```sh
cp -v config/settings.json.sample config/settings.json
```

Fill the values of your _lastfm_ 'USER' and 'API_KEY' in the json file.
```sh
vi config/settings.json
```

### Run get_top_artists script
```sh
python get_top_artists.py
```

### Run artist_name script to create an htm file
```sh
python artists_name.py
```

### Open artist_name file in a Browser
```sh
open artist_name.html
```

