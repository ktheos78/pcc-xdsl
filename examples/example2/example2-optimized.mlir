builtin.module {
  func.func @example2() -> i32 {
    %0 = arith.constant 5 : i32
    %1 = arith.constant 6179199 : i32
    %2 = arith.constant 2 : i32
    %3 = arith.shrsi %0, %2 : i32
    %4 = arith.subi %3, %1 : i32
    func.return %4 : i32
  }
}
