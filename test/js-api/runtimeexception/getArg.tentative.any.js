// META: global=window,dedicatedworker,jsshell
// META: script=/wasm/jsapi/memory/assertions.js

test(() => {
  const exn = new WebAssembly.Exception({ "parameters": [] })
  const runtimeExn = new WebAssembly.RuntimeException(exn, []);
  assert_throws_js(TypeError, () => runtimeExn.getArg());
  assert_throws_js(TypeError, () => runtimeExn.getArg(exn));
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
  const runtimeExn = new WebAssembly.RuntimeException(exn, []);
  for (argument of invalidValues) {
    assert_throws_js(TypeError, () => runtimeExn.getArg(argument, 0));
  }
}, "Invalid exception argument");

test(() => {
  const exn = new WebAssembly.Exception({ "parameters": [] })
  const runtimeExn = new WebAssembly.RuntimeException(exn, []);
  assert_throws_js(RangeError, () => runtimeExn.getArg(exn, 1));
}, "Index out of bounds");

test(() => {
  const outOfRangeValues = [
    undefined,
    NaN,
    Infinity,
    -Infinity,
    -1,
    0x100000000,
    0x1000000000,
    "0x100000000",
    { valueOf() { return 0x100000000; } },
  ];

  const exn = new WebAssembly.Exception({ "parameters": [] })
  const runtimeExn = new WebAssembly.RuntimeException(exn, []);
  for (const value of outOfRangeValues) {
    assert_throws_js(TypeError, () => runtimeExn.getArg(exn, value));
  }
}, "Getting out-of-range argument");

test(() => {
  const exn = new WebAssembly.Exception({ "parameters": ["i32"] })
  const runtimeExn = new WebAssembly.RuntimeException(exn, [42]);
  assert_equals(runtimeExn.getArg(exn, 0), 42);
}, "getArg");
