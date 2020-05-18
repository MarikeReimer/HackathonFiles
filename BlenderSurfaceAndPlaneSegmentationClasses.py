from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec, NWBAttributeSpec, NWBDatasetSpec
from pynwb import register_class, get_class, load_namespaces
from hdmf.utils import docval, call_docval_func, getargs, get_docval
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb import NWBHDF5IO
from pynwb.file import MultiContainerInterface, NWBContainer
from pynwb.spec import NWBDatasetSpec
import numpy as np
import pynwb
from pynwb.ophys import TwoPhotonSeries, OpticalChannel, ImageSegmentation, Fluorescence
from pynwb.device import Device

#Blender surfaces (Directly repurposed from CorticalSurfaces)
 
name = 'BlenderClasses'
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"
ns_builder = NWBNamespaceBuilder('Extension for use in my Lab', "TanLab", version='0.1.0')

blender_surface = NWBGroupSpec(doc='mesh body from Blender',
                       datasets=[
                           NWBDatasetSpec(doc='faces for surface, indexes vertices', shape=(None, 3),
                                          name='faces', dtype='uint', dims=('face_number', 'vertex_index')),
                           NWBDatasetSpec(doc='vertices for surface, points in 3D space', shape=(None, 3),
                                          name='vertices', dtype='float', dims=('vertex_number', 'xyz'))],
                       neurodata_type_def='BlenderSurface',
                       neurodata_type_inc='NWBDataInterface')

# @register_class('blender_surface', name)
# class BlenderSurface(NWBContainer):
#     __nwbfields__ = (
#         'faces',
#         'verticies'
#         )

#     @docval({'name': 'name', 'type': str, 'doc': 'name of this BlenderSurface'},
#             {'name': 'faces', 'type': ('array_data', 'data'),'doc': 'faces for this surface', 'default': None}, 
#             {'name': 'vertices', 'type': ('array_data', 'data'),'doc': 'faces for this surface', 'default': None})
           
#     def __init__(self, **kwargs):
#         call_docval_func(super((BlenderSurface, self).__init__, kwargs))
#         self.faces = getargs('faces', kwargs)
#         self.vertices = getargs('vertices', kwargs)

#ns_builder.add_spec(ext_source, blender_surface)



blender_plane_segmentation = NWBGroupSpec('A plane to store data from blender',
                            neurodata_type_inc='PlaneSegmentation',
                            neurodata_type_def='BlenderPlaneSegmentation',
                            groups = [blender_surface])

ns_builder.add_spec(ext_source, blender_plane_segmentation)

                            
#Writes YAML files
ns_builder.export(ns_path)
