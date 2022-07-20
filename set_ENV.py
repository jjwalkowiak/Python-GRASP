import os

os.environ["PATH"] = os.environ["HOME"] + "/grasp/grasp-2018-12-03/bin:" + os.environ["PATH"]
os.environ["PATH"] = os.environ["HOME"] + "/opt.openmpi/bin:" + os.environ["PATH"]
os.environ["LD_LIBRARY_PATH"] = "LD_LIBRARY_PATH:" + os.environ["HOME"] + "/opt.openmpi/lib"
os.environ["MPI_TMP"] = os.environ["HOME"] + "/temp/MPI"

set_ENV_flag = True
