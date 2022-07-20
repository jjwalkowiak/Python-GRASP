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

    #  First the biorthogonal transformations
    with open("out_rbiotransform",'w') as output:
        subprocess.run(['rbiotransform'],
                       input="y\ny\ngrd5\nexc8\ny\n",
                       stdout=output,
                       encoding="utf-8",
                       check=True)

    # Then the transition calculations
    with open("out_transition",'w') as output:
        subprocess.run(['rtransition'],
                       input="y\ny\ngrd5\nexc8\nE1\n",
                       stdout=output,
                       encoding="utf-8",
                       check=True)

    os.chdir('..')

# back to the Python scripts directory
os.chdir('./Python')