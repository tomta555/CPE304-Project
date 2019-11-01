import fileinput
import sys
inFilePath = ''
_state = {}
_machine_code = {}
opcode = {}
halt_pc = 0
num_Memory = 0


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
    max_len = 0
    len_A = len(format(regA, 'b'))
    len_B = len(format(regB, 'b'))

    if(len_A >= len_B):
        max_len = len_A
    else:
        max_len = len_B
    max_value = 0
    for i in range(max_len - 1, -1, -1):
        max_value += 1 << i

    return max_value - (regA & regB)


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


def get_reg_number(pc, AorBorDest):
    """return register number of regA or regB or destReg ex. get_reg_number(_state["pc"],"Dest")"""
    if AorBorDest == "A":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 10, 13))
    elif AorBorDest == "B":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 13, 16))
    elif AorBorDest == "Dest":
        return binary_to_decimal(get_bits(decimal_to_binary(_state["mem[ " + str(pc) + " ]"], 32), 29, 32))


def get_bits(binary, left, right):
    """return select bits [left:right] from binary ex. get_bits("100101",0,3) will return 100"""
    return binary[left:right]


def init_MEM_REG():
    """create initial value in memory and register"""
    inFile = open(inFilePath, 'r')
    i = 0
    lineCount = 0
    halt_passed = False
    _state["pc"] = 0

    while (i < 8):
        _state["reg[ " + str(i) + " ]"] = 0
        i += 1

    for line in inFile:
        _state["mem[ " + str(lineCount) + " ]"] = int(line.replace('\n', ''))
        _machine_code["line" + str(lineCount)] = int(line.replace('\n', ''))
        if not halt_passed:
            opcode["pc" + str(lineCount)] = get_bits(
                decimal_to_binary(int(line.replace('\n', '')), 32), 7, 10)
        if(line.replace('\n', '') == "25165824"):
            global halt_pc
            halt_pc = lineCount + 1
            halt_passed = True
        lineCount += 1
    global num_Memory
    num_Memory = lineCount

    inFile.close()


def print_state():
    """Print state and value in each memory and register"""
    print("@@@\nstate:\n\tpc " + str(_state["pc"])+"\n\tmemory:")
    for i in range(0, num_Memory, 1):
        print("\t\t" + "mem[ " + str(i) + " ] " +
              str(_state["mem[ " + str(i) + " ]"]))
    print("\tregisters:")
    for i in range(0, 8, 1):
        print("\t\t" + "reg[ " + str(i) + " ] " +
              str(_state["reg[ " + str(i) + " ]"]))
    print("end state\n\n")


def simulation():
    """Simulation each instruction behavior"""
    # เรียกใช้ pc ด้วย _state["pc"]
    # เรียกใช้ memory ด้วย _state["mem[ " + index + " ]"]  -> index ตั้งแต่ 0 ถึง num_Memory
    # เรียกใช้ register ด้วย _state["reg[ " + index + " ]"] -> index ตั้งแต่ 0 ถึง 7

    inst_count = 0
    while (_state["pc"] != halt_pc):
        inst_count += 1
        if(opcode["pc"+str(_state["pc"])] == "000"):  # add
            print("add")
            print_state()
            regA = get_reg_number(_state["pc"], "A")
            regB = get_reg_number(_state["pc"], "B")
            destReg = get_reg_number(_state["pc"], "Dest")
            _state["reg[ " + str(destReg) + " ]"] = _state["reg[ " + str(regA) + " ]"] + _state["reg[ " + str(regB) + " ]"]
            _state["pc"] += 1
        elif(opcode["pc"+str(_state["pc"])] == "001"):  # nand
            print("nand")
            print_state()
            regA = get_reg_number(_state["pc"], "A")
            regA_value = _state["reg[ " + str(regA) + " ]"]
            regB = get_reg_number(_state["pc"], "B")
            regB_value = _state["reg[ " + str(regB) + " ]"]
            destReg = get_reg_number(_state["pc"], "Dest")
            _state["reg[ " + str(destReg) + " ]"] = nand(regA_value,regB_value)
            _state["pc"] += 1
        elif(opcode["pc"+str(_state["pc"])] == "010"):  # lw
            print_state()
            offset = get_offset(_state["pc"])
            regA = get_reg_number(_state["pc"], "A")
            regA_value = _state["reg[ " + str(regA) + " ]"]
            regB = get_reg_number(_state["pc"], "B")
            _state["reg[ " + str(regB) + " ]"] = _state["mem[ " + str(regA_value + offset) + " ]"]
            _state["pc"] += 1
        elif(opcode["pc"+str(_state["pc"])] == "011"):  # sw
            print_state()
            offset = get_offset(_state["pc"])
            regA = get_reg_number(_state["pc"], "A")
            regA_value = _state["reg[ " + str(regA) + " ]"]
            regB = get_reg_number(_state["pc"], "B")
            regB_value = _state["reg[ " + str(regB) + " ]"]
            _state["mem[ " + str(regA_value+offset) + " ]"] = regB_value
            _state["pc"] += 1
        elif(opcode["pc"+str(_state["pc"])] == "100"):  # beq
            print("beq")
            print_state()
            branch = False
            offset = get_offset(_state["pc"])
            # do your code here
            if(branch):
                _state["pc"] += (1 + offset)
            else:
                _state["pc"] += 1
        elif(opcode["pc"+str(_state["pc"])] == "101"):  # jalr
            print_state()
            regA = get_reg_number(_state["pc"], "A") 
            regB = get_reg_number(_state["pc"], "B")
            if(regA == regB):
                _state["reg[ " + str(regB) + " ]"] = _state["pc"] + 1
                _state["pc"] += 1
            else:
                _state["reg[ " + str(regB) + " ]"] = _state["pc"] + 1
                _state["pc"] = _state["reg[ " + str(regA) + " ]"]
        elif(opcode["pc"+str(_state["pc"])] == "110"):  # halt
            print("halt")
            print_state()
            print("machine halted\ntotal of " + str(inst_count) +
                  " instructions executed\nfinal state of machine:\n")
            _state["pc"] += 1
            print_state()
        elif(opcode["pc"+str(_state["pc"])] == "111"):  # noop
            print_state()
            _state["pc"] += 1


try:
    # receive machine argument from command line ex. python Simulation.py machineCode.txt
    inFilePath = sys.argv[1]
except:
    print("please insert input file ex. python Simulation.py machineCode.txt")
    exit(1)
init_MEM_REG()
simulation()
