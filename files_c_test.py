import os
import subprocess
import shutil
import callgrasp as GRASP

GRASP.setENV()

# go to working directory
os.chdir('test')

# remove all generated files
subprocess.run(['sh', './clean'])

#  1.  Generate grasp2K expansions
#      1.1 for ground state

# reference CSF
con = ['1s(2,i)']
act = ['1s']
lJ = 0
hJ = 0
GRASP.rcsfgenerate(con, act, lJ, hJ, 0, 'grd1.c')

# expansion CSF
con = ['1s(2,*)']
act = ['5s','5p','5d','5f','5g']
lJ = 0
hJ = 0
excitations = 2
GRASP.rcsfgenerate(con, act, lJ, hJ, excitations, 'grd.c')

# split grd by layers
flabels = ['2','3','4','5']
orbitals = [['2s','2p'],
            ['3s','3p','3d'],
            ['4s','4p','4d','4f'],
            ['5s','5p','5d','5f','5g']]
GRASP.rcsfsplit('grd',flabels,orbitals)
##########################################
if False:
#  2.  Generate grasp2K expansions
#      2.1 for excited states

    # reference CSF
    subprocess.run(['rcsfgenerate'],
                   input="*\n0\n1s(1,i)2p(1,i)\n\n2s,2p\n0,2\n0\nn\n",
                   encoding="utf-8")
    # copy output to destination file
    shutil.copyfile('rcsf.out', 'exc1.c')

    # expansion CSF
    subprocess.run(['rcsfgenerate'],
                   input="*\n0\n1s(1,*)2p(1,*)\n\n8s,8p,8d,8f,8g\n0,2\n2\nn\n",
                   encoding="utf-8")
    # copy output to destination file
    shutil.copyfile('rcsf.out', 'exc.c')

    # split grd by layers
    subprocess.run(['rcsfsplit'],
                   input=("exc\n7\n2s,2p\n2\n3s,3p,3d\n3\n4s,4p,4d,4f\n4\n5s,5p,5d,5f,5g\n5\n"
                          "6s,6p,6d,6f,6g\n6\n7s,7p,7d,7f,7g\n7\n8s,8p,8d,8f,8g\n8\n"),
                   encoding="utf-8")

    # back to the Python scripts directory
    os.chdir('..')