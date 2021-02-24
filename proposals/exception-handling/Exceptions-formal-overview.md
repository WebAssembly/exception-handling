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
        | try bt instr* (catch x instr*)+ end
        | try bt instr* (catch x instr*)* catch_all instr* end
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


To verify that a `try...delegate l` instruction refers to a label surrounding the instructions of a try block (call this a try-label), introduce a `kind` attribute to labels in the validation context, which is set to `try` when the label is a try-label.

Similarly, to verify that the `rethrow l` instruction refers to a label surrounding the instructions of a catch block (call this a catch-label), we allow the `kind` attribute of labels in the validation context to be set to `catch` when the label is a catch-label. This addition is reflected in the execution rules, by the administrative instruction `caught` which introduces a label around the catching try-block.

The original notation `label [t*]` is now a shortcut for `label {result [t*], kind ε}`.


### Instructions


```
C_exn(x) = [t*] -> []
--------------------------------
C ⊢ throw x : [t1* t*] -> [t2*]


C_label(l) =/= ε
C_label(l).kind = catch
-------------------------------
C ⊢ rethrow l : [t1*] -> [t2*]


bt = [t1*] -> [t2*]
C, label {result [t2*], kind try} ⊢ instr* : [t1*] -> [t2*]
(C_exn(x_i) = [t'_i*] -> [])^n
(C, label { result [t2*], kind catch } ⊢ instr_i* : [t'_i*] -> [t2*])^n
(C, label { result [t2*], kind catch } ⊢ instr'* : [] -> [t2*])^k
(k=0 and n>0) or (k=1 and n≥0)
------------------------------------------------------------------
C ⊢ try bt instr* (catch x_i instr_i*)^n (catch_all instr'*)^k end : bt


bt = [t1*] -> [t2*]
C, label {result [t2*], kind try} ⊢ instr* : [t1*] -> [t2*]
C_label(l) =/= ε
C_label(l).kind = try
------------------------------------------------------------
C ⊢ try bt instr* delegate l : bt


bt = [t1*] -> [t2*]
C, label {result [t2*], kind try} ⊢ instr_1* : [t1*] -> [t2*]
C, label [t2*] ⊢ instr_2* : [] -> []
--------------------------------------------------------------
C ⊢ try bt instr_1* unwind instr_2* end : bt
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
m ::= {..., exn a*}
```

Administrative Instructions

```
instr ::= ... | throw a | catch_n{a instr*}*{instr*}? instr* end
        | delegate{l} instr* end | caught_m{a val^n} instr* end
```

Throw Contexts

```
T ::= val* [_] instr* | label_n{instr*} T end | caught_m{a val^n} T end | frame_n{F} T end
```

### Instructions


```
F; throw x  ↪  F; throw a  (iff F_exn(x) = a)

caught_m{a val^n} B^{l+1}[rethrow l] end
  ↪ caught_m{a val^n} B^{l+1}[val^n (throw a)] end

caught_m{a val^n} val^m end  ↪  val^m
```

A keyword `all` is introduced to simplify the requirements for the `try` execution step below.

```
F; val^n (try bt instr* (catch x_i instr_i*)* (catch_all instr'*)? end)
  ↪  F; catch_m{a_i instr_i*}*{all instr'*}? (label_m{} val^n instr* end) end
  (iff bt = [t1^n] -> [t2^m] and (F_exn(x_i) = a_i)*)

catch_m{a? instr*}* val^m end ↪ val^m

S; F; catch_m{a1? instr*}{a'? instr'*}* T[val^n (throw a)] end
  ↪  S; F; caught_m{a val^n} (label_m{} val^n instr* end) end
  (iff (a1? = eps \/ a1? = a) /\ S_exn(a) = {type [t^n]->[]})

S; F; catch_m{a1? instr*}{a'? instr'*}* T[val^n (throw a)] end
  ↪  S; F; catch_m{a'? instr'*}* T[val^n (throw a)] end
  (iff a1? =/= eps /\ a1? =/= a)

S; F; catch_m T[val^n (throw a)] end
  ↪  S; F; val^n (throw a)


val^n (try bt instr* delegate l) ↪ delegate{l} (label_m{} val^n instr* end) end
  (iff bt = [t^n] -> [t^m])

B^l[ delegate{l} (T[val^n (throw a)]) end ] end
  ↪ val^n (throw a)


try bt instr* unwind instr'* end ↪ try bt instr* catch_all instr'* rethrow 0 end
```
