builtin.module {
  func.func @example3() -> i32 {
    %0 = arith.constant 0 : i32
    %1 = arith.constant 0 : i32
    %2 = arith.constant 0 : i32
    %3 = arith.constant 5 : i32
    %4 = arith.constant 5 : i32
    %5 = arith.addi %3, %4 : i32
    %6 = arith.constant 99999 : i32
    %7 = arith.constant 2 : i32
    %8 = arith.shrui %5, %7 : i32
    %9 = arith.muli %6, %8 : i32
    func.return %9 : i32
  }
}
