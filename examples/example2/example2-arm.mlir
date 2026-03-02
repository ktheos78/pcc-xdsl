builtin.module {
  func.func @example2(%arg0 : i32, %arg1 : i32, %arg2 : i32, %arg3 : i32) -> i32 {
    %c617919_i32 = "arm.movw"() {imm = 28095 : i32} : () -> i32
    %c617919_i32_1 = "arm.movt"(%c617919_i32) {imm = 9 : i32} : (i32) -> i32
    %0 = "arm.mov"() {imm = 2 : i32} : () -> i32
    %1 = "arm.asr"(%arg3, %0) : (i32, i32) -> i32
    %2 = "arm.add"(%1, %c617919_i32_1) : (i32, i32) -> i32
    %3 = "arm.movreg"(%2) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
