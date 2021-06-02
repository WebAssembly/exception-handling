// META: global=window,dedicatedworker,jsshell
// META: script=/wasm/jsapi/memory/assertions.js

test(() => {
  const exn = new WebAssembly.Exception({ "parameters": [] })
  const runtimeExn = new WebAssembly.RuntimeException(exn);
  assert_throws_js(TypeError, () => runtimeExn.is());
}, "Missing arguments");

test(() => {
  const invalidValues = [
    undefined,
    null,
    true,
    "",
    Symbol(),
    1,
    {}
  ];
  const exn = new WebAssembly.Exception({ "parameters": [] })
  const runtimeExn = new WebAssembly.RuntimeException(exn);
  for (argument of invalidValues) {
    assert_throws_js(TypeError, () => runtimeExn.is(argument));
  }
}, "Invalid exception argument");

test(() => {
  const exn1 = new WebAssembly.Exception({ "parameters": ["i32"] })
  const exn2 = new WebAssembly.Exception({ "parameters": ["i32"] })
  const runtimeExn = new WebAssembly.RuntimeException(exn1, 42);
  assert_true(runtimeExn.is(exn1));
  assert_false(runtimeExn.is(exn2));
}, "is");
