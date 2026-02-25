int compiled_asm(void)
{
    int a, b, c;

    a = 70000;
    b = a / 16;
    c = b >> 3;
    
    return c * 3;
}