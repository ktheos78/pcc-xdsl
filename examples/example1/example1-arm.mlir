builtin.module {
  func.func @example1(%arg0 : i32, %arg1 : i32) -> i32 {
    %c80_i32 = "arm.mov"() {imm = 80 : i32} : () -> i32
    %0 = "arm.mov"() {imm = 4 : i32} : () -> i32
    %1 = "arm.lsl"(%arg0, %0) : (i32, i32) -> i32
    %2 = "arm.mul"(%arg0, %c80_i32) : (i32, i32) -> i32
    %3 = "arm.sub"(%2, %arg0) : (i32, i32) -> i32
    %4 = "arm.sub"(%1, %3) : (i32, i32) -> i32
    %5 = "arm.movreg"(%4) : (i32) -> i32
    "arm.ret"() : () -> ()
  }
}
