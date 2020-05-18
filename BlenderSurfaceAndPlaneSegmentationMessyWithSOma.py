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
import open3d as o3d
import os

#Blender surfaces (Directly repurposed from CorticalSurfaces)
 
name = 'blenderbits'
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


load_namespaces('blenderbits.namespace.yaml')
BlenderSurface = get_class('BlenderSurface', 'TanLab')
BlenderPlaneSegmentation = get_class('BlenderPlaneSegmentation', 'TanLab')

#Read in OBJ
os.chdir('C:/Users/Mrika/OneDrive/TanLab/NWBHackathonFiles/HackthonFiles/ObjectModels')
soma_triangles = o3d.io.read_triangle_mesh("soma.obj")
soma_triangles = np.asarray(soma_triangles.triangles)



#Testing stuff
soma_surface = BlenderSurface(vertices=[[0.0, 1.0, 1.0],
                                             [1.0, 1.0, 2.0],
                                             [2.0, 2.0, 1.0],
                                             [2.0, 1.0, 1.0],
                                             [1.0, 2.0, 1.0]],
                                   faces= soma_triangles,
                                   name='soma')

nwbfile = NWBFile('my first synthetic recording', 'EXAMPLE_ID', datetime.now())

cortex_module = nwbfile.create_processing_module(name='cortex',
                                                 description='description')
cortex_module.add_container(soma_surface)

#Ophys tutorial
device = Device('imaging_device_1')
nwbfile.add_device(device)
optical_channel = OpticalChannel('my_optchan', 'description', 500.)
imaging_plane = nwbfile.create_imaging_plane('my_imgpln', optical_channel, 'a very interesting part of the brain',
                                             device, 600., 300., 'GFP', 'my favorite brain location',
                                             np.ones((5, 5, 3)), 4.0, 'manifold unit', 'A frame to refer to')
image_series = TwoPhotonSeries(name='test_iS', dimension=[2],
                               external_file=['images.tiff'], imaging_plane=imaging_plane,
                               starting_frame=[0], format='tiff', starting_time=0.0, rate=1.0)
nwbfile.add_acquisition(image_series)
mod = nwbfile.create_processing_module('ophys', 'contains optical physiology processed data')
img_seg = ImageSegmentation()
mod.add(img_seg)
ps = img_seg.create_plane_segmentation('output from segmenting my favorite imaging plane',
                                       imaging_plane, 'my_planeseg', image_series)
w, h = 3, 3
pix_mask1 = [(0, 0, 1.1), (1, 1, 1.2), (2, 2, 1.3)]
img_mask1 = [[0.0 for x in range(w)] for y in range(h)]
img_mask1[0][0] = 1.1
img_mask1[1][1] = 1.2
img_mask1[2][2] = 1.3
ps.add_roi(pixel_mask=pix_mask1, image_mask=img_mask1)

bob = pynwb.ophys.PlaneSegmentation('description', imaging_plane, name = "bob")                               

#Alas, I can't just tack stuff onto the plane segmentation
#ps.add_container(cortical_surface)

img_seg.add_plane_segmentation(bob)
bob.add_roi(pixel_mask=pix_mask1, image_mask=img_mask1)


duck = BlenderPlaneSegmentation('description', imaging_plane, name = "blender seg", blender_surface = soma_surface) 
duck.add_roi(pixel_mask=pix_mask1, image_mask=img_mask1)  
img_seg.add_plane_segmentation(duck)    

with NWBHDF5IO('bubtest2.nwb', 'w') as io:
    io.write(nwbfile)
