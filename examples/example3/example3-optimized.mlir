builtin.module {
  func.func @example3_1(%arg0 : i32, %arg1 : i32) -> i32 {
    %c2_i32 = arith.constant 2 : i32
    %c99999_i32 = arith.constant 99999 : i32
    %0 = arith.shrsi %arg0, %c2_i32 : i32
    %1 = arith.muli %0, %c99999_i32 : i32
    func.return %1 : i32
  }
  func.func @example3_2(%arg0 : i8, %arg1 : i8, %arg2 : i8) -> i32 {
    %c5_i32 = arith.constant 5 : i32
    %0 = arith.extsi %arg0 : i8 to i32
    %1 = arith.extsi %arg1 : i8 to i32
    %2 = arith.muli %0, %1 : i32
    %3 = arith.extsi %arg2 : i8 to i32
    %4 = arith.extsi %arg0 : i8 to i32
    %5 = arith.shrsi %3, %4 : i32
    %6 = arith.andi %2, %5 : i32
    %7 = arith.muli %6, %c5_i32 : i32
    func.return %7 : i32
  }
}
