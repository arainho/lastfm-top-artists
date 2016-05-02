import sqlite3

'''
Connect to Last.fm SQLite database,
and read the fields 'artist' and 'playcounts' from table TopArtists
'''
conn = sqlite3.connect("db/lastfm.sqlite")
conn.text_factory = str
cur = conn.cursor()
cur.execute('''SELECT artist, playcount FROM TopArtists''')


'''
 Create a dictionary with artists and playcount's
'''
play_counts = dict()
for message_row in cur:
    artist_name = message_row[0]
    if artist_name.find(':') is not -1 or artist_name.find('('):
        offset = artist_name.find(':')
        artist_name = artist_name[:offset]
    play_counts[artist_name] = message_row[1]


'''
 Find the top 100 artists
'''
artists = sorted(play_counts, key=play_counts.get, reverse=True)
highest = None
lowest = None
for a in artists[:100]:
    print a
    if highest is None or highest < play_counts[a]:
        highest = play_counts[a]
    if lowest is None or lowest > play_counts[a]:
        lowest = play_counts[a]
print 'Range of counts:',highest,lowest


'''
 Spread the font sizes across 20-100 based on the count
'''
bigsize = 80
smallsize = 20

fhand = open('js/artist.name.js','w')
fhand.write("artist_name = [")
first = True

'''
Write artists to javascript file
'''
for artist in artists[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = play_counts[artist]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: \"" + artist + "\", size: " + str(size) + "}")
fhand.write( "\n];\n")

print "Output written to artist.name.js"
print "Open artist_name.html in a browser to view"
