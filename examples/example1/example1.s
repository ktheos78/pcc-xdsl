.syntax unified
.thumb
.global example1
.type example1, %function

example1:
    mov r0, #5
    mov r1, #9
    mov r2, #4
    lsls r3, r0, r2
    subs r4, r3, r1
    movs r0, r4
    bx lr
