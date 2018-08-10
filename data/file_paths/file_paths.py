# defines important file paths

import os

# project location
project = '/Users/rmiparks/git/IMAGE/'

# data from knmi for brazil analysis
minas_knmi_climate_data = os.path.join(project, 'data/knmi/rcp85/')
minas_knmi_climate_output = os.path.join(project, 'output/')
minas_real_climate_data = os.path.join(project,'data/minas_brazil/')

# el nino data from knmi
knmi_elnino = os.path.join(project, 'data/knmi/elnino/')

# IMAGE output data
image_output_local = os.path.join('/Users/rmiparks/data/IMAGE/CLaGARMi/euro_cordex_output/')
cordex_output_local = os.path.join('/Users/rmiparks/data/IMAGE/CORDEX/')

