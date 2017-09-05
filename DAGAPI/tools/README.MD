#DAG makfile
- This common script used as a PRE script before every node in DAG.
- The script can automatically pause or active a node in DAG when a part of input data or executable_file are updated.

### Rule:
```python
if a OP node:
    if all input_sandbox files exist:
        if all output_sandbox files exist:
            if the all output files are created lately than all input files:
                turn into NOOP
            else:
                no change # new input
        else:
            no change  # lack output
    else：
        turn into NOOP
if a NOOP node:
    if all input—sandbox files exist:
        if all output files exist:
            if all output files created lately than all input files:
                no change  #no new input
            else:
                turn into OP