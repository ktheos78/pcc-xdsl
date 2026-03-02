builtin.module {
  func.func @example3_1(%arg0 : i32, %arg1 : i32) -> i32 {
    %c2_i32 = "arm.mov"() {imm = 2 : i32} : () -> i32
    %c99999_i32 = "arm.movw"() {imm = 34463 : i32} : () -> i32
    %c99999_i32_1 = "arm.movt"(%c99999_i32) {imm = 1 : i32} : (i32) -> i32
    %0 = "arm.asr"(%arg0, %c2_i32) : (i32, i32) -> i32
    %1 = "arm.mul"(%0, %c99999_i32_1) : (i32, i32) -> i32
    %2 = "arm.movreg"(%1) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
  func.func @example3_2(%arg0 : i8, %arg1 : i8, %arg2 : i8) -> i32 {
    %c5_i32 = "arm.mov"() {imm = 5 : i32} : () -> i32
    %0 = arith.extsi %arg0 : i8 to i32
    %1 = arith.extsi %arg1 : i8 to i32
    %2 = "arm.mul"(%0, %1) : (i32, i32) -> i32
    %3 = arith.extsi %arg2 : i8 to i32
    %4 = arith.extsi %arg0 : i8 to i32
    %5 = "arm.asr"(%3, %4) : (i32, i32) -> i32
    %6 = "arm.and"(%2, %5) : (i32, i32) -> i32
    %7 = "arm.mul"(%6, %c5_i32) : (i32, i32) -> i32
    %8 = "arm.movreg"(%7) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
