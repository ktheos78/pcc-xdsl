.syntax unified
.thumb
.global example3
.type example3, %function

example3:
    mov r0, #5
    adds r1, r0, r0
    movw r2, #34463
    movt r2, #1
    mov r3, #2
    lsrs r4, r1, r3
    mul r5, r2, r4
    movs r0, r5
    bx lr
