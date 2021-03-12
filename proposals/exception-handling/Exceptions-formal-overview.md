# 3rd proposal formal spec overview

This is an overview of the 3rd proposal's formal spec additions, to aid in discussions concerning the proposed semantics.

## Abstract Syntax

### Types

Exception Types

```
exntype ::= [t*]→[]
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

#### Modification to labels

To verify that a `try...delegate l` instruction refers to a label surrounding the instructions of a try block (call this a try-label), introduce a `kind` attribute to labels in the validation context, which is set to `try` when the label is a try-label.

Similarly, to verify that the `rethrow l` instruction refers to a label surrounding the instructions of a catch block (call this a catch-label), we allow the `kind` attribute of labels in the validation context to be set to `catch` when the label is a catch-label. This addition is reflected in the execution rules, by the administrative instruction `caught` which introduces a label around the catching try-block.

The original notation `label [t*]` is now an abbreviation for:

````
label {result [t*], kind ε}
```


### Instructions


```
C.exns(x) = [t*]→[]
-----------------------------
C ⊢ throw x : [t1* t*]→[t2*]


C.labels(l).kind = catch
----------------------------
C ⊢ rethrow l : [t1*]→[t2*]


C.types(bt) = [t1*]→[t2*]
C, labels {result [t2*], kind try} ⊢ instr* : [t1*]→[t2*]
(C.exns(x) = [t*]→[] ∧
 C, labels { result [t2*], kind catch } ⊢ instr* : [t*]→[t2*])*
(C, labels { result [t2*], kind catch } ⊢ instr'* : []→[t2*])?
-----------------------------------------------------------------------------
C ⊢ try bt instr* (catch x instr'*)* (catch_all instr''*)? end : [t1*]→[t2*]


C.types(bt) = [t1*]→[t2*]
C, labels {result [t2*], kind try} ⊢ instr* : [t1*]→[t2*]
C.labels(l).kind = try
----------------------------------------------------------
C ⊢ try bt instr* delegate l : [t1*]→[t2*]


C.types(bt) = [t1*]→[t2*]
C, labels {result [t2*], kind try} ⊢ instr1* : [t1*]→[t2*]
C, labels [t2*] ⊢ instr2* : []→[]
-----------------------------------------------------------
C ⊢ try bt instr1* unwind instr2* end : [t1*]→[t2*]
```

## Execution (Reduction)

### Runtime structure

Stores

```
S ::= {..., exns exninst*}
```

Exception Instances

```
exninst ::= {type exntype}
```

Module Instances

```
m ::= {..., exns a*}
```

Administrative Instructions

```
instr ::= ... | throw a | catch_n{a? instr*}* instr* end
        | delegate{l} instr* end | caught_m{a val^n} instr* end
```

Throw Contexts

```
T ::= val* [_] instr* | label_n{instr*} T end | caught_m{a val^n} T end
   | frame_n{F} T end
```

### Instructions


```
F; throw x  ↪  F; throw a  (if F.module.exnaddrs[x]=a)

caught_m{a val^n} B^{l+1}[rethrow l] end
  ↪ caught_m{a val^n} B^{l+1}[val^n (throw a)] end

caught_m{a val^n} val^m end  ↪  val^m
```

A missing exception address in a `catch_m` clause (i.e., `a? = ε`) represents a `catch_all`.

```
F; val^n (try bt instr* (catch x instr'*)* (catch_all instr''*)? end)
  ↪  F; catch_m{a instr'*}*{instr''*}? (label_m{} val^n instr* end) end
  (iff bt = [t1^n]→[t2^m] ∧ (val:t1)^n ∧ (F.module.exnaddrs[x]=a)*)

catch_m{a? instr*}* val^m end ↪ val^m
```

In the below reduction, a try-label is replaced by a catch label (see comment in the end of this file).

```
S; F; catch_m{a1? instr*}{a'? instr'*}* (label_m T[val^n (throw a)] end) end
  ↪  S; F; caught_m{a val^n} (label_m{} (val^n)? instr* end) end
  (iff (a1? = ε ∨ a1? = a) ∧ S.exceptions(a).type = [t^n]→[])

S; F; catch_m{a1? instr*}{a'? instr'*}* T[val^n (throw a)] end
  ↪  S; F; catch_m{a'? instr'*}* T[val^n (throw a)] end
  (iff a1? ≠ ε ∧ a1? ≠ a)

S; F; catch_m T[val^n (throw a)] end
  ↪  S; F; val^n (throw a)


val^n (try bt instr* delegate l)
  ↪ delegate{l} (label_m{} val^n instr* end) end
  (iff bt = [t^n]→[t^m])

delegate{l} val^n end ↪ val^n

B^l[ delegate{l} T[val^n (throw a)] end ] end
  ↪ val^n (throw a)


try bt instr* unwind instr'* end
  ↪ try bt instr* catch_all instr'* rethrow 0 end
```

### Typing rules for administrative instructions

```
S.exceptions(a).type = [t*]→[]
-------------------------------
S;C ⊢ throw a : [t1* t*]→[t2*]

(S.exceptions(a).type = [t'*]→[] ∧
 S;C, labels {result [t*], kind catch} ⊢ instr1* : [t'*]→[t*])*
(S;C, labels {result [t*], kind catch} ⊢ instr2* : []→[t*])?
S;C, labels {result [t*], kind try} ⊢ instr3* : []→[t*]
---------------------------------------------------------------------------
S;C ⊢ catch_n{a instr1*}*{instr2*}? (label_n {} instr3* end) end : []→[t*]

S;C, label {result [t*], kind try} ⊢ instr* : []→[t*]
C_label(l).kind = try
-------------------------------------------------------
S;C ⊢ delegate{l} (label_m{} instr* end) end : []→[t*]

S.exceptions(a).type = [t*]→[]
(val:t)*
S;C, labels {result [t'*], kind catch} ⊢ instr* : []→[t'*]
---------------------------------------------------------------  [T-caught-adm]
S;C ⊢ caught_m{a val^n} (label_m{} instr* end) end : []→[t'*]
```

The above typing rules preserve types, because the manipulated labels (e.g. during `kind`-change)
are included in the conclusions of such type rules. So for example one could see

- `caught_m{...} (label_m {} ... end) end` as the catch-label (holding the caught exception),
- `catch_m{}*label_m{} ... end end` as a try-label (holding all its handlers), and
- `delegate{l} (label_m{} instr* end) end` as a try-label holding the destination (depth) to another try-label.
