

;Programa que calcula o fatorial de 5 e armazena na memória

loadlit r0, 1000
loadlit r4, 5
loadlit r5, 7 
loadlit r6, 5
jal r5
store r0,r6
L: j L

FATORIAL:
    deca r4, r4
    passa r1, r4
    jf.zero MULTIPLICA
    jr r7

MULTIPLICA: add r2,r2,r6
    deca r1,r1
    jf.zero MULTIPLICA
    passa r6, r2
    zeros r2
    j FATORIAL
    
