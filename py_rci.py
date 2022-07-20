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

    # RCI calculations for ground5
    with open("outgrd_rci",'w') as output:
        subprocess.run(['rci'],
                       input="y\ngrd5\ny\ny\n1.d-6\ny\nn\nn\ny\n1\n1\n",
                       stdout=output,
                       encoding="utf-8")

    # RCI calculations for excited8
    with open("outexc_rci",'w') as output:
        subprocess.run(['rci'],
                       input="y\nexc8\ny\ny\n1.d-6\ny\nn\nn\ny\n1\n1-7\n1-14\n",
                       stdout=output,
                       encoding="utf-8")

    os.chdir('..')

# back to the Python scripts directory
os.chdir('./Python')