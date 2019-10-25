import fileinput
import sys
inFilePath = ''
_label = {}
# with fileinput.input(files=('in.txt')) as f:

# mapLabel to _label["Key"] = "Value"


def map_label():
    inFile = open(inFilePath, 'r')
    lineCount = 0
    for line in inFile:
        lineSplit = line.split("    ")
        if lineSplit[0] != '':                  # if line have label
            _label[lineSplit[0]] = lineCount    # map label with current PC
        lineCount += 1
    inFile.close()


def binary_to_decimal(str_val):     # convert binary string to decimal
    """convert binary string to decimal"""
    result = 0
    base = 1
    binary_len = len(str_val)
    for i in range(binary_len - 1, -1, -1):
        if(str_val[i] == "1"):
            result += base
        base *= 2
    return result                   # return int


def decimal_to_binary(val, bits):    # convert decimal int to binary string
    """convert decimal int to binary string"""
    result = ""
    for i in range(bits-1, -1, -1):
        j = val >> i
        if(j & 1):
            result += "1"
        else:
            result += "0"
    return result                   # return string


def twos_comp(val, bits):
    """compute the 2's complement of int"""
    val = val - (1 << bits)         # compute negative value
    return -val                     # return positive value


def writeData(data):  # write data to output.txt
    f = open("output.txt", "a")
    f.write(data + "\n")
    f.close()


def inFileParse():
    map_label()
    bit31_25 = '0000000'            # Set Unused Bits to 0
    bit21_0 = '0000000000000000000000'
    bit15_3 = '0000000000000'
    bit15_0 = '0000000000000000'
    pc = 0                          # Initial PC = 0
    inFile = open(inFilePath, 'r')  # Open file for Read ('r')
    for line in inFile:             # Read line
        # Split field to Array lineSplit[idx]
        lineSplit = line.split("    ")
        if(lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq' or lineSplit[1] == 'add' or lineSplit[1] == 'nand'):
            if(lineSplit[1] == 'beq'):
                opcode = '100'
                # Check if field is Number
                if lineSplit[2].isnumeric():
                    # Format Number in field0 to Binary length 3 bits ({0:03b})
                    field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    field0 = decimal_to_binary(int(_label[lineSplit[2]]), 3)
                if lineSplit[3].isnumeric():
                    field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    field1 = decimal_to_binary(int(_label[lineSplit[3]]), 3)

                if lineSplit[4].isnumeric():
                    field2 = decimal_to_binary(int(lineSplit[4]), 16)
                else:
                    if(int(_label[lineSplit[4]]) >= pc):
                        field2 = decimal_to_binary(
                            int(_label[lineSplit[4]]), 16)
                    else:                                                # If branch backward use 2's complement
                        field2 = int(
                            twos_comp(int(_label[lineSplit[4]] + 1), 16))
                        field2 = decimal_to_binary(field2, 16)

            elif(lineSplit[1] == 'lw' or lineSplit[1] == 'sw'):
                if(lineSplit[1] == 'lw'):
                    opcode = '010'
                elif(lineSplit[1] == 'sw'):
                    opcode = '011'

                if lineSplit[2].isnumeric():
                    field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    field0 = decimal_to_binary(int(_label[lineSplit[2]]), 3)
                if lineSplit[3].isnumeric():
                    field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    field1 = decimal_to_binary(int(_label[lineSplit[3]]), 3)
                if lineSplit[4].isnumeric():
                    field2 = decimal_to_binary(int(lineSplit[4]), 16)
                else:
                    field2 = decimal_to_binary(int(_label[lineSplit[4]]), 16)

            elif(lineSplit[1] == 'add'):
                opcode = '000'
                if lineSplit[2].isnumeric():
                    field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    field0 = decimal_to_binary(int(_label[lineSplit[2]]), 3)
                if lineSplit[3].isnumeric():
                    field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    field1 = decimal_to_binary(int(_label[lineSplit[3]]), 3)
                if lineSplit[4].isnumeric():
                    field2 = decimal_to_binary(int(lineSplit[4]), 3)
                else:
                    field2 = decimal_to_binary(int(_label[lineSplit[4]]), 3)

            elif(lineSplit[1] == 'nand'):
                opcode = '001'
                if lineSplit[2].isnumeric():
                    field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    field0 = decimal_to_binary(int(_label[lineSplit[2]]), 3)
                if lineSplit[3].isnumeric():
                    field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    field1 = decimal_to_binary(int(_label[lineSplit[3]]), 3)
                if lineSplit[4].isnumeric():
                    field2 = decimal_to_binary(int(lineSplit[4]), 3)
                else:
                    field2 = decimal_to_binary(int(_label[lineSplit[4]]), 3)

            if(lineSplit[1] == 'add' or lineSplit[1] == 'nand'):
                machineCode = binary_to_decimal(
                    bit31_25 + opcode + field0 + field1 + bit15_3 + field2)
                print(machineCode)

            elif(lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq'):
                machineCode = binary_to_decimal(
                    bit31_25 + opcode + field0 + field1 + field2)
                print(machineCode)

            writeData(str(machineCode))  # write machine code to output.txt
        pc += 1
    inFile.close()


# receive machine argument from command line ex. python ASMtoMachine.py in.txt
inFilePath = sys.argv[1]
inFileParse()
