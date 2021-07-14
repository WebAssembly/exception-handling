# 3rd proposal formal spec overview

This is an overview of the 3rd proposal's formal spec additions, to aid in discussions concerning the proposed semantics.

## Abstract Syntax

### Types

Tag Types

```
tagtype ::= [t*]→[]
```

### Instructions

```
instr ::= ... | throw x | rethrow l
        | try bt instr* (catch x instr*)* (catch_all instr*)? end
        | try bt instr* delegate l
```

### Modules

Tags

```
tag ::= export* tag tagtype  | export* tag tagtype import
```

Modules

```
mod ::= module ... tag*
```

## Validation (Typing)

#### Modification to labels

To verify that a `try...delegate l` instruction refers to a label surrounding the instructions of a try block (call this a try-label), introduce a `kind` attribute to labels in the validation context, which is set to `try` when the label is a try-label.

Similarly, to verify that the `rethrow l` instruction refers to a label surrounding the instructions of a catch block (call this a catch-label), we allow the `kind` attribute of labels in the validation context to be set to `catch` when the label is a catch-label.
labelkind ::= try | catch
labeltype ::= {result resulttype, kind labelkind?}
C ::= {..., labels labeltype}
The original notation `labels [t*]` is now an abbreviation for:

```
labels {result [t*], kind ε}
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
C, labels {result [t2*], kind try} ⊢ instr* : [t1*]→[t2*]
(C.tags[x] = [t*]→[] ∧
 C, labels { result [t2*], kind catch } ⊢ instr* : [t*]→[t2*])*
(C, labels { result [t2*], kind catch } ⊢ instr'* : []→[t2*])?
-----------------------------------------------------------------------------
C ⊢ try bt instr* (catch x instr'*)* (catch_all instr''*)? end : 	[t1*]→[t2*]


C.types[bt] = [t1*]→[t2*]
C, labels {result [t2*], kind try} ⊢ instr* : [t1*]→[t2*]
C.labels[l].kind = try
----------------------------------------------------------
C ⊢ try bt instr* delegate l : [t1*]→[t2*]
```

## Execution (Reduction)

### Runtime structure

Stores

```
S ::= {..., tags taginst*}
```

Tag Instances

```
taginst ::= {type tagtype}
```

Module Instances

```
m ::= {..., tags a*}
```

Administrative Instructions

```
instr ::= ... | throw a | catch_n{a? instr*}* instr* end
        | delegate{l} instr* end | caught_m{a val^n} instr* end
```

Block contexts and label kinds

So far block contexts are only used in the reduction of `br l` and `return`, and only include labels or values on the stack above the hole. If we want to be able to break jumping over try-catch and try-delegate blocks, we must allow for the new administrative control instructions to appear after labels in block contexts, mirroring the label kinds of labels in validation contexts.

```
B^k ::= val* B'^k instr*
B'^0 ::= [_]
B'^{k+1} ::= label_n{instr*} B^k end | catch_m{a? instr*}* B^{k+1} end | caught_m{a val*} B^{k+1} end | delegate{l} B^{k+1} end
```

Note that `label_n{instr*} label_kind? [_] end? end` could be seen as a simplified control frame.

(Alternatively, we could have the above `label_kind`s be also labels,  remove the additional `label_m` from the execution rules below, and remove the execution rules below where the new administrative instructions only contain `val*`. This would make labels even more similar to control frames.)

Throw Contexts

```
T ::= val* [_] instr* | label_n{instr*} T end | caught_m{a val^n} T end
   | frame_n{F} T end
```

### Instructions


```
F; throw x  ↪  F; throw a  (if F.module.tagaddrs[x]=a)

caught_m{a val^n} B^l[rethrow l] end
  ↪ caught_m{a val^n} B^l[val^n (throw a)] end

caught_m{a val^n} val^m end  ↪  val^m
```

An absent tagaddr in a `catch_m` clause (i.e., `a? = ε`) represents a `catch_all`.

```
F; val^n (try bt instr* (catch x instr'*)* (catch_all instr''*)? end)
  ↪  F; label_m{} (catch_m{a instr'*}*{instr''*}? val^n instr* end) end
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

B^l[ delegate{l} T[val^n (throw a)] end ]
  ↪ val^n (throw a)
```

### Typing rules for administrative instructions

```
S.tags[a].type = [t*]→[]
--------------------------------
S;C ⊢ throw a : [t1* t*]→[t2*]

((S.tags[a].type = [t'*]→[])?
 S;C, labels {result [t*], kind catch} ⊢ instr'* : [t'*?]→[t*])*
S;C, labels {result [t*], kind try} ⊢ instr* : []→[t*]
-----------------------------------------------------------------------
S;C, labels [t*] ⊢ catch_n{a? instr'*}* instr* end : []→[t*]

S;C, labels {result [t*], kind try} ⊢ instr* : []→[t*]
C.labels[l].kind = try
-----------------------------------------------------------------------
S;C, labels [t*] ⊢ delegate{l} instr* end : []→[t*]

S.tags[a].type = [t'*]→[]
(val:t')*
S;C, labels {result [t*], kind catch} ⊢ instr* : []→[t*]
--------------------------------------------------------------------------------
S;C, labels [t*] ⊢ caught_m{a val^n} instr* end : []→[t'*]
```

By adding the attribute `kind` to labels, we are creating situations in the proof of type preservation, where we have a derivation of some `S;C, label [t*] ⊢ instr* : []→[t*]` but we need to have that `S;C, label {result [t*], kind <labelkind>} ⊢ instr* : []→[t*]` for some `<labelkind> ::= try | catch`. To resolve this we add the following typing rule for labels in the context, which ensures our newly introduced `try` and `catch` blocks can contain any instructions a regular block can.

```
S;C, label [t*] ⊢ instr* : []→[t*]
labelkind = try ∨ labelkind = catch
-----------------------------------------------------------
S;C, label {result [t*], kind labelkind} ⊢ instr* : []→[t*]
```
