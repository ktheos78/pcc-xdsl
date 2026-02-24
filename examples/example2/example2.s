.syntax unified
.thumb
.global example2
.type example2, %function

example2:
    mov r0, #5
    movw r1, #18815
    movt r1, #94
    mov r2, #2
    asrs r3, r0, r2
    subs r4, r3, r1
    movs r0, r4
    bx lr
