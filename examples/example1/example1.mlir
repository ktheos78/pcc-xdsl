builtin.module {
  func.func @example1() -> i32 {
    %0 = arith.constant 0 : i32
    %1 = arith.constant 0 : i32
    %2 = arith.constant 0 : i32
    %3 = arith.constant 5 : i32
    %4 = arith.constant 9 : i32
    %5 = arith.constant 16 : i32
    %6 = arith.muli %3, %5 : i32
    %7 = arith.subi %6, %4 : i32
    func.return %7 : i32
  }
}
