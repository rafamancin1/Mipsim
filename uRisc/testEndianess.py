from Registers import switchEndianess

D = "0x00ab"
print(int(D,16))
D = switchEndianess(D)
print(int(D,16))
print(D)
D = switchEndianess(D)
print(int(D,16))
print(D)
