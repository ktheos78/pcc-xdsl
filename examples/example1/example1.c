int example1(void) {
    int a, b, c;
    
    a = 5;
    b = 9;
    c = a * 16;     // this gets turned into c = a << 4

    return c - b;
}

