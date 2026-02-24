builtin.module {
  func.func @example2() -> i32 {
    %0 = arith.constant 0 : i32
    %1 = arith.constant 0 : i32
    %2 = arith.constant 0 : i32
    %3 = arith.constant 0 : i32
    %4 = arith.constant 0 : i32
    %5 = arith.constant 5 : i32
    %6 = arith.constant 6179199 : i32
    %7 = arith.constant 0 : i32
    %8 = arith.addi %5, %7 : i32
    %9 = arith.constant 4 : i32
    %10 = arith.divsi %8, %9 : i32
    %11 = arith.subi %10, %6 : i32
    func.return %11 : i32
  }
}
