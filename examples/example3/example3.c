int example3_1(int int1, int int2) {
    int int3;
    
    int2 = 99999;
    int3 = int1 >> 2;

    return int2 * int3;
}

int example3_2(char int1, char int2, char int3) {
    int int4 = int1 * int2;
    int int5 = int3 >> int1;
    int int6 = int4 & int5;

    return int6 *5;
}