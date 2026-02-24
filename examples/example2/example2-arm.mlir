builtin.module {
  func.func @example2() -> i32 {
    %0 = "arm.mov"() {imm = 5 : i32} : () -> i32
    %1 = "arm.movw"() {imm = 18815 : i32} : () -> i32
    %2 = "arm.movt"(%1) {imm = 94 : i32} : (i32) -> i32
    %3 = "arm.mov"() {imm = 2 : i32} : () -> i32
    %4 = "arm.asr"(%0, %3) : (i32, i32) -> i32
    %5 = "arm.sub"(%4, %2) : (i32, i32) -> i32
    %6 = "arm.movreg"(%5) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
