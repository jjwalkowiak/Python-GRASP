import os
import subprocess
import shutil

# set environmental variables
if not 'set_ENV_flag' in globals():
    import set_ENV

# go to working directory
os.chdir('..')

for z in (2, 10, 74):
    # go to Z specific directory
    os.chdir('Z'+str(z))
    # copy csf list as input file
    shutil.copyfile('../grd1.c', 'rcsf.inp')

    #  Get angular data
    subprocess.run(['rangular'],
                   input="y\n",
                   encoding="utf-8")

    # Get initial estimates of wave functions
    subprocess.run(['rwfnestimate'],
                   input="y\n2\n*\n",
                   encoding="utf-8")

    # Perform self-consistent field calculations (save log)
    with open("outgrd_rmcdhf",'w') as output:
        subprocess.run(['rmcdhf'],
                       input="y\n1\n*\n*\n100\n",
                       stdout=output,
                       encoding="utf-8")

    subprocess.run(['rsave', 'grd1'])
    print('done')

    os.chdir('..')

# back to the Python scripts directory
os.chdir('./Python')