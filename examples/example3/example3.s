.syntax unified
.thumb

.global example3_1
.type example3_1, %function
example3_1:
    mov r2, #2
    movw r3, #34463
    movt r3, #1
    asrs r4, r0, r2
    mul r5, r4, r3
    movs r0, r5
    bx lr

.global example3_2
.type example3_2, %function
example3_2:
    mov r3, #5
    mul r4, r5, r6
    asrs r7, r8, r9
    ands r10, r4, r7
    mul r11, r10, r3
    movs r0, r11
    bx lr
