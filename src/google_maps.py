import urllib2
import json
import base64
import struct
import itertools
import matplotlib.pyplot as plt

def points_decode(points_str):
    coord_chunks = []
    num_chunk = []
    for c in points_str:        
        
        # convert the character to binary number
        val = ord(c) - 63
        
        # value with more chunks following will have 0x20
        more_chunks = val & 0x20        
        val &= 0x1F
        
        # append the current value to the num_chunk
        num_chunk.append(val)
        
        # if no more chunk follows, add the num_chunk to the list
        if not more_chunks:
            coord_chunks.append(num_chunk)
            num_chunk = []
            
    num_list = []
    
    for num_chunk in coord_chunks:
        val = 0
        
        # regenerate the value
        for x in reversed(num_chunk):
            val = (val << 5) | x
              
        # the sign bit is the first bit now
        if(val & 0x01):
            val = ~val
            
        # regenerate the original value
        val = val >> 1
        
        val /= 1.0e5
        num_list.append(val)
    
    points_list = []
    
    cur_x = 0
    cur_y = 0
    
    for i in xrange(0, len(num_list), 2):
        offset_x = num_list[i]
        offset_y = num_list[i+1]
        
        # if nothing changes, continue
        if offset_x == offset_y:
            continue
        
        cur_x += offset_x
        cur_y += offset_y
        
        # round to 6 digits, to be the same as what they are before encoded
        points_list.append((round(cur_x, 6), round(cur_y, 6)))
    
    return points_list

api_key = 'AIzaSyA_184La6d9B8IR4STZljUmYqcci6RLt50'
base_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={dest}&key={key}&alternatives=true'

url = base_url.format(origin='Pasadena', dest='LAX', key=api_key)
url = urllib2.quote(url, safe=':?&=/')

print url
try:
    usock = urllib2.urlopen(url)
    if 'application/json' in usock.info()['content-type']:  
        data_str = usock.read()
        
        with open("Pasadena2LAX.txt", 'w') as output_file:
            output_file.write(data_str)
            
        data = json.loads(data_str)
        print data
        routes = data['routes']
        route = routes[0]
        print len(routes)
#         for key, val in route.items():
#             print key, val
        print route['overview_polyline']
#         points = route['overview_polyline']['points'] + '='
# 
        points_raw = route['overview_polyline']['points']
        lon, lat = zip(*points_decode(points_raw))
        plt.plot(lat, lon, 'o')
        plt.show()
#         for x in points_decode(points_raw):
#             print x

except:
    raise