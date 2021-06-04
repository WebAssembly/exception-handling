// META: global=window,dedicatedworker,jsshell
// META: script=/wasm/jsapi/assertions.js

test(() => {
  assert_function_name(WebAssembly.RuntimeException, "RuntimeException", "WebAssembly.RuntimeException");
}, "name");

test(() => {
  assert_function_length(WebAssembly.RuntimeException, 1, "WebAssembly.RuntimeException");
}, "length");

test(() => {
  assert_throws_js(TypeError, () => new WebAssembly.RuntimeException());
}, "No arguments");

test(() => {
  const argument = new WebAssembly.Exception({ parameters: [] });
  assert_throws_js(TypeError, () => WebAssembly.RuntimeException(argument));
}, "Calling");

test(() => {
  const invalidArguments = [
    undefined,
    null,
    false,
    true,
    "",
    "test",
    Symbol(),
    1,
    NaN,
    {},
  ];
  for (const invalidArgument of invalidArguments) {
    assert_throws_js(TypeError,
                     () => new WebAssembly.RuntimeException(invalidArgument),
                     `new RuntimeException(${format_value(invalidArgument)})`);
  }
}, "Invalid descriptor argument");

test(() => {
  const typesAndArgs = [["i32", 123n], ["i32", Symbol()], ["f32", 123n], ["f64", 123n], ["i64", undefined]];
  for (const typeAndArg of typesAndArgs) {
    const exn = new WebAssembly.Exception({ parameters: [typeAndArg[0]] });
    assert_throws_js(TypeError, () => new WebAssembly.RuntimeException(exn, typeAndArg[1]));
  }
}, "Invalid exception argument");
