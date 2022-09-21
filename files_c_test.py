import os
import callgrasp as GRASP

GRASP.setENV()

# go to working directory
os.chdir('test')

# remove all generated files
GRASP.clean_all_files(['grd', 'exc'])

#  1.  Generate grasp2K expansions
#      1.1 for ground state

# reference CSF
con = ['1s(2,i)']
act = ['1s']
lJ = 0
hJ = 0
excitations = 0
GRASP.rcsfgenerate(con, act, lJ, hJ, excitations, 'grd1.c')

# expansion CSF
con = ['1s(2,*)']
act = ['5s', '5p', '5d', '5f', '5g']
lJ = 0
hJ = 0
excitations = 2
GRASP.rcsfgenerate(con, act, lJ, hJ, excitations, 'grd.c')

# split grd by layers
flabels = ['2', '3', '4', '5']
orbitals = [['2s', '2p'],
            ['3s', '3p', '3d'],
            ['4s', '4p', '4d', '4f'],
            ['5s', '5p', '5d', '5f', '5g']]
GRASP.rcsfsplit('grd', flabels, orbitals)
##########################################

#  2.  Generate grasp2K expansions
#      2.1 for excited states

# reference CSF
con = ['1s(1,i)2p(1,i)']
act = ['2s', '2p']
lJ = 0
hJ = 2
excitations = 0
GRASP.rcsfgenerate(con, act, lJ, hJ, excitations, 'exc1.c')

# expansion CSF
con = ['1s(1,*)2p(1,*)']
act = ['8s', '8p', '8d', '8f', '8g']
lJ = 0
hJ = 2
excitations = 2
GRASP.rcsfgenerate(con, act, lJ, hJ, excitations, 'exc.c')

# split grd by layers
flabels = ['2','3','4','5','6','7','8']
orbitals = [['2s','2p'],
            ['3s','3p','3d'],
            ['4s','4p','4d','4f'],
            ['5s','5p','5d','5f','5g'],
            ['6s','6p','6d','6f','6g'],
            ['7s','7p','7d','7f','7g'],
            ['8s','8p','8d','8f','8g']]
GRASP.rcsfsplit('exc',flabels,orbitals)

# back to the Python scripts directory
os.chdir('..')
