builtin.module {
  func.func @example3() -> i32 {
    %0 = arith.constant 5 : i32
    %1 = arith.addi %0, %0 : i32
    %2 = arith.constant 99999 : i32
    %3 = arith.constant 2 : i32
    %4 = arith.shrui %1, %3 : i32
    %5 = arith.muli %2, %4 : i32
    func.return %5 : i32
  }
}
