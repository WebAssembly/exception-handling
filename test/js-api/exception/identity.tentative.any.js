// META: global=window,dedicatedworker,jsshell
// META: script=/wasm/jsapi/assertions.js
// META: script=/wasm/jsapi/wasm-module-builder.js

test(() => {
  const builder = new WasmModuleBuilder();

  // Tag defined in JavaScript and imported into Wasm
  const jsTag = new WebAssembly.Tag({ parameters: ["i32"] });
  const jsTagIndex = builder.addImportedTag("module", "jsTag", kSig_v_i)
  const jsTagExn = new WebAssembly.Exception(jsTag, [42]);
  const jsTagExnSamePayload = new WebAssembly.Exception(jsTag, [42]);
  const jsTagExnDiffPayload = new WebAssembly.Exception(jsTag, [53]);
  const throwJSTagExnIndex = builder.addImport("module", "throwJSTagExn", kSig_v_v);

  // Tag defined in Wasm and exported to JS
  const wasmTagIndex = builder.addTag(kSig_v_i);
  builder.addExportOfKind("wasmTag", kExternalTag, wasmTagIndex);
  const throwWasmTagExnIndex = builder.addImport("module", "throwWasmTagExn", kSig_v_v);
  // Will be assigned after an instance is created
  let wasmTagExn = null;
  let wasmTagExnSamePayload = null;
  let wasmTagExnDiffPayload = null;

  const imports = {
    module: {
      throwJSTagExn: function() { throw jsTagExn; },
      throwWasmTagExn: function() { throw wasmTagExn; },
      jsTag: jsTag
    }
  };

  // Call a JS function that throws an exception using a JS-defined tag, catches
  // it with a 'catch' instruction, and rethrows it.
  builder
    .addFunction("catch_js_tag_rethrow", kSig_v_v)
    .addBody([
      kExprTry, kWasmStmt,
        kExprCallFunction, throwJSTagExnIndex,
      kExprCatch, jsTagIndex,
        kExprDrop,
        kExprRethrow, 0x00,
      kExprEnd
    ])
    .exportFunc();

  // Call a JS function that throws an exception using a Wasm-defined tag,
  // catches it with a 'catch' instruction, and rethrows it.
  builder
    .addFunction("catch_wasm_tag_rethrow", kSig_v_v)
    .addBody([
      kExprTry, kWasmStmt,
        kExprCallFunction, throwWasmTagExnIndex,
      kExprCatch, wasmTagIndex,
        kExprDrop,
        kExprRethrow, 0x00,
      kExprEnd
    ])
    .exportFunc();

  // Call a JS function that throws an exception using a JS-defined tag, catches
  // it with a 'catch_all' instruction, and rethrows it.
  builder
    .addFunction("catch_all_js_tag_rethrow", kSig_v_v)
    .addBody([
      kExprTry, kWasmStmt,
        kExprCallFunction, throwJSTagExnIndex,
      kExprCatchAll,
        kExprRethrow, 0x00,
      kExprEnd
    ])
    .exportFunc();

  // Call a JS function that throws an exception using a Wasm-defined tag,
  // catches it with a 'catch_all' instruction, and rethrows it.
  builder
    .addFunction("catch_all_wasm_tag_rethrow", kSig_v_v)
    .addBody([
      kExprTry, kWasmStmt,
        kExprCallFunction, throwWasmTagExnIndex,
      kExprCatchAll,
        kExprRethrow, 0x00,
      kExprEnd
    ])
    .exportFunc();

  const buffer = builder.toBuffer();

  // The exception object's identity should be preserved across 'rethrow's in
  // Wasm code. Do tests with a tag defined in JS.
  WebAssembly.instantiate(buffer, imports).then(result => {
    try {
      result.instance.exports.catch_js_tag_rethrow();
    } catch (e) {
      assert_equals(e, jsTagExn);
      // Even if they have the same payload, they are different objects, so they
      // shouldn't compare equal.
      assert_not_equals(e, jsTagExnSamePayload);
      assert_not_equals(e, jsTagExnDiffPayload);
    }
    try {
      result.instance.exports.catch_all_js_tag_rethrow();
    } catch (e) {
      assert_equals(e, jsTagExn);
      assert_not_equals(e, jsTagExnSamePayload);
      assert_not_equals(e, jsTagExnDiffPayload);
    }
  });

  // Do the same tests with a tag defined in Wasm.
  WebAssembly.instantiate(buffer, imports).then(result => {
    const wasmTag = result.instance.exports.wasmTag;
    wasmTagExn = new WebAssembly.Exception(wasmTag, [42]);
    wasmTagExnSamePayload = new WebAssembly.Exception(wasmTag, [42]);
    wasmTagExnDiffPayload = new WebAssembly.Exception(wasmTag, [53]);
    try {
      result.instance.exports.catch_wasm_tag_rethrow();
    } catch (e) {
      assert_equals(e, wasmTagExn);
      assert_not_equals(e, wasmTagExnSamePayload);
      assert_not_equals(e, wasmTagExnDiffPayload);
    }
    try {
      result.instance.exports.catch_all_wasm_tag_rethrow();
    } catch (e) {
      assert_equals(e, wasmTagExn);
      assert_not_equals(e, wasmTagExnSamePayload);
      assert_not_equals(e, wasmTagExnDiffPayload);
    }
  });
}, "Identity check");
