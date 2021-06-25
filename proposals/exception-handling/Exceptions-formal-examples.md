# 3rd proposal formal spec examples

This document contains WebAssembly code examples mentioned in comments on this repository, and what they reduce to, according to the "3rd proposal formal spec overview".

Its purpose is to make sure everyone is happy with the implications of the semantics in the current 3rd proposal, or to aid discussions on these semantics.

The first *example 0* contains all the new instructions, and it is the only one with an almost full reduction displayed. It is meant to easily show how the spec works, even if the reader has not spent much time with the WebAssembly formal spec.

For all other examples just the result of the reduction is given. These examples are taken from comments in this repository, which are linked. Some times/often the examples are modified to fit the current syntax.

If anyone would like that I add another reduction trace, or other examples, please let me know, I'd be happy to.

### notation

If `x` is an exception tag index, then `a_x` denotes its exception tag address, i.e., `F.exception[x] = a_x`, where `F` is the current frame.

## example 0

The only example with an almost full reduction trace, and all new instructions. The first 3 steps, reducing the several `try`s to their respective administrative instructions, are not shown.

```
(func (result i32) (local i32)
  try
    try
      try
        throw x
      catch_all
        i32.const 27
        local.set 0
      rethrow 0
      end
    delegate 0
  catch x
    local.get 0
  end)
```

Take the frame `F = (locals i32.const 0, module m)`. We have:

```
↪ ↪ ↪ F; label_1{} (catch_1{a_x local.get 0}
           (label_0{} (delegate{0}
             (label_0{} (catch_0{i32.const 27 local.set 0 rethrow 0}
               throw a_x end) end) end) end) end) end
```

For the empty throw context `T = [_]` the above is the same as

```
F; label_1{} (catch_1{a_x local.get 0}
     label_0{} (delegate{0}
       label_0{} (catch_0{i32.const 27 local.set 0 rethrow 0}
         T[throw a_x] end) end) end) end) end

↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         (label_0{} (caught{a_x} i32.const 27 local.set 0 rethrow 0
           end) end) end) end) end) end
```

Let `F'` be the frame `{locals i32.const 27, module m}`, and let `B^0 = [_]`.

```
↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         (label_0{} (caught{a_x} B^0 [rethrow 0]
           end) end) end) end) end) end

↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         (label_0{} (caught{a_x} B^0 [throw a_x]
           end) end) end) end) end) end
```

Let `T' = label_0{} (caught{a_x} B^0 [_] end) end`.

```
↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         T'[throw a_x] end) end) end) end

↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         T'[throw a_x] end) end) end) end

↪ F; label_1{} (catch_1{a_x local.get 0}
       (label_0{} (delegate{0}
         T'[throw a_x] end) end) end) end

↪ F; label_1{} (catch_1{a_x local.get 0}
       T'[throw a_x] end) end

↪ F; label_1{} (caught_1{a_x} local.get 0 end) end

↪ ↪ ↪ i32.const 27
```

## behaviour of `rethrow`

### example 1

Location of a rethrown exception.

```
try
  val1
  throw x
catch x
  try
    val2
    throw y
  catch_all
    try
      val3
      throw z
    catch z
      rethrow 2
    end
  end
end
```

In the above example, all thrown exceptions get caught and the first one gets rethrown from the catching block of the last one. So the above reduces to

```
label_0{} caught{a_x val1}
  val1 (label_0{} caught{a_y val2}
    (label_0{} caught{a_z val3}
      val3 val1 (throw a_x) end end)
        end end) end end)
```

which in this case is the same as `val1 (throw a_x)`.

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

`delegate` targeting a catch is a validation error.

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

`delegate` correctly targeting a `try-delegate` and a `try-catch`.

```
try $label1
  try $label0
    try
      throw x
    delegate $label0 ;; delegate 0
  delegate $label1 ;; delegate 1
catch x
  instr*
end
```

The thrown exception is (eventually) caught by the outer try's `catch x`, so the above reduces to the following.

```
label_0 {} (caught_0{a_x}  (label_0 {} instr* end) end
```

