#############
############
##########
########################
# Submit description file for mathematica
########################
executable = mathematica.sh
universe = vanilla
#input = test.data,  abde.data, a_$(Process)
output = test.out
error = test.error
log = test.log
transfer_input_files   =  8788.abc, uim.data

transfer_output_files  = t.py, test.py


noop_job=True
noop_job=True
queue    5