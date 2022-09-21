import os
import glob
import shutil
import callgrasp as GRASP

# set environmental variables
GRASP.setENV()
# go to working directory
os.chdir('test')

# Calculation for ground state
##############################################
# create input file and generate angular data
# copy csf list as input file
shutil.copyfile('./grd1.c', 'rcsf.inp')
#  Get angular data
GRASP.rangular()

for z in (2, 10, 74):
    # go to Z specific directory
    os.chdir('Z'+str(z))
    # clean directory and import files from main directory
    GRASP.clean_files()
    shutil.copyfile('../rcsf.inp', 'rcsf.inp')
    for ang_file in glob.glob(r'../mcp.*'):
        shutil.copy(ang_file, '.')

    # Get initial estimates of wave functions
    GRASP.rwfnestimate(init_guess=2, subshells='*')

    # Perform self-consistent field calculations (save log)
    GRASP.rmcdhf(1, output_log='outgrd_rmcdhf')

    GRASP.rsave('grd1')
    print('done')

    # back to test directory
    os.chdir('..')

# Calculation for excited state
##############################################
# create input file and generate angular data
# copy csf list as input file
shutil.copyfile('./exc1.c', 'rcsf.inp')
#  Get angular data
GRASP.rangular()

for z in (2, 10, 74):
    # go to Z specific directory
    os.chdir('Z'+str(z))
    # copy input file from parent directory
    GRASP.clean_files()
    shutil.copyfile('../rcsf.inp', 'rcsf.inp')
    for ang_file in glob.glob(r'../mcp.*'):
        shutil.copy(ang_file, '.')

    # Get initial estimates of wave functions
    GRASP.rwfnestimate(init_guess=2, subshells='*')

    # Perform self-consistent field calculations (save log)
    ASF = [[1], [1, 2]]
    weights = [5, 5]
    GRASP.rmcdhf(ASF, weights, output_log='outexc_rmcdhf')

    GRASP.rsave('exc1')
    print('done')

    # back to test directory
    os.chdir('..')
# back to mian directory
os.chdir('..')
