#!/usr/bin/env python3
#
# COMMANDS TO RUN GRASP PROGRAMS
# --------
# This module contains definition of commands needed to call GRASP programs
# as subprocesses.
#
# J. Walkowiak
# 09.2022
# #################################################################################

import os
import subprocess
import shutil
import glob

def setENV(pathGRASP='/grasp/grasp-2018-12-03', pathOpenMPI='/opt.openmpi', pathMPI_TMP='/temp/MPI'):
    """
    Set environment variables necessary to run GRASP code
    :param pathGRASP: location of the GRASP installation starting from $HOME
    :param pathOpenMPI: location of the OpenMPI libraries starting from $HOME
    :param pathMPI_TMP: Temp location for MPI calculations starting from $HOME
    :return: 0
    """
    os.environ["PATH"] = os.environ["HOME"] + pathGRASP + "/bin:" + os.environ["PATH"]
    os.environ["PATH"] = os.environ["HOME"] + pathOpenMPI + "/bin:" + os.environ["PATH"]
    os.environ["LD_LIBRARY_PATH"] = "LD_LIBRARY_PATH:" + os.environ["HOME"] + pathOpenMPI + "/lib"
    os.environ["MPI_TMP"] = os.environ["HOME"] + pathMPI_TMP

    return 0

def rcsfgenerate(configurations, activeSet, lowJnumber, highJnumber, excitations, output, encoding="utf-8", ordering='*', core='0', printInput=False):
    """
    Run rcsfgenerate as subprocess and save output to file
    :param configurations: a list of reference configurations
    :param activeSet: a limit of active set given as a list of nl combination for every shell included
    :param lowJnumber: Resulting lower 2*J number
    :param highJnumber: Resulting higher 2*J number
    :param excitations: Number of excitations (if negative number e.g. -2, correlation orbitals will always be doubly occupied)
    :param output: name of the output file
    :param encoding: encoding for subprocesss, default utf-8
    :param ordering: Default, reverse, symmetry or user specified ordering? (*/r/s/u)
    :param core: Select core (default 0)
        0: No core
        1: He (       1s(2)                  =  2 electrons)
        2: Ne ([He] + 2s(2)2p(6)             = 10 electrons)
        3: Ar ([Ne] + 3s(2)3p(6)             = 18 electrons)
        4: Kr ([Ar] + 3d(10)4s(2)4p(6)       = 36 electrons)
        5: Xe ([Kr] + 4d(10)5s(2)5p(6)       = 54 electrons)
        6: Rn ([Xe] + 4f(14)5d(10)6s(2)6p(6) = 86 electrons)
    :return: 0
    """
    #Combine input
    inputC = ordering + '\n' + core + '\n'
    for conf in configurations:
        inputC += conf +'\n'
    inputC += '\n'
    inputC +=','.join(activeSet)
    inputC += '\n' + str(lowJnumber) + ',' + str(highJnumber) + '\n' + str(excitations) + '\nn\n'

    if printInput:
        print("Input to rcsfgenerate")
        print(inputC)

    #Run rcsfgenerate
    subprocess.run(['rcsfgenerate'],
                   input=inputC,
                   encoding=encoding)

    # copy output to destination file
    shutil.copyfile('rcsf.out', output)
    return 0

def rcsfsplit(input, fileLabels, orbitalSets, encoding="utf-8", printInput=False):
    """
    Run rcsfsplit subprocess
    :param input: name of the file to split
    :param fileLabels: labels which will be added to resulting files (output files -> input+fileLabel)
    :param orbitalSets: list of list of orbitals which will be used to split the input
    !WARNING! - fileLabels and orbitalSets should give the mase length
    :param encoding: encoding for subprocesss, default utf-8
    :param printInput: If True, input to subprocess will be printed (False by default)
    :return: 0
    """

    #Check input consistency
    if len(orbitalSets) == len(fileLabels):
        # Combine input
        inputC = input + '\n' + str(len(orbitalSets)) +'\n'
        for i, orbitalSet in enumerate(orbitalSets):
            inputC +=','.join(orbitalSet)
            inputC += '\n' + fileLabels[i] + '\n'

        if printInput:
            print("Input to rcsfsplit")
            print(inputC)

        # Run rcsfsplit
        subprocess.run(['rcsfsplit'],
                       input=inputC,
                       encoding=encoding)
        return 0
    else: return 1 #I should give here some warning, that input is wrong

def rnucleus(charge, mass_number=0, mass=0, nuc_spin=1, nuc_dipol_moment=1, nuc_quadrupole_moment=1, encoding="utf-8"):
    """
    Run rnucleus subprocess
    :param charge: charge of the nucleus
    :param mass_number: mass number (0 if the nucleus is to be modelled as a point source - default)
    :param mass: mass of the neutral atom (in amu) (0 if the nucleus is to be static - default)
    :param nuc_spin: nuclear spin quantum number (I) (in units of h / 2 pi) (1 to neglect - default)
    :param nuc_dipol_moment: nuclear dipole moment (in nuclear magnetons) (1 to neglect - default)
    :param nuc_quadrupole_moment: nuclear quadrupole moment (in barns) (1 to neglect - default)
    :param encoding: encoding for subprocesss, default utf-8
    :return: 0
    """
    inputC = str(charge) + '\n' + str(mass_number) + '\n'
    if mass_number > 0: inputC += 'n\n'
    inputC += str(mass) + '\n' + str(nuc_spin) + '\n' + str(nuc_dipol_moment) + '\n' + str(nuc_quadrupole_moment) + '\n'

    subprocess.run(['rnucleus'],
                   input=inputC,
                   encoding=encoding)
    return 0

def rangular(input="y\n", encoding="utf-8"):
    """
    Run rangular - calculate abgular part of the wave function
    :param input: input to subprocess, default setting uses default GRASP values
    :param encoding: encoding for subprocesss, default utf-8
    :return: 0
    """
    subprocess.run(['rangular'],
                   input=input,
                   encoding=encoding)
    return 0

def rwfnestimate(input, encoding="utf-8"):
    subprocess.run(['rwfnestimate'],
                   input=input,
                   encoding=encoding)
    return 0

def rmcdhf(input, output_log, encoding="utf-8"):
    subprocess.run(['rmcdhf'],
                   input=input,
                   stdout=output_log,
                   encoding=encoding)
    return 0

def rsave(output_file):
    """
    Run rsave - change name of the output files, so they will not be overwritten by the next calculations
    :param output_file: new name of the output files
    :return: 0
    """
    subprocess.run(['rsave', output_file])
    return 0

def clean_all_files(file_names=None):
    if file_names is None: file_names=[]
    """
    Look for files generated by GRASP and delete them
    :param file_names: list of file names which will be looked for and deleted (like shell rm name*)
    :return: 0
    """
    if not isinstance(file_names, list): var_1 = [file_names]
    file_names += ['trans', 'hfs', 'energy', 'rcsf']
    for name in file_names:
        name = name + '*'
        for file in glob.glob(name):
            os.remove(file)

    for file in glob.glob('*.m'):
        os.remove(file)

    for file in ["output", "excitationdata", "rcsfexcitation.log", "clist.new"]:
        if os.path.isfile(file): os.remove(file)

    for dir in glob.glob('Z*'):
        if os.path.isdir(dir):  shutil.rmtree(dir)
    return 0