
Regs = [format(0, "#06x") for i in range(8)]

def WriteToRegister(n, data, R=None):
    data = format(int(data, 2), "#06x")
    if R != None:
        #0xff00 if lcl(R=0) else 0x00ff (lch-R=1)
        if R == 1:
            Regs[n] = data
        else:
            data = switchBytes(data)
            Regs[n] = data
        return
    Regs[n] = data
    
    
def switchBytes(data):
    aux = ""
    b1 = data[2] + data[3]
    b2 = data[4] + data[5]
    aux += b2 + b1
    return "0x"+aux 

def ReadFromRegister(n):
    if n == None:
        return
    regData = Regs[n]
    regData = int(regData, 16)
    return regData

