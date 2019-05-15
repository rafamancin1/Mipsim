from ALU import ALU

def main():
    a = int("0x7fea", 16)
    b = int("0x2bc7", 16)
    a = format(a, "#018b")
    b = format(b, "#018b")
    print(int(b, 2))
    print(int(a,2))
    A = ALU()
    c = A.Sub(b, a)
    print(A.neg)
    print(c)
    
main()
