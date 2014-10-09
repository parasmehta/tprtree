'''
Created on Oct 8, 2014

@author: paras
'''

import index
import core
import ctypes

class TPRTree(index.Index):
    '''
    classdocs
    '''

    def __init__(self,  *args, **kwargs):
        '''
        Constructor
        '''
        index.Index.__init__(self,  *args, **kwargs)
                
#    def getIndex(self):
#        if self.idx is None:
#            self.idx = TPRTree()
#        return self.idx
    
    
    def insert(self, id, coordinates, velocities, tstart, tend, obj = None):
        core.rt.Index_InsertTPData.argtypes = [ctypes.c_void_p, 
                                ctypes.c_int64, 
                                ctypes.POINTER(ctypes.c_double), 
                                ctypes.POINTER(ctypes.c_double), 
                                ctypes.POINTER(ctypes.c_double), 
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_double,
                                ctypes.c_double, 
                                ctypes.c_uint32, 
                                ctypes.POINTER(ctypes.c_ubyte), 
                                ctypes.c_uint32]
        core.rt.Index_InsertData.restype = ctypes.c_int
        core.rt.Index_InsertData.errcheck = core.check_return
        
        p_mins, p_maxs = self.get_coordinate_pointers(coordinates)
        v_mins, v_maxs = self.get_coordinate_pointers(velocities)
        data = ctypes.c_ubyte(0)
        size = 0
        pyserialized = None
        if obj is not None:
            size, data, pyserialized = self._serialize(obj)
        core.rt.Index_InsertTPData(self.handle, id, p_mins, p_maxs, v_mins, v_maxs, tstart, tend, self.properties.dimension, data, size)
        
    
    
    def count(self, coordinates, velocities, tstart, tend):     
        core.rt.Index_TPIntersects_count.argtypes = [  ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.c_double,
                                        ctypes.c_double,
                                        ctypes.c_uint32,
                                        ctypes.POINTER(ctypes.c_uint64)]
        
        p_mins, p_maxs = self.get_coordinate_pointers(coordinates)
        v_mins, v_maxs = self.get_coordinate_pointers(velocities)
        p_num_results = ctypes.c_uint64(0)


        core.rt.Index_TPIntersects_count(self.handle,
                                        p_mins,
                                        p_maxs,
                                        v_mins,
                                        v_maxs,
                                        tstart,
                                        tend,
                                        self.properties.dimension,
                                        ctypes.byref(p_num_results))


        return p_num_results.value
    
    
    
    def intersection(self, coordinates, velocities, tstart, tend, objects=False):
        if objects: return self._intersection_obj(coordinates, velocities, tstart, tend, objects)

        core.rt.Index_TPIntersects_id.argtypes = [ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_double), 
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.c_double,
                                        ctypes.c_double,                                     
                                        ctypes.c_uint32, 
                                        ctypes.POINTER(ctypes.POINTER(ctypes.c_int64)),
                                        ctypes.POINTER(ctypes.c_uint64)]
        
        core.rt.Index_Intersects_id.restype = ctypes.c_int
        core.rt.Index_Intersects_id.errcheck = core.check_return
        
        p_mins, p_maxs = self.get_coordinate_pointers(coordinates)
        v_mins, v_maxs = self.get_coordinate_pointers(velocities)
        
        p_num_results = ctypes.c_uint64(0)

        it = ctypes.pointer(ctypes.c_int64())

        core.rt.Index_TPIntersects_id(self.handle,
                                        p_mins,
                                        p_maxs,
                                        v_mins,
                                        v_maxs,
                                        tstart,
                                        tend,
                                        self.properties.dimension,
                                        ctypes.byref(it),
                                        ctypes.byref(p_num_results))
        return self._get_ids(it, p_num_results.value)
    
    
    
    def _intersection_obj(self, coordinates, velocities, tstart, tend, objects):
        # Index_TPIntersects_obj(  IndexH index,
#                    double* pdMin,
#                    double* pdMax,
#                   double* pdVMin,
#                    double* pdVMax,
#                    double tStart,
#                    double tEnd,
#                    uint32_t nDimension,
#                    IndexItemH** items,
#                    uint64_t* nResults)

        core.rt.Index_TPIntersects_obj.argtypes = [ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_double), 
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_double),
                                        ctypes.c_double,
                                        ctypes.c_double,                                     
                                        ctypes.c_uint32,
                                        ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)),
                                        ctypes.POINTER(ctypes.c_uint64)]
        core.rt.Index_TPIntersects_obj.restype = ctypes.c_int
        core.rt.Index_TPIntersects_obj.errcheck = core.check_return
        
        p_mins, p_maxs = self.get_coordinate_pointers(coordinates)
        v_mins, v_maxs = self.get_coordinate_pointers(velocities)
        
        p_num_results = ctypes.c_uint64(0)

        it = ctypes.pointer(ctypes.c_void_p())

        core.rt.Index_TPIntersects_obj(self.handle,
                                        p_mins,
                                        p_maxs,
                                        v_mins,
                                        v_maxs,
                                        tstart,
                                        tend,
                                        self.properties.dimension,
                                        ctypes.byref(it),
                                        ctypes.byref(p_num_results))
        return self._get_objects(it, p_num_results.value, objects)
        