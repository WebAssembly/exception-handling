// META: global=window,dedicatedworker,jsshell

test(() => {
  const argument = { "parameters": [] };
  const exception = new WebAssembly.Exception(argument);
  const runtimeException = new WebAssembly.RuntimeException(exception);
  assert_class_string(runtimeException, "WebAssembly.RuntimeException");
}, "Object.prototype.toString on a RuntimeException");

test(() => {
  assert_own_property(WebAssembly.RuntimeException.prototype, Symbol.toStringTag);

  const propDesc = Object.getOwnPropertyDescriptor(WebAssembly.RuntimeException.prototype, Symbol.toStringTag);
  assert_equals(propDesc.value, "WebAssembly.RuntimeException", "value");
  assert_equals(propDesc.configurable, true, "configurable");
  assert_equals(propDesc.enumerable, false, "enumerable");
  assert_equals(propDesc.writable, false, "writable");
}, "@@toStringTag exists on the prototype with the appropriate descriptor");
