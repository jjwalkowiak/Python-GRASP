#!/usr/bin/env python3
#
# COMMANDS TO POST-PROCESS GRASP RESULTS
# --------
#
#
# J. Walkowiak
# 09.2022
# #################################################################################
import dataclasses
import os
import re
import callgrasp as GRASP


def load_transitions(filename1, filename2=None):

    transition_list = list()

    if filename2 is None:
        filename = filename1
    else:
        filename = filename1 + '.' + filename2 + '.ct'

# Define dataclass for transition data
    State = dataclasses.make_dataclass("State", [('File', str), ('Lev', int), ('J', int), ('Parity', str)])
    Transition_Properties = dataclasses.make_dataclass(
        "Properties", [('Gauge', str), ('A_s1', float), ('gf', float), ('S', float)])
    Transition = dataclasses.make_dataclass(
                        "Transition", [
                                        ('Upper', State),
                                        ('Lower', State),
                                        ('E_Kays', float),
                                        ('Coulomb', Transition_Properties),
                                        ('Babushkin', Transition_Properties)])

    pattern = re.compile('f1|f2')
    re_number = re.compile('\S+')

    saveFlag = False  # This is just for saving second line

    if os.path.exists(filename):
        with open(filename) as file:
            for i in range(3): next(file)  # Skip 3 lines
            for line in (file.readlines()):
                if saveFlag:
                    data = re.findall(re_number, line)
                    data4 = Transition_Properties(Gauge=data[0],
                                                  A_s1=float(data[1].replace('D', 'E')),
                                                  gf=float(data[2].replace('D', 'E')),
                                                  S=float(data[3].replace('D', 'E')))
                    transition_list.append(Transition(Upper=data1, Lower=data2, E_Kays=Energy, Coulomb=data3, Babushkin=data4))
                    # print(data)
                    saveFlag = False

                elif re.search(pattern, line) is not None:
                    data = re.findall(re_number, line)
                    data1 = State(File=data[0], Lev=int(data[1]), J=int(data[2]), Parity=data[3])
                    data2 = State(File=data[4], Lev=int(data[5]), J=int(data[6]), Parity=data[7])
                    Energy = float(data[8])
                    data3 = Transition_Properties(Gauge=data[9],
                                                  A_s1=float(data[10].replace('D', 'E')),
                                                  gf=float(data[11].replace('D', 'E')),
                                                  S=float(data[12].replace('D', 'E')))
                    saveFlag = True

    else:
        print(filename + " don't exist")

    return transition_list


if __name__ == "__main__":
    # set environmental variables
    GRASP.setENV()
    # go to working directory
    os.chdir('test')

    list_of_transitions = load_transitions('trans38')
    properties_list = [[T.E_Kays, T.Coulomb.gf, T.Babushkin.gf] for T in list_of_transitions]
    #print(*load_transitions('grd5', 'exc5'), sep='\n')
    print(*properties_list, sep='\n')

    os.chdir('..')
