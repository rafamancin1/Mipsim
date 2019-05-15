	.data
n1:	.word	4
n2:	.word	4
	.text
main:	li $t0, 4
	li $t1, 5
	mult $t0, $t1
	mfhi $t0
	mflo $t1