import os
import glob
import shutil
import callgrasp as GRASP


def dfh_grd(elements_Zlist, number_of_CPUs):
    # Calculation for ground state
    for n in range(2, 6):
        # create input file and generate angular data
        # copy csf list as input file
        shutil.copyfile('./grd'+str(n)+'.c', 'rcsf.inp')
        #  Get angular data
        GRASP.rangular(mpi_cores=number_of_CPUs)

        for z in elements_Zlist:
            # go to Z specific directory
            os.chdir('Z'+str(z))

            # clean directory and import files from main directory
            GRASP.clean_files()
            shutil.copyfile('../rcsf.inp', 'rcsf.inp')
            for ang_file in glob.glob(r'../mcp.*'):
                shutil.copy(ang_file, '.')

            # Get initial estimates of wave functions
            GRASP.rwfnestimate(init_guess=2, inputFile="grd"+str(n-1)+".w")

            # Perform self-consistent field calculations (save log)
            GRASP.rmcdhf(1,
                         orbitals=str(n)+"*",
                         spectroscopic_orbitals='',
                         output_log="outgrd_rmcdhf_"+str(n)
                         )

            GRASP.rsave('grd'+str(n))
            print('Done')

            os.chdir('..')


def dfh_exc(elements_Zlist, number_of_CPUs):
    # Calculation for excited state
    for n in range(2, 7):
        # create input file and generate angular data
        # copy csf list as input file
        shutil.copyfile('./exc'+str(n)+'.c', 'rcsf.inp')
        #  Get angular data
        GRASP.rangular(mpi_cores=number_of_CPUs)

        for z in elements_Zlist:
            # go to Z specific directory
            os.chdir('Z'+str(z))
            # copy input file from parent directory
            GRASP.clean_files()
            shutil.copyfile('../rcsf.inp', 'rcsf.inp')
            for ang_file in glob.glob(r'../mcp.*'):
                shutil.copy(ang_file, '.')

            # Get initial estimates of wave functions
            GRASP.rwfnestimate(init_guess=2, inputFile="exc"+str(n-1)+".w")

            # Perform self-consistent field calculations (save log)
            ASF = [[1], [1, 2]]
            weights = [5, 5]

            GRASP.rmcdhf(ASF,
                         weights,
                         orbitals=str(n)+"*",
                         spectroscopic_orbitals='',
                         output_log="outexc_rmcdhf_"+str(n)
                         )

            GRASP.rsave('exc'+str(n))
            print('Done')

            # back to test directory
            os.chdir('..')


if __name__ == "__main__":
    # set environmental variables
    GRASP.setENV()
    # go to working directory
    os.chdir('test')

    cores = 1
    z_list = [2, 10, 74]

    # dfh_grd(z_list, cores)

    dfh_exc(z_list, cores)

    # back to mian directory
    os.chdir('..')

