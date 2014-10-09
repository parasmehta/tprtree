'''
Created on Oct 7, 2014

@author: paras
'''

import index
import ctypes
import tprtree


twodouble = ctypes.c_double * 2

teststreet = {
    "type": "Feature",
    "geometry": {
        "type":"MultiLineString",
        "coordinates":[[
            [1402528.63585071451962,7491973.552016104571521],
            [1402597.665066956076771,7491840.036925406195223]
        ]]
    },
    "properties": {
        "name": "Bla Bla Street",
        "oneway": "yes"
    },
    "crs": {
        "type":"link",
        "properties": {
            "http://spatialreference.org/ref/sr-org/6864/proj4/",
            "proj4"
        }
    }
}
 
# minimum bounding rectangle
#left, bottom, right, top = (
#    1402528.63585071, 
#    7491840.03692541, 
#    1402597.66506696, 
#    7491973.5520161)
    
if __name__ == '__main__':
    p = index.Property()
    p.set_dimension(2)
    p.set_index_type(index.RT_TPRTree)
    p.set_overwrite(True)    
    #idx = index.Index(properties = p)
    idx = tprtree.TPRTree(properties = p)
    #idx = tprtree.TPRTree.getIndex()
    print idx
    
    left, bottom, right, top = (0.0, -5.0, 0.0, -5.0)
    leftv, bottomv, rightv, topv = (0.0, 0.0, 0.0, 0.0)
    tstart, tend = 0, 10
    itemid = 1
    idx.insert(itemid, (left, bottom, right, top), (leftv, bottomv, rightv, topv), tstart, tend, None)
    
    itemid = 2
    tstart, tend = 0, 2
    idx.insert(itemid, (left, bottom, right, top), (leftv, bottomv, rightv, topv), tstart, tend, None)
    
    itemid = 3
    tstart, tend = 0, 10
    left, bottom, right, top = (-10.0, 5.0, -10.0, 5.0)
    leftv, bottomv, rightv, topv = (5.0, 0.0, 5.0, 0.0)    
    idx.insert(itemid, (left, bottom, right, top), (leftv, bottomv, rightv, topv), tstart, tend, None)
    
    itemid = 4
    idx.insert(itemid, (left, bottom, right, top), (leftv, bottomv, rightv, topv), tstart, tend, obj=teststreet)
    
    itemid = 2
    tstart, tend = 2, 10
    left, bottom, right, top = (5.0, 0.0, 5.0, 0.0)
    leftv, bottomv, rightv, topv = (5.0, 0.0, 5.0, 0.0)  
    idx.insert(itemid, (left, bottom, right, top), (leftv, bottomv, rightv, topv), tstart, tend, None)
    
    qleft, qbottom, qright, qtop = (0.0, 0.0, 10.0, 10.0)
    qleftv, qbottomv, qrightv, qtopv = (0.0, 0.0, 0.0, 0.0)
    qtstart, qtend = 2, 5
    intersect_count = idx.count((qleft, qbottom, qright, qtop), (qleftv, qbottomv, qrightv, qtopv), qtstart, qtend)
    print "Intersection count:", intersect_count
    
    ids_list = list(idx.intersection((qleft, qbottom, qright, qtop), (qleftv, qbottomv, qrightv, qtopv), qtstart, qtend))
    print ids_list
      