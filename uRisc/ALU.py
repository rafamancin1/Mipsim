from Registers import WriteToRegister

class ALU():
    def __init__(self):
        self.overflow = 0b0
        self.carry = 0b0
        self.neg = 0b0
        self.zero = 0b0
        self.negzero = 0b0
    def Exe(self, opCode, RC, ra, rb):
        if ra != None:
            ra = format(ra, "#018b")
        if rb != None:
            rb = format(rb, "#018b")
        if opCode == 0b0: #zero
            WriteToRegister(RC, format(0, "#018b"))
            self.zero = 1
            self.neg = 0
            self.carry = 0
            self.overflow = 0 
            self.negzero = 1
        if opCode == 0b1001:
            WriteToRegister(RC, ra)
            self.carry = 0
            self.overflow = 0
            if ra[2] == '1':
                self.neg = 1
                self.zero = 0
                self.negzero = 1
            elif int(ra, 2) == 0:
                self.zero = 1
                self.neg = 0
                self.negzero = 1
        elif opCode == 0b11000 or opCode == 0b11010 or opCode == 0b11100 or opCode == 0b11101 or opCode == 0b11011 or opCode == 0b11001:
            rc = 0
            if opCode == 0b11000: #arithmetic op
                rc = self.Adder(ra, rb)#ra+rb
            elif opCode == 0b11010:
                rc = self.Adder(ra, rb)
                rc = self.Adder(rc, format(1, "#018b"))#ra+rb+1
            elif opCode == 0b11100:
                rc = self.Adder(ra, format(1, "#018b"))#ra+1
            elif opCode == 0b11101:
                rc = self.Sub(ra, format(1, "#018b"))#ra-1
            elif opCode == 0b11011:
                rc = self.Sub(ra, rb)
                rc = self.Sub(ra, format(1, "#018b"))#ra-rb-1
            elif opCode == 0b11001:
                rc = self.Sub(ra, rb)#ra-rb
            if int(rc,2) == 0:
                self.zero = 1
                self.neg = 0
                self.negzero = 1
            else:
                self.zero = 0
                if rc[2] == '1':
                    self.neg = 1 
                    self.negzero = 1
                else:
                    self.neg = 0
                    self.negzero = 0
            WriteToRegister(RC, rc)
        elif opCode == 0b110 or opCode == 0b111 or opCode == 0b1000 or opCode == 0b1011 or opCode == 0b1011 or opCode == 0b01 or opCode == 0b00011 or opCode == 0b00101 or opCode == 0b00100 or opCode == 0b1010 or opCode == 0b10:
            self.carry = 0   #logical op
            self.overflow = 0
            if opCode == 0b110:
                WriteToRegister(RC, self.Xorb(ra,rb))
            elif opCode == 0b1010:
                WriteToRegister(RC, self.Andb(self.Notb(ra), rb))
            elif opCode == 0b111:
                WriteToRegister(RC, self.Notb(self.Xorb(ra,rb)))
            elif opCode == 0b1000:
                WriteToRegister(RC, self.Notb(ra))
            elif opCode == 0b1011:
                WriteToRegister(RC, self.Orb(ra, self.Notb(rb)))
            elif opCode == 0b01:
                WriteToRegister(RC, format(1, "#018b"))
            elif opCode == 0b00011:
                WriteToRegister(RC, self.Orb(self.Notb(ra), self.Notb(rb)))
            elif opCode == 0b00101:
                WriteToRegister(RC, self.Andb(self.Notb(ra), self.Notb(rb)))
            elif opCode == 0b00100:
                WriteToRegister(RC, self.Orb(ra,rb))
            elif opCode == 0b10:
                WriteToRegister(RC, self.Andb(ra,rb)) 
        elif opCode == 0b10001 or opCode == 0b10000: #pode estar errado
            ra = format(int(ra, 2)<<1, "#018b")
            if(len(ra) > 18):
                ra = "0b"+ra[3:]
            bRa = ra
            r15 = int(bRa[2])
            r14 = int(ra[2])
            self.carry = r15
            if opCode == 0b10000:
                self.overflow = 0
            else:
                self.overflow = r15 ^ r14
            if ra[2] == '1':
                self.neg = 1
                self.negzero = 1
            WriteToRegister(RC, ra) #shift aritmético à esquerda msm q lógico.
        elif opCode == 0b10011:
            sign = ra[2]
            ra = format(int(ra, 2)>>1, "#018b") 
            newRa = "0b"+sign+ra[3:]
            if sign == '1':
                self.neg = 1
                self.negzero = 1
            WriteToRegister(RC, newRa) #tbm
            self.carry = 0
            self.overflow = 0
        elif opCode == 0b10010:
            ra = format(int(ra, 2)>>1, "#018b")
            WriteToRegister(RC, ra)
            if int(ra, 2) == 0:
                self.zero = 1
                self.negzero = 1
            else:
                self.neg = 0
                self.zero = 0
                self.negzero = 0
            self.carry = 0
            self.overflow = 0
    
    def Adder(self, a, b):#16bits input com o 0b
        self.carry = 0
        c = ['0']*16
        carryIn = 0
        carryOut = 0
        for i in range(17, 1, -1):
            carryIn = self.carry
            if a[i] == '1' and b[i] == '1':
                if self.carry == 0:
                    c[i-2] = '0'
                else:
                    c[i-2] = '1'
                self.carry = 1
            elif a[i] == '1' or b[i] == '1':
                if self.carry == 1:
                    c[i-2] = '0'
                else:
                    c[i-2] = '1'
                    self.carry = 0
            else:
                if self.carry == 1:
                    c[i-2] = '1'
                else:
                    c[i-2] = '0'
                self.carry = 0
            carryOut = self.carry
        self.overflow = carryIn ^ carryOut
        result = "0b"
        for i in c:
            result += i
        return result

    def Sub(self, a, b):#16bits input com o 0b
        self.carry = 0
        c = ['0']*16
        borrowIn = 0
        borrowOut = 0
        for i in range(17, 1, -1):
            borrowIn = self.carry
            if a[i] == b[i]:
                if self.carry == 1:
                    c[i-2] = '1'
                else:
                    c[i-2] = '0'
                    self.carry = 0
            elif a[i] == '1':
                if self.carry == 1:
                    c[i-2] = '0'
                    self.carry = 0
                else:
                    c[i-2] = '1'
            else:
                if self.carry == 1:
                    c[i-2] = '0'
                else:
                    c[i-2] = '1'
                    self.carry = 1
            borrowOut = self.carry
        self.overflow = borrowIn ^ borrowOut
        result = "0b"
        for i in c:
            result += i
        return result
    
    def Notb(self, c):
        res = "0b"
        for i in range(2, 18):
            if c[i] == '1':
                res += '0'
            else:
                res += '1'
        return res
    
    def Andb(self, a, b):
        res = "0b"
        for i in range(2, 18):
            if a[i] != b[i]:
                res += '0'
            else:
                res += a[i]
        return res
    
    def Orb(self, a, b):
        res = "0b"
        for i in range(2, 18):
            if a[i] != b[i]:
                res += '1'
            else:
                res += a[i]
        return res
    
    def Xorb(self, a, b):
        res = "0b"
        for i in range(2, 18):
            if a[i] != b[i]:
                res += '1'
            else:
                res += '0'
        return res
    
    


