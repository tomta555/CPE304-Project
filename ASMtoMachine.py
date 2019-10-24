import fileinput
inFilePath = 'in.txt'
_label = {}
# with fileinput.input(files=('in.txt')) as f:

# mapLabel to _label["Key"] = "Value"
def mapLabel():
    inFile = open(inFilePath, 'r')
    lineCount = 0
    for line in inFile:
        lineSplit = line.split("    ")
        if lineSplit[0] != '':                  # if line have label
            _label[lineSplit[0]] = lineCount    # map label with current PC
        lineCount += 1
    inFile.close()


def twos_comp(val, bits):
    """compute the 2's complement of int"""
    val = val - (1 << bits)         # compute negative value
    return -val                     # return positive value


def inFileParse():
    mapLabel()
    bit31_25 = '0000000'            # Set Unused Bits to 0
    pc = 0                          # Initial PC = 0
    inFile = open(inFilePath, 'r')  # Open file for Read ('r')
    for line in inFile:             # Read line
        lineSplit = line.split("    ")      # Split field to Array lineSplit[idx]
        if(lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq'):
            if(lineSplit[1] == 'beq'):
                opcode = '100'
                if lineSplit[2].isnumeric():                            # Check if field is Number
                    field0 = "{0:03b}".format(int(lineSplit[2]))        # Format Number in field0 to Binary length 3 bits ({0:03b})
                else:
                    field0 = "{0:03b}".format(int(_label[lineSplit[2]]))
                if lineSplit[3].isnumeric():
                    field1 = "{0:03b}".format(int(lineSplit[3]))
                else:
                    field1 = "{0:03b}".format(int(_label[lineSplit[3]]))
                if lineSplit[4].isnumeric():
                    field2 = "{0:016b}".format(int(lineSplit[4]))
                else:
                    if(int(_label[lineSplit[4]]) >= pc):
                        field2 = "{0:03b}".format(int(_label[lineSplit[4]]))
                    else:                                                # If branch backward use 2's complement 
                        field2 = int(
                            twos_comp(int(_label[lineSplit[4]] + 1), 16))
                        field2 = "{0:03b}".format(field2)

            elif(lineSplit[1] == 'lw' or lineSplit[1] == 'sw'):
                if(lineSplit[1] == 'lw'):
                    opcode = '010'
                elif(lineSplit[1] == 'sw'):
                    opcode = '011'

                if lineSplit[2].isnumeric():
                    field0 = "{0:03b}".format(int(lineSplit[2]))
                else:
                    field0 = "{0:03b}".format(int(_label[lineSplit[2]]))
                if lineSplit[3].isnumeric():
                    field1 = "{0:03b}".format(int(lineSplit[3]))
                else:
                    field1 = "{0:03b}".format(int(_label[lineSplit[3]]))
                if lineSplit[4].isnumeric():
                    field2 = "{0:016b}".format(int(lineSplit[4]))
                else:
                    field2 = "{0:03b}".format(int(_label[lineSplit[4]]))

            machineCode = int(bit31_25 + opcode + field0 + field1 + field2, 2)  # concat machineCode and cast to int
        print(machineCode)
        pc += 1


inFileParse()
