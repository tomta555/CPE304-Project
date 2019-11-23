import fileinput
import sys
inFilePath = ''
_state = {}
_machine_code = {}
opcode = {}
num_Memory = 0


def writeData(data):  # write data to output file
    f = open("PrintState.txt", "a")
    f.write(data + "\n")
    f.close()


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


def nand(regA, regB):
    """compute nand from value in regA and regB : input is decimal"""
    if regA < 0:
        bi_regA = "{0:b}".format(4294967296+regA)
    else:
        bi_regA = "{0:032b}".format(regA)
    if regB < 0:
        bi_regB = "{0:b}".format(4294967296+regB)
    else:
        bi_regB = "{0:032b}".format(regB)
    result_and = ""
    for i in range(0, len(bi_regA), 1):
        if bi_regA[i] == "1" and bi_regB[i] == "1":
            result_and += "1"
        else:
            result_and += "0"
    result = ""
    for i in range(0, len(result_and), 1):
        if result_and[i] == "0":
            result += "1"
        else:
            result += "0"
    count = 0
    for i in range(0, len(result), 1):
        if result[i] == "1":
            count += 1
    if count == len(result):
        return -1
    else:
        return twos_comp(int(result, 2), 32)


def twos_comp(val, bits):
    """compute the 2's complement of int"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set
        val = val - (1 << bits)         # compute negative value
    return val                          # return positive value


def get_offset(pc):
    """return offset"""
    offset = twos_comp(binary_to_decimal(
        get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 16, 32)), 16)
    return offset


def get_reg_number(pc, RegName):
    """return register number of regA or regB or destReg ex. get_reg_number(_state["pc"],"Dest")"""
    if RegName == "A":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 10, 13))
    elif RegName == "B":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 13, 16))
    elif RegName == "Dest":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 29, 32))


def get_bits(binary, left, right):
    """return select bits [left:right] from binary ex. get_bits("100101",0,3) will return 100"""
    return binary[left:right]


def init_MEM_REG():
    """create initial value in memory and register"""
    inFile = open(inFilePath, 'r')
    i = 0
    lineCount = 0
    _state["pc"] = 0

    while (i < 8):
        _state["reg[ " + str(i) + " ]"] = 0
        i += 1

    for line in inFile:
        _state["mem[ " + str(lineCount) + " ]"] = int(line.replace('\n', ''))
        _machine_code["line" + str(lineCount)] = int(line.replace('\n', ''))
        opcode["pc" + str(lineCount)] = get_bits(
            decimal_to_binary(int(line.replace('\n', '')), 32), 7, 10)
        lineCount += 1
    global num_Memory
    num_Memory = lineCount

    inFile.close()


def print_state():
    """Print state and value in each memory and register"""
    writeData("\n@@@\nstate:\n\tpc " + str(_state["pc"])+"\n\tmemory:")
    for i in range(0, num_Memory, 1):
        writeData("\t\t" + "mem[ " + str(i) + " ] " + str(_state["mem[ " + str(i) + " ]"]))
    writeData("\tregisters:")
    for i in range(0, 8, 1):
        writeData("\t\t" + "reg[ " + str(i) + " ] " + str(_state["reg[ " + str(i) + " ]"]))
    writeData("end state")


def simulation():
    """Simulation each instruction behavior"""
    inst_count = 0
    try:
        while (True):
            inst_count += 1
            if(opcode["pc"+str(_state["pc"])] == "000"):  # add
                print_state()
                regA = get_reg_number(_state["pc"], "A")
                regB = get_reg_number(_state["pc"], "B")
                destReg = get_reg_number(_state["pc"], "Dest")
                regA_value = _state["reg[ " + str(regA) + " ]"]
                regB_value = _state["reg[ " + str(regB) + " ]"]
                if(regA_value > 2147483648):
                    regA_value -= 2147483648
                if(regA_value < -2147483648):
                    regA_value += 2147483648
                if(regB_value > 2147483648):
                    regB_value -= 2147483648
                if(regB_value < -2147483648):
                    regB_value += 2147483648                
                if(regA_value == 2147483648 or regA_value == -2147483648):
                    result = -regA_value+regB_value
                elif(regB_value == 2147483648 or regB_value == -2147483648):
                    result = -regB_value+regA_value
                else:
                    result = regA_value+regB_value
                # destReg_value = regA_value + regB_value
                _state["reg[ " + str(destReg) + " ]"] = result
                _state["pc"] += 1
            elif(opcode["pc"+str(_state["pc"])] == "001"):  # nand
                print_state()
                regA = get_reg_number(_state["pc"], "A")
                regA_value = _state["reg[ " + str(regA) + " ]"]
                regB = get_reg_number(_state["pc"], "B")
                regB_value = _state["reg[ " + str(regB) + " ]"]
                destReg = get_reg_number(_state["pc"], "Dest")
                # destReg_value = ~(regA_value & regB_value)
                _state["reg[ " + str(destReg) +
                    " ]"] = nand(regA_value, regB_value)
                _state["pc"] += 1
            elif(opcode["pc"+str(_state["pc"])] == "010"):  # lw
                print_state()
                offset = get_offset(_state["pc"])
                regA = get_reg_number(_state["pc"], "A")
                regA_value = _state["reg[ " + str(regA) + " ]"]
                regB = get_reg_number(_state["pc"], "B")
                # regB_value = mem[regA_value + offset]
                _state["reg[ " + str(regB) + " ]"] = _state["mem[ " +
                                                            str(regA_value + offset) + " ]"]
                _state["pc"] += 1
            elif(opcode["pc"+str(_state["pc"])] == "011"):  # sw
                print_state()
                offset = get_offset(_state["pc"])
                regA = get_reg_number(_state["pc"], "A")
                regA_value = _state["reg[ " + str(regA) + " ]"]
                regB = get_reg_number(_state["pc"], "B")
                regB_value = _state["reg[ " + str(regB) + " ]"]
                # mem[regA_value + offset] = regB_value
                _state["mem[ " + str(regA_value+offset) + " ]"] = regB_value
                _state["pc"] += 1
            elif(opcode["pc"+str(_state["pc"])] == "100"):  # beq
                print_state()
                offset = get_offset(_state["pc"])
                regA = get_reg_number(_state["pc"], "A")
                regB = get_reg_number(_state["pc"], "B")
                # if regA_value = regB_value then Branch to pc + 1 + offset
                if(_state["reg[ " + str(regA) + " ]"] == _state["reg[ " + str(regB) + " ]"]):
                    _state["pc"] += (1 + offset)
                else:
                    _state["pc"] += 1
            elif(opcode["pc"+str(_state["pc"])] == "101"):  # jalr
                print_state()
                regA = get_reg_number(_state["pc"], "A")
                regB = get_reg_number(_state["pc"], "B")
                # if regA and regB is the same register then store pc + 1 to that reg and jump to pc + 1
                if(regA == regB):
                    _state["reg[ " + str(regB) + " ]"] = _state["pc"] + 1
                    _state["pc"] += 1
                # if regA and regB is not the same register then store pc + 1 to regB and jump to regA_value line  
                else:
                    _state["reg[ " + str(regB) + " ]"] = _state["pc"] + 1
                    _state["pc"] = _state["reg[ " + str(regA) + " ]"]
            elif(opcode["pc"+str(_state["pc"])] == "110"):  # halt
                print_state()
                writeData("machine halted\ntotal of " + str(inst_count) +
                        " instructions executed\nfinal state of machine:")
                _state["pc"] += 1
                print_state()
                break
            elif(opcode["pc"+str(_state["pc"])] == "111"):  # noop
                print_state()
                _state["pc"] += 1
    except KeyError:
        print("Error: Code=exit(1) Branch or Jump to non-exists line")
        exit(1)


try:
    # receive machine argument from command line ex. python Simulation.py machineCode.txt
    inFilePath = sys.argv[1]
except:
    print("Error: Code=exit(1) please insert input file ex. python Simulation.py machineCode.txt")
    exit(1)
try:
    init_MEM_REG()
except ValueError:
    print("Error:  Code=exit(1) input file is not machine code")
    exit(1)
simulation()
