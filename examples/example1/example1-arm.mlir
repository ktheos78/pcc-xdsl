builtin.module {
  func.func @example1() -> i32 {
    %0 = "arm.mov"() {imm = 5 : i32} : () -> i32
    %1 = "arm.mov"() {imm = 9 : i32} : () -> i32
    %2 = "arm.mov"() {imm = 4 : i32} : () -> i32
    %3 = "arm.lsl"(%0, %2) : (i32, i32) -> i32
    %4 = "arm.sub"(%3, %1) : (i32, i32) -> i32
    %5 = "arm.movreg"(%4) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
