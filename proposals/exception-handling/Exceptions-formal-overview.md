# 3rd proposal formal spec overview

This is an overview of the 3rd proposal's formal spec additions, to aid in discussions concerning the proposed semantics.

## Abstract Syntax

### Types

Exception Types

```
exntype ::= [t*] -> []
```

### Instructions

```
instr ::= ... | throw x | rethrow l
        | try bt instr* (catch x instr*)* (catch_all instr*)? end
        | try bt instr* delegate l
        | try bt instr* unwind instr* end
```

### Modules

Exceptions (definitions)

```
exn ::= export* exception exntype  | export* exception exntype import
```

Modules


```
mod ::= module ... exn*
```

## Validation (Typing)

To verify that a `try...delegate l` instruction refers to a label introduced by a try block (I'll call this a try-label), introduce a type attribute to labels in the validation context, which type attribute is set to `try` when the label is a try-label. The original notation `label [t*]` will then be a shortcut for `label {result [t*], type ε}`.

To verify that the `rethrow l` instruction refers to a surrounding catch block, we introduce a stack `caught` to validation contexts, which gets an exception index or the keywork `all` prepended whenever we enter instructions inside a `catch exnidx` or `catch_all` block, respectively. This addition is reflected in the execution rules, by the administrative instruction `caught` which models the stack of caught exceptions on the wasm stack.

### Instructions


```
C_exn(x) = [t*] -> []
--------------------------------
C |- throw x : [t1* t*] -> [t2*]


C_caught(l) =/= ε
-------------------------------
C |- rethrow l : [t1*] -> [t2*]


bt = [t1*] -> [t2*]
C, label {result [t2*], type try} |- instr* : [t1*] -> [t2*]
(C_exn(x_i) = [t'_i*] -> [])^n
(C, label [t2*], caught x_i |- instr_i* : [t'_i*] -> [t2*])^n
(C, label [t2*], caught all |- instr'* : [] -> [t2*])?
------------------------------------------------------------------
try bt instr* (catch x_i instr_i*)^n (catch_all instr'*)? end : bt


bt = [t1*] -> [t2*]
C, label {result [t2*], type try} |- instr* : [t1*] -> [t2*]
C_label(l).type = try
------------------------------------------------------------
try bt instr* delegate l : bt


bt = [t1*] -> [t2*]
C, label {result [t2*], type try} |- instr_1* : [t1*] -> [t2*]
C, label [t2*], caught all |- instr_2* : [] -> [t2*]
--------------------------------------------------------------
try bt instr_1* unwind instr_2* : bt
```

## Execution (Reduction)

### Runtime structure

Stores

```
S ::= {..., exn exninst*}
```

Exception Instances

```
exninst ::= {type exntype}
```

Module Instances

```
m ::= {..., (exn a)*}
```

Administrative Instructions

```
instr ::= ... | throw a | catch_n{a instr*}*{instr*}? instr* end
        | delegate{l} instr* end | caught_m{a val^n} instr* end
```

Caught exceptions stack

```
C^0 ::= val^m [_] instr
C^{n+1} ::= caught{exnaddr val^k} C^n end
```

Throw Contexts

```
T ::= v* [_] e* | label_n{e*} T end | caught_m{a val^n} T end | frame_n{F} T end
```

### Instructions


```
F; throw x  -->  F; throw a  (iff F_exn(x) = a)

caught_m{a val^n} C^l[rethrow l] end
  --> caught_m{a val^n} C^l[val^n (throw a)] end

caught_m{a val^n} val^m end  -->  val^m
```

A keyword `all` is introduced to simplify the requirements for the `try` execution step below.

```
F; val^n (try bt instr* (catch x_i instr_i*)* (catch_all instr'*)? end)
  -->  F; catch_m{a_i instr_i*}*{all instr'*}? (label_m{} val^n instr* end) end
  (iff bt = [t1^n] -> [t2^m] and (F_exn(x_i) = a_i)*)

catch_m{a_i instr_i*}*{all instr'*}? val^m end --> val^m

S; F; catch_m{a_i instr_i*}*{all instr'*}? T[val^n (throw a)] end
  -->  S; F; caught_m{a val^n} val^n instr_i* end
  (iff S_exn(a) = {type [t^n]->[]} and i is the least such that a_i = a)

S; F; catch_m{a_i instr_i*}*{all instr*} T[val^n (throw a)] end
  -->  S; F; caught_m{a val^n} instr* end
  (iff S_exn(a) = {type [t^n]->[]} and for every i, a_i =/= a)

S; F; catch_m{a_i instr_i*}* T[val^n (throw a)] end
  -->  S; F; val^n (throw a)
  (iff for every i, a_i =/= a)


val^n (try bt instr* delegate l) --> delegate{l} (label_m{} val^n instr* end) end
  (iff bt = [t^n] -> [t^m])

catch_m{a_i instr_i*}*{instr*}? (label_m{} B^l[ delegate{l} (T[val^n (throw a)]) end ] end) end
  --> catch_m{a_i instr_i*}*{instr*}? label_m{} val^n (throw a) end end


try bt instr* unwind instr'* end --> try bt instr* catch_all instr'* rethrow 0 end
```
