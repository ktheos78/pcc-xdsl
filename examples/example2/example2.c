int example2(void) {
    int a, b, c;
    char d, e;

    a = 5;
    b = 6179199;
    d = a + 0;      // this gets eliminated
    c = d / 4;      // this gets turned into a >> 2

    return c - b;
}

