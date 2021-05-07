#!/usr/bin/env python3

# imports
import re

def create_mem_file(mem_data, mem_filename):
    ### Creates a file named mem_filename with data from  mem_data
    ###
    ### Inputs
    ###     mem_data: string - inline memory initiation as a string separated by \n
    ###     mem_filename: string - output memory filename

    mem_re = re.compile('8\'h([\da-f]+)')
    with open(mem_filename, 'w') as mem_f:
        for line in mem_data.splitlines():
            mem_f.write(mem_re.search(line).group(1) + '\n')


def main(inv_synt_filename, val_synt_filename, mem_filename, re=None):
    ### Replaces verilog file with invalid syntax for another file with the correct(valid) syntax and creates a memory file with initialization values
    ###
    ### Inputs
    ###     inv_synt_filename: string - name of verilog file with invalid syntax
    ###     val_synt_filename: string - name of verilog file with valid syntax
    ###     mem_filename: string - name of memory file where initialization data is store
    ###     re: regular expression - regular expression according to invalid syntax


    #Open original file with invalid syntax and match re
    with open(inv_synt_filename, 'r') as inv_synt_f:
        inv_synt_filedata = inv_synt_f.read()
        match = inv_synt_re.search(inv_synt_filedata)
        match_start, match_end = match.span()

        # Writes new file with correct syntax
        with open(val_synt_filename, 'w') as val_synt_f:
            val_synt_f.write(inv_synt_filedata[0:match_start])
            val_synt_f.write("  reg [" + match.group(1) + "] " + match.group(2) + " [" + match.group(3) + "]\n")
            val_synt_f.write("  $readmemh(\""+ mem_filename + "\", " + match.group(2) + ")\n")
            val_synt_f.write(inv_synt_filedata[match_end:])

    # Creates new file where initialization memory values are stored
    create_mem_file(match.group(4), mem_filename)

if __name__ == '__main__':

    # TO DO: add argument functionality to script for the following variables
    inv_synt_filename = 'testcase.v'
    val_synt_filename = 'expected.v'
    mem_filename = "memdump.mem"

    # Regular expression for invalid syntax
    inv_synt_re = re.compile('  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')

    main(inv_synt_filename, val_synt_filename, mem_filename, inv_synt_re)
