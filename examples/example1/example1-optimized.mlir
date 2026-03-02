builtin.module {
  func.func @example1(%arg0 : i32, %arg1 : i32) -> i32 {
    %c80_i32 = arith.constant 80 : i32
    %0 = arith.constant 4 : i32
    %1 = arith.shli %arg0, %0 : i32
    %2 = arith.muli %arg0, %c80_i32 : i32
    %3 = arith.subi %2, %arg0 : i32
    %4 = arith.subi %1, %3 : i32
    func.return %4 : i32
  }
}
