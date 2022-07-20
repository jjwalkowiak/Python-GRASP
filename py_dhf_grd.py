import os
import subprocess
import shutil

# set environmental variables
if not 'set_ENV_flag' in globals():
    import set_ENV

# go to working directory
os.chdir('..')

for n in (2, 3, 4, 5):
    for z in (2, 10, 74):
        # go to Z specific directory
        os.chdir('Z'+str(z))
        # copy csf list as input file
        shutil.copyfile('../grd'+str(n)+'.c', 'rcsf.inp')

        #  Get angular data (MPI version)
        # subprocess.run(['mpirun', '-np', '8', 'rangular_mpi'],
        #                input="y\n",
        #                encoding="utf-8")

        subprocess.run(['rangular'],
                       input="y\n",
                       encoding="utf-8")

        # Get initial estimates of wave functions
        subprocess.run(['rwfnestimate'],
                       input="y\n1\ngrd"+str(n-1)+".w\n*\n2\n*\n",
                       encoding="utf-8")

        # Perform self-consistent field calculations (save log)
        with open("outgrd_rmcdhf_"+str(n),'w') as output:
            subprocess.run(['rmcdhf'],
                           input="y\n1\n"+str(n)+"*\n\n100\n",
                           stdout=output,
                           encoding="utf-8")

        subprocess.run(['rsave', 'grd'+str(n)])
        print('done')

        os.chdir('..')

# back to the Python scripts directory
os.chdir('./Python')