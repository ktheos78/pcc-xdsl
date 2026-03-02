int example1(int a, int b) {
    
    int c = a * 16;     // this gets turned into c = a << 4
    int d = c * 5;
    b = d - a;
    return c - b;
}

