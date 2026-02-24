builtin.module {
  func.func @example3() -> i32 {
    %0 = "arm.mov"() {imm = 5 : i32} : () -> i32
    %1 = "arm.add"(%0, %0) : (i32, i32) -> i32
    %2 = "arm.movw"() {imm = 34463 : i32} : () -> i32
    %3 = "arm.movt"(%2) {imm = 1 : i32} : (i32) -> i32
    %4 = "arm.mov"() {imm = 2 : i32} : () -> i32
    %5 = "arm.lsr"(%1, %4) : (i32, i32) -> i32
    %6 = "arm.mul"(%3, %5) : (i32, i32) -> i32
    %7 = "arm.movreg"(%6) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
