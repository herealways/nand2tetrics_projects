// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@SCREEN
D=A
@arr
M=D

@8192 //set n to 8192
D=A
@n
M=D
(LOOP)
	@i
	M=0
	@KBD
	D=M
	@BLACK
	D;JGT
	
	@WHITE
	D;JEQ
	
	@LOOP
	D;JMP
	
	(BLACK)	
	@arr //set SCREEN[i]=-1
	D=M
	@i
	A=D+M
	M=-1
	
	@i //i++
	M=M+1

	@i //if i=n then draw finished, else continue to set SCREEN[i]=-1
	D=M
	@n
	D=M-D
	@FINISHBLACK
	D;JEQ
	@BLACK
	D;JGT

	(FINISHBLACK)
	@KBD
	D=M
	
	@LOOP
	D;JEQ
	
	@FINISHBLACK
	D;JGT

	(WHITE)	
	@arr
	D=M
	@i
	A=D+M
	M=0

	@i
	M=M+1

	@i
	D=M
	@n
	D=M-D
	@FINISHWHITE
	D;JEQ
	@WHITE
	D;JGT

	(FINISHWHITE)
	@KBD
	D=M
	
	@LOOP
	D;JGT
	
	@FINISHWHITE
	D;JEQ
