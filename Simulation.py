import fileinput
import sys
inFilePath = ''
_state = {}
_pc_oppcode = {}
_halt_pc = 0
_lastline = 0

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
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set
        val = val - (1 << bits)         # compute negative value
    return val                          # return positive value


def get_bits(decimal,left,right):
    """return select bits from decimal ex. get_bits("100101",0,3) will return 100"""
    binary = decimal_to_binary(decimal,32)
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
        _state["mem[ " + str(lineCount) + " ]"] = line.replace('\n', '')
        if not halt_passed:
            _pc_oppcode["pc"+ str(lineCount)] = get_bits(int(line.replace('\n', '')),7,10)
        if(line.replace('\n', '') == "25165824"):
            global _halt_pc
            _halt_pc = lineCount + 1  
            halt_passed = True
        lineCount += 1
    global _lastline
    _lastline = lineCount
        
    inFile.close()


def print_state():
    """Print state and value in each memory and register"""
    print("@@@\nstate:\n\tpc " + str(_state["pc"])+"\n\tmemory:")
    for i in range(0,_lastline,1):
        print("\t\t" + "mem[ " + str(i) + " ] " + _state["mem[ " + str(i) + " ]"])
    print("\tregisters:")
    for i in range(0,8,1):
        print("\t\t" + "reg[ " + str(i) + " ] " + str(_state["reg[ " + str(i) + " ]"]))
    print("end state\n\n")

def simulation():
    """Simulation each instruction behavior"""
    # เรียกใช้ pc ด้วย _state["pc"]
    # เรียกใช้ memory ด้วย _state["mem[ " + index + " ]"]  -> index ตั้งแต่ 0 ถึง _lastline
    # เรียกใช้ register ด้วย _state["reg[ " + index + " ]"] -> index ตั้งแต่ 0 ถึง 7
    
    inst_count = 0
    while (_state["pc"] != _halt_pc):
        inst_count += 1
        if(_pc_oppcode["pc"+str(_state["pc"])] == "000"): # add
            print("add")
            print_state()
            # do your code here 

            _state["pc"] += 1
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "001"): # nand
            print("nand")
            print_state()
            # do your code here
            
            _state["pc"] += 1
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "010"): # lw
            print("lw")
            print_state()
            # do your code here
           
            _state["pc"] += 1
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "011"): # sw
            print("sw")
            print_state()
            # do your code here

            _state["pc"] += 1
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "100"): # beq
            print("beq")
            branch = False
            offset = twos_comp(binary_to_decimal(get_bits(int(_state["mem[ "+ str(_state["pc"]) +" ]"]),16,32)),16)
            print_state()
            # do your code here
            
            if(branch):
                _state["pc"] += 1 + offset
            else:
                _state["pc"] += 1
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "101"): # jalr
            print("jalr")
            print_state()
            # do your code here
            
            # _state["pc"] = regA
            _state["pc"] += 1 # dummy
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "110"): # halt
            print("halt")
            print_state()
            # do your code here
            
            print("machine halted\ntotal of " + str(inst_count) + " instructions executed\nfinal state of machine:\n")
            _state["pc"] += 1
            print_state()
        elif(_pc_oppcode["pc"+str(_state["pc"])] == "111"): # noop
            print("noop")
            print_state()
            # do your code here
            
            _state["pc"] += 1 # dummy


try:
    # receive machine argument from command line ex. python Simulation.py machineCode.txt
    inFilePath = sys.argv[1]
except :
    print("please insert input file ex. python Simulation.py machineCode.txt")
    exit(1)
init_MEM_REG()
simulation()
