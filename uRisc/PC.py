class ProgramCounter():
    def __init__(self):
        self.PC = 0
        self.IR = []

    def UpdatePC(self, offset=None):
        if offset == None:
            self.PC += 1
        else:
            self.PC = offset
        
    def ReadInstruction(self, line):
        preIR = ""
        line = line.strip('\n')
        if line == "":
            return line
        commentPos = line.find(';')
        if commentPos != -1:
            preIR = line[:commentPos]
        else:
            preIR = line
        labelPos = preIR.find(':')
        if labelPos != -1:
            preIR = preIR[labelPos+1:]
        return preIR.split()
    
    def loadIR(self, I):
        self.IR.append(I)
        
    def InstructionFetch(self):
        return self.IR[self.PC]
        
