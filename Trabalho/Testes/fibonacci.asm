

;Programa que armazena na memória os 10 primeiros números da sequência de fibonacci

loadlit r0, 1000
loadlit r6, 10
zeros r1
ones r2
store r0, r1
inca r0, r0
store r0, r2
inca r0, r0

LOOP: add r3, r2, r1
    store r0, r3
    inca r0, r0
    passa r1, r2
    passa r2, r3
    deca r6, r6
    jf.zero LOOP
