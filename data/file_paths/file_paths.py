# defines important file paths

import os
import sys

# file loc in case its being run on linux platform
if sys.platform == 'linux' or sys.platform == 'linux2':
    root_loc = '/home/rmp15/'
elif sys.platform == 'darwin':
    root_loc = '/Users/rmiparks/'


# project location
project = os.path.join(root_loc, 'git/IMAGE/')

# data from knmi for brazil analysis
minas_knmi_climate_data = os.path.join(project, 'data/knmi/rcp85/')
minas_knmi_climate_output = os.path.join(project, 'output/')
minas_real_climate_data = os.path.join(project, 'data/minas_brazil/')

# shapefile of europe
shapefile_europe = os.path.join(project, 'data/shapefiles/Europe/')

# el nino data from knmi
knmi_elnino = os.path.join(project, 'data/knmi/elnino/')

# IMAGE output location
image_output_local = os.path.join(root_loc, 'data/IMAGE/CLaGARMi/euro_cordex_output/')
cordex_output_local = os.path.join(root_loc, 'data/IMAGE/CORDEX/')


