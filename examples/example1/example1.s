.syntax unified
.thumb

.global example1
.type example1, %function
example1:
    mov r2, #80
    mov r3, #4
    lsls r4, r0, r3
    mul r5, r0, r2
    subs r6, r5, r0
    subs r7, r4, r6
    movs r0, r7
    bx lr
