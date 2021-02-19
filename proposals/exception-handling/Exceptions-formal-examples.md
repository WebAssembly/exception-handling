# 3rd proposal formal spec examples

This document contains WebAssembly code examples mentioned in comments on this repository, and what they reduce to, according to the "3rd proposal formal spec overview".

Its purpose is to make sure everyone is happy with the implications of the semantics in the current 3rd proposal, or to aid discussions on these semantics.

The first *example 0* contains all the new instructions, and it is the only one with an almost full reduction displayed. It is meant to easily show how the spec works, even if the reader has not spent much time with the WebAssembly formal spec.

For all other examples just the result of the reduction is given. These examples are taken from comments in this repository, which are linked. Some times/often the examples are modified to fit the current syntax.

If anyone would like that I add another reduction trace, or other examples, please let me know, I'd be happy to.

### notation

If `x` is an exception index, then `a_x` denotes its exception tag, i.e., `F_exn(x) = a_x`, where `F` is the current frame.

## example 0

The only example with an almost full reduction trace, and all new instructions (`rethrow` is hidden in `unwind`'s reduct). The first 3 steps, reducing the several `try`s to their respective administrative instructions, are not shown.

```
(func (result i32) (local i32)
  try
    try
      try
        throw x
      unwind
        i32.const 27
        local.set 0
      end
    delegate 0
  catch x
    local.get 0
  end)
```

Take the frame `F = (locals i32.const 0, module m)`. We have:

```
↪ ↪ ↪ F; catch_1{a_x local.get 0} (label_1{}
           (delegate{0} (label_0{}
             (catch_0{all i32.const 27 local.set 0 rethrow 0} (label_0{}     ;; the try-unwind
               throw a_x end) end) end) end) end) end

```

For the throw context `T = label_0{}[_]end` the above is the same as

```
F; catch_1{a_x local.get 0} (label_1{}
     (delegate{0} (label_0{}
       (catch_0{all i32.const 27 local.set 0 rethrow 0}
         T[throw a_x] end) end) end) end) end

↪ F; catch_1{a_x local.get 0} (label_1{}
       (delegate{0} (label_0{}
         (caught{a_x} (label_0{} i32.const 27 local.set 0 rethrow 0
           end) end) end) end) end) end
```

Let `F'` be the frame `{locals i32.const 27, module m}`, and let `B^1 = label_0{} [_] end`.

```
↪ F'; catch_1{a_x local.get 0} (label_1{}
       (delegate{0} (label_0{}
         (caught{a_x} B^1 [rethrow 0] end) end) end) end) end

↪ F'; catch_1{a_x local.get 0} (label_1{}
       (delegate{0} (label_0{}
         (caught{a_x} B^1 [throw a_x] end) end) end) end) end
```

Let `T' = label_0{} (caught{a_x} B^1 [_] end) end`.

```
↪ F'; catch_1{a_x local.get 0} (label_1{} throw a_x end) end

↪ F'; caught_1{a_x} (label_1{} local.get 0 end) end

↪ ↪ ↪ i32.const 27
```

## behaviour of `rethrow`

### example 1

Interaction of `rethrow` with `unwind`. Taken from [this comment](https://github.com/WebAssembly/exception-handling/issues/87#issuecomment-705586912) by @rossberg.

```
try
  throw x
catch x
  try
    instr1*
    rethrow 0
  unwind
    instr2*
  end
end
```

Reduces to

```
caught_0{a_x} (label_0 {} (caught_0{a_x} (label_0 {} instr2* throw a_x end) end) end) end
```

which in turn reduces to `throw a_x`.

Note that any global state changes due to `instr1*` or `instr2*` will take place.

### example 2

`rethrow`'s immediate validation error.

@aheejin gave the following
[example in this comment](https://github.com/WebAssembly/exception-handling/pull/143#discussion_r522673735)

```
try $label0
  rethrow $label0  ;; cannot be done, because it's not within catch below
catch
end
```

This is a validation error (no catch block at given rethrow depth).

## target of `delegate`'s immediate (label depth)

@aheejin gave the following
[examples in this comment](https://github.com/WebAssembly/exception-handling/pull/143#discussion_r522673735)

### example 3

`delegate` inside a catch is a validation error.

```
try $label0
catch
  try
    ...
  delegate $label0  ;; cannot be done, because $label0's catch is not below but above here
end
```

This is a validation error because `delegate`'s `$label0` refers to the catch-label `label { result ε, type catch}`, not to a try-label.

### example 4

`delegate` correctly targetting a `try-delegate` and a `try-catch`.

```
try $label1
  try $label0
    try
      throw x
    delegate $label0
  delegate $label1
catch x
  instr*
end
```

The thrown exception is (eventually) caught by the outer try's `catch x`, so the above reduces to

```
caught_0{a_x} (label_0 {} instr* end) end
```


## interaction of `delegate` and `unwind`

Two examples from issue #130.

### example 5

The [opening example](https://github.com/WebAssembly/exception-handling/issues/130#issue-713113953)
of issue #130.

```
i32.const 11
global.set 0
try $l
  try
    try
      throw x
    delegate 1
  unwind
    i32.const 27
    global.set 0
  end
catch_all
end
global.get 0
```

Here, `delegate 1` targets the label `$l` (so it would be the same if we wrote `delegate $l` instead).

This example returns `11`, because `delegate` skips everything up to and not including `try $l`.

### example 6

This example
[appears to keep](https://github.com/WebAssembly/exception-handling/issues/130#issuecomment-704249682)
the issue #130 open.

@RossTate expressed concerns with respect to an example possibly equivalent to
the one below. "Possibly", because the original example in the comment refers to
an `unwinding` branch, first presented in issue #124, so I attempted to rewrite
the example to match the current syntax as best I could.

```
try $t
  try $l
    try $u
      try
        throw x
      delegate $t
    unwind
      instr1*
    end
  catch x
    instr2*
  end
  instr3*
catch_all
  instr4*
end
```

The thrown exception tag `a_x` is delegated to the outer `try $l - catch_all`, ignoring the `try $u - unwind` and `try - catch x` in between. So this example reduces to

```
caught_0{a_x} (label_0{} instr4* end) end
```

During the above reduction, `instr1*`, `instr2*`, and `instr3*` are never executed.


