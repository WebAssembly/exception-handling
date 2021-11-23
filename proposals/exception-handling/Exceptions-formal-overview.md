# 3rd proposal formal spec overview

This is an overview of the 3rd proposal's formal spec additions, to aid in discussions concerning the proposed semantics.

## Abstract Syntax

### Types

#### Tag Types

```
tagtype ::= [t*]→[]
```

### Instructions

```
instr ::= ... | throw tagidx | rethrow labelidx
        | try blocktype instr* (catch tagidx instr*)* (catch_all instr*)? end
        | try blocktype instr* delegate labelidx
```

### Modules

#### Tags

```
tag ::= export* tag tagtype  | export* tag tagtype import
```

#### Modules

```
mod ::= module ... tag*
```

## Validation (Typing)

#### Modification to labels

To verify that the `rethrow l` instruction refers to a label surrounding the instructions of a catch block (call this a catch-label), we introduce a `kind` attribute to labels in the validation context, which is set to `catch` when the label is a catch-label and empty otherwise.

```
labelkind ::= catch
labeltype ::= {result resulttype, kind labelkind?}
C ::= {..., labels labeltype}
```

The original notation `labels [t*]` is now an abbreviation for:

```
labels [t*] ::= labels {result [t*], kind ε}
```


### Instructions


```
C.tags[x] = [t*]→[]
-----------------------------
C ⊢ throw x : [t1* t*]→[t2*]


C.labels[l].kind = catch
----------------------------
C ⊢ rethrow l : [t1*]→[t2*]


C.types[bt] = [t1*]→[t2*]
C, labels [t2*] ⊢ instr* : [t1*]→[t2*]
(C.tags[x] = [t*]→[] ∧
 C, labels { result [t2*], kind catch } ⊢ instr'* : [t*]→[t2*])*
(C, labels { result [t2*], kind catch } ⊢ instr''* : []→[t2*])?
-----------------------------------------------------------------------------
C ⊢ try bt instr* (catch x instr'*)* (catch_all instr''*)? end : [t1*]→[t2*]


C.types[bt] = [t1*]→[t2*]
C, labels [t2*] ⊢ instr* : [t1*]→[t2*]
C.labels[l] = [t*]
-------------------------------------------
C ⊢ try bt instr* delegate l : [t1*]→[t2*]
```

## Execution (Reduction)

### Runtime structure

#### Stores

```
S ::= {..., tags taginst*}
```

#### Tag Instances

```
taginst ::= {type tagtype}
```

#### Module Instances

```
m ::= {..., tags tagaddr*}
```

#### Administrative Instructions

```
instr ::= ... | throw tagaddr | catch_n{ tagaddr? instr* }* instr* end
        | delegate{ labelidx } instr* end | caught_m{ tagaddr val^n } instr* end
```

#### Block contexts and label kinds

So far block contexts are only used in the reduction of `br l` and `return`, and only include labels or values on the stack above the hole. If we want to be able to break jumping over try-catch and try-delegate blocks, we must allow for the new administrative control instructions to appear after labels in block contexts.

```
B^0 ::= val* [_] instr*
B^k ::= catch_m{ tagaddr^? instr* }* B^k end | caught_m{ tagaddr val* } B^k end
      | delegate{ labelidx } B^k end
B^{k+1} ::= val* (label_n{instr*} B^k end) instr*
```

#### Throw Contexts

Throw contexts don't skip over handlers, they are used to match a thrown exception with the innermost handler.

```
T ::= val* [_] instr* | label_n{instr*} T end | caught_m{ tagaddr val^n } T end
   | frame_n{F} T end
```

Note that because `catch_n` instructions are not included above, there is always a unique maximal throw context.

### Reduction of instructions

Reduction steps for the new instructions or administrative instructions.

```
F; throw x  ↪  F; throw a  (if F.module.tagaddrs[x]=a)

caught_m{a val^n} B^l[rethrow l] end
  ↪ caught_m{a val^n} B^l[val^n (throw a)] end

caught_m{a val^n} val^m end  ↪  val^m
```

An absent tag address in a `handler` clause (i.e., `a? = ε`) represents a `catch_all`.

```
F; val^n (try bt instr* (catch x instr'*)* (catch_all instr''*)? end)
  ↪  F; label_m{} (catch_m{a instr'*}*{ε instr''*}? val^n instr* end) end
  (if bt = [t1^n]→[t2^m] ∧ (F.module.tagaddrs[x]=a)*)

catch_m{a? instr*}* val^m end ↪ val^m

S; F; catch_m{a1? instr*}{a'? instr'*}* T[val^n (throw a)] end
  ↪  S; F; caught_m{a val^n} (val^n)? instr* end
  (if (a1? = ε ∨ a1? = a) ∧ S.tags(a).type = [t^n]→[])

S; F; catch_m{a1? instr*}{a'? instr'*}* T[val^n (throw a)] end
  ↪  S; F; catch_m{a'? instr'*}* T[val^n (throw a)] end
  (if a1? ≠ ε ∧ a1? ≠ a)

S; F; catch_m T[val^n (throw a)] end
  ↪  S; F; val^n (throw a)


val^n (try bt instr* delegate l)
  ↪ label_m{} (delegate{l} val^n instr* end) end
  (if bt = [t^n]→[t^m])

delegate{l} val^n end ↪ val^n

label_m{} B^l[ delegate{l} T[val^n (throw a)] end ] end
  ↪ val^n (throw a)
```

Note that the last reduction step above is similar to the reduction of `br`.

### Typing rules for administrative instructions

```
S.tags[a].type = [t*]→[]
--------------------------------
S;C ⊢ throw a : [t1* t*]→[t2*]

((S.tags[a].type = [t'*]→[])?
 S;C, labels {result [t*], kind catch} ⊢ instr'* : [t'*?]→[t*])*
S;C, labels [t*] ⊢ instr* : []→[t*]
-----------------------------------------------------------------
S;C, labels [t*] ⊢ catch_n{a? instr'*}* instr* end : []→[t*]

S;C, labels [t*] ⊢ instr* : []→[t*]
C.labels[l] = [t'*]
------------------------------------------------------
S;C, labels [t*] ⊢ delegate{l} instr* end : []→[t*]

S.tags[a].type = [t'*]→[]
(val:t')*
S;C, labels {result [t*], kind catch} ⊢ instr* : []→[t*]
----------------------------------------------------------
S;C, labels [t*] ⊢ caught_m{a val^n} instr* end : []→[t*]
```

