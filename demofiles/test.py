#############
############
##########
########################
# Submit description file for mathematica
universe = vanilla
#input = test.data,  abde.data, a_$(Process)
output = test.out
error = test.error
log = test.log
transfer_input_files   =  a.input

transfer_output_files  =  b.output

queue    5


