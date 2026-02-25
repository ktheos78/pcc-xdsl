.syntax unified
.thumb
.global compiled_asm
.type compiled_asm, %function

compiled_asm:
    movw r0, #4464
    movt r0, #1
    mov r1, #4
    asrs r2, r0, r1
    mov r3, #3
    lsrs r4, r2, r3
    mul r5, r4, r3
    movs r0, r5
    bx lr
