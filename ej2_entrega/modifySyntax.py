#!/usr/bin/env python3

# imports
import re


# TO DO: add argument functionality to script for the following variables
inv_synt_filename = 'testcase.v'
val_synt_filename = 'expected.v'
mem_filename = "memdump.mem"

# Regular expression for invalid syntax
inv_synt_re = re.compile('  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')
#inv_synt_re = re.compile('  reg \[(?P<first_part>.*)\] (?P<second_part>\S*) \[(?P<third_part>.*)\];\n  initial begin\n(?P<men_part>(?P<memory_part>    \S*\[\S*\] = \S*;\n)*)  end\n')

def create_mem_file(mem_data,mem_filename):
    ### Inputs
    ###     mem_data: string
    ###     mem_count: int
    ###     mem_filename: string
    ###
    ### Creates a file named mem_filename with data from  mem_data
    pass

def main(inv_synt_filename, val_synt_filename, mem_filename, re=None):
    ### Inputs
    ###     inv_synt_filename: string - filename of verilog file with invalid syntax
    ###     val_synt_filename: string - filename of verilog file with valid syntax
    ###     mem_filename: string - filename of memory file where initialization data is sent
    ###     re: regular expression - regular expression according to invalid syntax


    #Open original file with invalid syntax and match re
    with open(inv_synt_filename, 'r') as inv_synt_f:
        inv_synt_filedata = inv_synt_f.read()
        match = inv_synt_re.search(inv_synt_filedata)
        match_start, match_end = match.span()

        with open(val_synt_filename, 'w') as val_synt_f:
            val_synt_f.write(inv_synt_filedata[0:match_start])
            val_synt_f.write("  reg [" + match.group(1) + "] " + match.group(2) + " [" + match.group(3) + "]\n")
            val_synt_f.write("  $readmemh(\""+ mem_filename + "\", " + match.group(2) + ")\n")
            val_synt_f.write(inv_synt_filedata[match_end:])

    create_mem_file(match.group(4),mem_filename)

if __name__ == '__main__':
    main(inv_synt_filename, val_synt_filename, mem_filename, inv_synt_re)
