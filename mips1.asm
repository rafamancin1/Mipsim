	.data
	var1:	.word 4
	var2:	.word 5
	.text
main:
	lw $t0, var1
	lw $t1, var2
	add $t2, $t1, $t0
	sw $v0, var1
	syscall
	