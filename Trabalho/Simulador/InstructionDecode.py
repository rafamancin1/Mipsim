



typeI = ["zeros", "and", "andnota", "passa", "xor", "or", "nor", "xnor", "passnota",
         "ornotb", "nand", "ones", "add", "addinc", "inca", "subdec", "sub", "deca",
         "lsl", "lsr", "asr", "asl"]
typeII = ["loadlit", "lc"]
typeIII = ["lcl", "lch"]
typeIV = ["jf", "jt"]
typeV = ["j"]
typeVI = ["jal", "jr"]
typeVII = ["store", "st", "load", "ld"]

#, instrType, opCode=None, RC=None, RA=None, RB=None, offset=None, R=None, cond=None
    

class Instruction():
    def __init__(self):
        self.instrType = None
        self.opCode = None
        self.RC = None
        self.RA = None
        self.RB = None
        self.offset = None
        self.R = None
        self.cond = None
    def littleToBig(self, attr):
        c1 = attr & 255
        c2 = (attr >> 8) & 255
        attr = (c1 << 8) + c2
    def setRi(self, n, i):
        if n > 8:
            raise RuntimeError #registro inexistente
        else:
            if i == 1:
                self.RC = n
            elif i == 2:
                self.RA = n
            elif i == 3:
                self.RB = n
    def setOffset(self, n): #deve extender constante n
        extendedSignal = "0b"
        b = format(n, "#018b")
        if self.instrType != 0b10:
            self.offset = b
            return
        sign = b[7]
        for i in range(5):
            extendedSignal += sign
        extendedSignal += b[7:]
        self.offset = extendedSignal
        
    def printInstr(self):#teste
        print("Type:{}\tOpCode:{}\nRC:{}\toffset:{}\nRA:{}\tRB:{}\nR:{}\tcond:{}".format(bin(self.instrType), self.opCode, self.RC, self.offset, self.RA, self.RB, self.R, self.cond))


def Decode(line, Labels):
    I = Instruction()
    s = ""
    for elem in line[1:]:
        s += elem
    op = line[0]
    F = s.split(',')
    if op in typeI:
        I.instrType = 0b01
        decodeTypeI(op, I, F)
    elif op in typeII:
        I.instrType = 0b10
        decodeTypeII(I, F)
    elif op in typeIII:
        I.instrType = 0b11
        if op == "lcl":
            I.R = 0b0
        else:
            I.R = 0b1
        decodeTypeIII(I, F)
    elif op[:2] in typeIV or op in typeV or op in typeVI:
        cond = ""
        I.instrType = 0b00
        if op[:2] in typeIV:
            if op[:2] == "jf":
                I.opCode = 0b00
            else:
                I.opCode = 0b01
            cond += op[3:]
        elif op in typeV:
            I.opCode = 0b10
        elif op in typeVI:
            I.opCode = 0b11
            if op == "jal":
                I.R = 0b0
            else:
                I.R = 0b1
        decodeTypeIVtoVI(I, F, cond, Labels)
    elif op in typeVII:
        I.instrType = 0b01
        if op == "load" or op == "ld":
            I.opCode = 0b10100
        else:
            I.opCode = 0b10110
        decodeTypeVII(I, F)
    else:
        raise SyntaxError("Instrução errada")
    return I
		
            
def decodeTypeI(op, I, F):
    #adicionar tratamento para o zero e outras instruções especiais.
    opCode = -1
    if op == "zeros" or op == "ones":
        if op == "zeros":
            I.opCode = 0b0
        else:
            I.opCode = 0b1
        try:
            I.setRi(int(F[0][1]), 1)
        except IndexError:
            raise SyntaxError("Instrução incompleta")
        if F[0][0].lower() != 'r':
            raise SyntaxError("Instrução errada")
        return
    elif op == "and":
        I.opCode = 0b10
    elif op == "andnota":
        I.opCode = 0b1010
    elif op == "passa" or op == "passnota" or  op == "inca" or op == "deca" or op == "lsl" or op == "lsr" or op == "asr" or op == "asl":
        if op == "passa":
            I.opCode = 0b1001
        elif op == "passnota":
            I.opCode = 0b1000
        elif op == "inca":
            I.opCode = 0b11100
        elif op == "deca":
            I.opCode = 0b11101
        elif op == "lsl":
            I.opCode = 0b10000
        elif op == "lsr":
            I.opCode = 0b10010
        elif op == "asr":
            I.opCode = 0b10011
        elif op == "asl":
            I.opCode = 0b10001
        try:
            I.setRi(int(F[0][1]), 1)
            I.setRi(int(F[1][1]), 2)
        except IndexError:
            raise SyntaxError("Instrução incompleta")
        for i in F: 
            if i[0].lower() != 'r':
                raise SyntaxError("Instrução errada")
        return
    elif op == "xor":
        I.opCode = 0b110
    elif op == "or":
        I.opCode = 0b100
    elif op == "nor":
        I.opCode = 0b101
    elif op == "xnor":
        I.opCode = 0b111
    elif op == "ornotb":
        I.opCode = 0b1011
    elif op == "nand":
        I.opCode = 0b11
    elif op == "add":
        I.opCode = 0b11000
    elif op == "addinc":
        I.opCode = 0b11010
    elif op == "subdec":
        I.opCode = 0b11011
    elif op == "sub":
        I.opCode = 0b11001
    try:    
        I.setRi(int(F[0][1]), 1)
        I.setRi(int(F[1][1]), 2)
        I.setRi(int(F[2][1]), 3)
    except IndexError:
        raise SyntaxError("Instrução incompleta")
    for i in F: 
        if i[0].lower() != 'r':
            raise SyntaxError("Instrução errada")
            
        
def decodeTypeII(I, F):
    I.RC = int(F[0][1])
    I.setOffset(int(F[1]))

def decodeTypeIII(I, F):
    if F[0][0].lower() != 'r':
        raise SyntaxError("Instrução errada")
    I.setRi(int(F[0][1]), 1)
    const = F[1].lower().split("const")
    if len(const) == 2:
        I.setOffset(int(const[1]))
    else:
        I.setOffset(int(const[0]))

def decodeTypeIVtoVI(I, F, cond, Labels):
    if I.opCode == 0b00 or I.opCode == 0b01:
        condCode = 0
        if cond == "neg":
            condCode = 0b100
        elif cond == "zero":
            condCode = 0b101
        elif cond == "carry":
            condCode = 0b110
        elif cond == "negzero":
            condCode = 0b111
        elif cond == "true":
            condCode = 0b0
        elif cond == "overflow":
            condCode = 0b011
        else:
            raise SyntaxError("Instrução errada")
        try:
            I.setOffset(Labels[F[0].lower()]) 
        except KeyError:
            I.setOffset(int(F[0])) 
        I.cond = condCode
    elif I.opCode == 0b10:
        try:
            I.setOffset(Labels[F[0].lower()])
        except KeyError:
            I.setOffset(Labels[F[0].lower()])
    elif I.opCode == 0b11:
        if F[0][0].lower() != 'r':
            raise SyntaxError("Instrução errada")
        I.setRi(int(F[0][1]), 1)

def decodeTypeVII(I, F): 
    for i in F:
        if i[0].lower() != 'r':
            raise SyntaxError("Instrução errada")
    I.setRi(int(F[0][1]), 2)
    I.setRi(int(F[1][1]), 3)
    
        
        


        
        
        
        
        
    

                        
