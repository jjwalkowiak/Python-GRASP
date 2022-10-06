import os
import callgrasp as GRASP

# set environmental variables
GRASP.setENV()
# go to working directory
os.chdir('test')

z_list = [2, 10, 74]

for z in z_list:
    # go to Z specific directory
    os.chdir('Z'+str(z))

    GRASP.rbiotransform('grd5', 'exc5', output_log='out_rbiotransform')

    GRASP.rtransition('grd5', 'exc5', 'E1', output_log='out_transition')

    # back to test directory
    os.chdir('..')

os.chdir('..')

