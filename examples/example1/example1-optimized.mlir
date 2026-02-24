builtin.module {
  func.func @example1() -> i32 {
    %0 = arith.constant 5 : i32
    %1 = arith.constant 9 : i32
    %2 = arith.constant 4 : i32
    %3 = arith.shli %0, %2 : i32
    %4 = arith.subi %3, %1 : i32
    func.return %4 : i32
  }
}
