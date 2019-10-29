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


def is_number(val):
    """Check if input string is a number"""
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_number_in_range(val, check):
    """Check if number is in range"""
    if(check == "offset"):
        if ((int(val) >= -32768) and (int(val) <= 32767)):
            return True
        else:
            print("Error: offset out of range")
            exit(1)
    elif(check == "reg"):
        if((int(val) >= 0) and (int(val) <= 7)):
            return True
        else:
            print("Error: register number out of range")
            exit(1)


def is_label_defined(key):
    """Check if label is defined"""
    if key in _label:
        return True
    else:
        print("Error: label undefine")
        exit(1)


def twos_comp(val, bits):
    """compute the 2's complement of int for negative decimal to binary bits"""
    val = val - (1 << bits)         # compute negative value
    return -val                     # return positive value


def writeData(data):  # write data to output.txt
    f = open("machineCode.txt", "a")
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
        if(lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq' or lineSplit[1] == 'add' or lineSplit[1] == 'nand' or lineSplit[1] == 'jalr' or lineSplit[1] == 'halt' or lineSplit[1] == 'noop' or lineSplit[1] == '.fill'):
            if(lineSplit[1] == 'beq'):
                opcode = '100'
                # Check if field is Number
                if is_number(lineSplit[2]):
                    if is_number_in_range(lineSplit[2], "reg"):
                        field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    if is_label_defined(lineSplit[2]):
                        field0 = decimal_to_binary(
                            int(_label[lineSplit[2]]), 3)
                if is_number(lineSplit[3]):
                    if is_number_in_range(lineSplit[3], "reg"):
                        field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    if is_label_defined(lineSplit[3]):
                        field1 = decimal_to_binary(
                            int(_label[lineSplit[3]]), 3)
                if is_number(lineSplit[4]):
                    if is_number_in_range(lineSplit[4], "offset"):
                        field2 = decimal_to_binary(int(lineSplit[4]), 16)
                else:
                    if is_label_defined(lineSplit[4]):
                        if int(_label[lineSplit[4]]) >= pc:
                            field2 = decimal_to_binary(
                                int(_label[lineSplit[4]] - pc - 1), 16)
                        else:                                                # If branch backward use 2's complement
                            field2 = int(
                                twos_comp(int(pc - _label[lineSplit[4]] + 1), 16))
                            field2 = decimal_to_binary(field2, 16)

            elif(lineSplit[1] == 'lw' or lineSplit[1] == 'sw'):
                if(lineSplit[1] == 'lw'):
                    opcode = '010'
                elif(lineSplit[1] == 'sw'):
                    opcode = '011'

                if is_number(lineSplit[2]):
                    if is_number_in_range(lineSplit[2], "reg"):
                        field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    if is_label_defined(lineSplit[2]):
                        field0 = decimal_to_binary(
                            int(_label[lineSplit[2]]), 3)
                if is_number(lineSplit[3]):
                    if is_number_in_range(lineSplit[3], "reg"):
                        field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    if is_label_defined(lineSplit[3]):
                        field1 = decimal_to_binary(
                            int(_label[lineSplit[3]]), 3)
                if is_number(lineSplit[4]):
                    if is_number_in_range(lineSplit[4], "offset"):
                        field2 = decimal_to_binary(int(lineSplit[4]), 16)
                else:
                    if is_label_defined(lineSplit[4]):
                        field2 = decimal_to_binary(
                            int(_label[lineSplit[4]]), 16)

            elif(lineSplit[1] == 'add' or lineSplit[1] == 'nand'):
                if(lineSplit[1] == 'add'):
                    opcode = '000'
                elif(lineSplit[1] == 'nand'):
                    opcode = '001'

                if is_number(lineSplit[2]):
                    if is_number_in_range(lineSplit[2], "reg"):
                        field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    if is_label_defined(lineSplit[2]):
                        field0 = decimal_to_binary(
                            int(_label[lineSplit[2]]), 3)
                if is_number(lineSplit[3]):
                    if is_number_in_range(lineSplit[3], "reg"):
                        field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    if is_label_defined(lineSplit[3]):
                        field1 = decimal_to_binary(
                            int(_label[lineSplit[3]]), 3)
                if is_number(lineSplit[4]):
                    if is_number_in_range(lineSplit[4], "reg"):
                        field2 = decimal_to_binary(int(lineSplit[4]), 3)
                else:
                    if is_label_defined(lineSplit[4]):
                        field2 = decimal_to_binary(
                            int(_label[lineSplit[4]]), 3)

            elif(lineSplit[1] == 'jalr'):
                opcode = '101'
                if is_number(lineSplit[2]):
                    if is_number_in_range(lineSplit[2], "reg"):
                        field0 = decimal_to_binary(int(lineSplit[2]), 3)
                else:
                    if is_label_defined(lineSplit[2]):
                        field0 = decimal_to_binary(
                            int(_label[lineSplit[2]]), 3)
                if is_number(lineSplit[3]):
                    if is_number_in_range(lineSplit[3], "reg"):
                        field1 = decimal_to_binary(int(lineSplit[3]), 3)
                else:
                    if is_label_defined(lineSplit[3]):
                        field1 = decimal_to_binary(
                            int(_label[lineSplit[3]]), 3)

            elif(lineSplit[1] == 'halt' or lineSplit[1] == 'noop'):
                if(lineSplit[1] == 'halt'):
                    opcode = '110'
                elif(lineSplit[1] == 'noop'):
                    opcode = '111'

            elif(lineSplit[1] == '.fill'):
                opcode = lineSplit[2].replace('\n', '')
                if is_number(lineSplit[2]):
                    pass
                else:
                    if is_label_defined(opcode):
                        opcode = _label[opcode]
        else:
            print("Error : Undifined instruction")
            exit(1)

        if(lineSplit[1] == 'add' or lineSplit[1] == 'nand'):
            machineCode = binary_to_decimal(
                bit31_25 + opcode + field0 + field1 + bit15_3 + field2)
            print(machineCode)
        elif(lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq'):
            machineCode = binary_to_decimal(
                bit31_25 + opcode + field0 + field1 + field2)
            print(machineCode)
        elif(lineSplit[1] == 'jalr'):
            machineCode = binary_to_decimal(
                bit31_25 + opcode + field0 + field1 + bit15_0)
            print(machineCode)
        elif(lineSplit[1] == 'halt' or lineSplit[1] == 'noop'):
            machineCode = binary_to_decimal(bit31_25 + opcode + bit21_0)
            print(machineCode)
        elif(lineSplit[1] == '.fill'):
            machineCode = int(opcode)
            print(machineCode)
        writeData(str(machineCode))  # write machine code to output.txt
        pc += 1
    inFile.close()


try:
    # receive machine argument from command line ex. python ASMtoMachine.py in.txt
    inFilePath = sys.argv[1]
except :
    print("please insert input file ex. python ASMtoMachine.py in.txt")
    exit(1)
inFileParse()
