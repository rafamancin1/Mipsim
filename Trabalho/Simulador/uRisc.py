from InstructionDecode import Decode, typeI, typeII, typeIII, typeIV, typeV, typeVI, typeVII
from PC import ProgramCounter
from ALU import ALU
from random import randint
from Registers import *
import argparse

MEMORY = ["0x0000" for i in range(65535)]

def signed16b(n):#nem sei se será preciso usar
    if n > 32767:
        return n-65536
    else:
        return n
    
def screen(A, PC):
    print("-----Estado do processador-----")
    print("R0:{}\tR1:{}\tcarry:{}\nR2:{}\tR3:{}\toverflow:{}\nR4:{}\tR5:{}\tzero:{}\nR6:{}\tR7:{}\tneg:{}\n\t\tPC:{}\tnegzero:{}".format(Regs[0], Regs[1], A.carry, Regs[2], Regs[3], A.overflow, Regs[4], Regs[5], A.zero, Regs[6], Regs[7], A.neg, PC, A.negzero))
 
def fetchLabels(Labels, srcFile):
    i = 0
    f = open(srcFile, 'r')
    pendingLabel = ""
    for line in f:
        if line == '\n':
            continue
        commentPos = line.find(';')
        if commentPos != -1:
            line = line[:commentPos]
            if line == "":
                continue
        labelPos = line.find(':')
        if labelPos != -1:
            pendingLabel = line[:labelPos]
            line = line[labelPos+2:]
            if line == "":
                continue
        if pendingLabel != "":
            Labels.update({pendingLabel.lower():i})
            pendingLabel = ""
        i += 1
        
def uRisc(srcFile, screenFlag):
    f = open(srcFile, 'r') 
    Labels = dict()
    PC = ProgramCounter()
    A = ALU()
    fetchLabels(Labels, srcFile)
    for line in f:
        unpreparedI = []
        unpreparedI = PC.ReadInstruction(line)
        if unpreparedI == [] or unpreparedI == "":
            continue
        I = Decode(unpreparedI, Labels)
        if I == None:
            continue
        else:
            PC.loadIR(I)
    PCMax = len(PC.IR)
    if 'l' in Labels:
        PCMax = Labels['l']
    while True:
        if PC.PC == PCMax:
            break
        I = PC.InstructionFetch()
        PrevPC = PC.PC
        PC.UpdatePC()
        if I.instrType == 0b01:
            if I.opCode == 0b10100 or I.opCode == 0b10110:
                a = ReadFromRegister(I.RA)
                b = ReadFromRegister(I.RB)
                if I.opCode == 0b10100:
                    WriteToRegister(I.RA, MEMORY[b]) #load
                else:
                    MEMORY[a] = format(b, "#06x") #store
            else:
                a = ReadFromRegister(I.RA)
                b = ReadFromRegister(I.RB)
                A.Exe(I.opCode, I.RC, a, b)
        elif I.instrType == 0b10:
            WriteToRegister(I.RC, I.offset)
        elif I.instrType == 0b11:
            if I.R == 1:
                WriteToRegister(I.RC, I.offset, I.R)
            else:
                WriteToRegister(I.RC, I.offset, I.R)
        elif I.instrType == 0b00:#jumps
            jumpCond = None
            if I.opCode == 0b00:
                jumpCond = 0
            elif I.opCode == 0b01:
                jumpCond = 1
            elif I.opCode == 0b10:
                jumpCond = 1#vai dar jump
            elif I.opCode == 0b11:
                if I.R == 0:
                    WriteToRegister(7, format(PC.PC, "#016b")) #jump and link
                    b = ReadFromRegister(I.RC)
                    PC.UpdatePC(b)
                    continue
                else:
                    b = ReadFromRegister(I.RC)#jump register 
                    PC.UpdatePC(b)
                    continue
            #determinando cond agora
            jump = None
            if I.cond != None:
                if I.cond == 0b100:
                    jump = jumpCond == A.neg
                elif I.cond == 0b101:
                    jump = jumpCond == A.zero
                elif I.cond == 0b110:
                    jump = jumpCond == A.carry
                elif I.cond == 0b111:
                    jump = jumpCond == A.negzero
                elif I.cond == 0b0:
                    jump = True
                elif I.cond == 0b011:
                    jump = jumpCond == A.overflow
            else:
                jump = True
            if jump:
                off = int(I.offset, 2)
                PC.UpdatePC(off)
        if screenFlag:
            screen(A, format(PrevPC, "#06x"))
            wait = input()
        
def main():
    parser = argparse.ArgumentParser(prog="uRisc", description="Um simulador uRisc.", epilog="E é isso aí. Até mais, e obrigado pelos peixes!", usage="%(prog)s filename [-h] [-d inicio nPalavras] [-s] [-p]")
    parser.add_argument('filename', help="nome do arquivo que possui o código fonte")
    parser.add_argument('-d', '--dump', help="dump de memória a partir de uma posição inicial, seguido de n palavras", nargs=2)
    parser.add_argument('-s', '--screen', help="escreve na saída padrão o estado do processador após cada instrução", action='store_true')
    parser.add_argument('-p', '--pause', help="pausa quando a tela estiver cheia de tralha", action='store_true')
    args = parser.parse_args()
    srcFile = args.filename
    screen = args.screen
    pause = args.pause
    uRisc(srcFile, screen)
    if args.dump != None:
        aux = "0x"+args.dump[0]
        memDump = int(aux, 16)
        nWords = int(args.dump[1])
        print(MEMORY[memDump:memDump+nWords])

if __name__ == "__main__":
    main()
    
