.syntax unified
.thumb

.global example2
.type example2, %function
example2:
    movw r4, #28095
    movt r4, #9
    mov r5, #2
    asrs r6, r3, r5
    adds r7, r6, r4
    movs r0, r7
    bx lr
