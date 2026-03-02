builtin.module {
  func.func @example2(%arg0 : i32, %arg1 : i32, %arg2 : i32, %arg3 : i32) -> i32 {
    %c617919_i32 = arith.constant 617919 : i32
    %0 = arith.constant 2 : i32
    %1 = arith.shrsi %arg3, %0 : i32
    %2 = arith.addi %1, %c617919_i32 : i32
    func.return %2 : i32
  }
}
