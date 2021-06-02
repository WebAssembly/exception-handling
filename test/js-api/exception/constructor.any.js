// META: global=window,dedicatedworker,jsshell
// META: script=/wasm/jsapi/assertions.js

test(() => {
  assert_function_name(WebAssembly.Exception, "Exception", "WebAssembly.Exception");
}, "name");

test(() => {
  assert_function_length(WebAssembly.Exception, 1, "WebAssembly.Exception");
}, "length");

test(() => {
  assert_throws_js(TypeError, () => new WebAssembly.Exception());
}, "No arguments");

test(() => {
  const argument = { "parameters": [] };
  assert_throws_js(TypeError, () => WebAssembly.Exception(argument));
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
                     () => new WebAssembly.Exception(invalidArgument),
                     `new Exception(${format_value(invalidArgument)})`);
  }
}, "Invalid descriptor argument");

test(() => {
  const invalidTypes = ["i16", "i128", "f16", "f128", "u32", "u64", "i32\0"];
  for (const value of invalidTypes) {
    const argument = { parameters: [value] };
    assert_throws_js(TypeError, () => new WebAssembly.Exception(argument));
  }
}, "Invalid type parameter");
