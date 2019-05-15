	.data
array1:	.space	12
size:	.word	12
	.text
main:	la $t0, array1
	li $t3, 1
	sw $t3, ($t0)
	li $t3, 2
	sw $t3, 4($t0)
	li $t3, 3
	sw $t3, 8($t0)
	lw $t3, ($t0)
	lw $t4, 4($t0)
	add $t1, $t3, $t4
	lw $t3, 8($t0)
	add $v0, $t1, $t3
	syscall
	