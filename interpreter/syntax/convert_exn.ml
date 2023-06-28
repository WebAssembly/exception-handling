open Source
open Ast
open Types


type block =
{
  label : int32;            (* respective label's index after shift *)
  exnref : int32;           (* for catch blocks: local holding exnref (-1 otherwise) *)
  used : bool ref;          (* true if exnref is used *)
  handlers : (var * var) list * var option (* for try blocks: its handlers ([], -1 otherwise) *)
}

type env =
{
  blocks : block list;      (* control stack *)
  locals : int32;           (* number of original locals in function *)
  nest : int32;             (* current nesting depth of catch handlers *)
  maxnest : int32 ref;      (* maximum nesting depth of catch handlers *)
  types : type_ list ref;   (* types defined in module *)
  tags : func_type list;    (* tags defined in module *)
}


let (+$) = Int32.add
let (-$) = Int32.sub

let lookup_type' types x = (Lib.List32.nth !types x.it).it
let lookup_type (env : env) x = lookup_type' env.types x
let lookup_tag (env : env) x = Lib.List32.nth env.tags x.it
let lookup_block (env : env) l = Lib.List32.nth env.blocks l.it

let shift_handlers n (cs, ca) =
  ( List.map (fun (x, l) -> (x, (l.it +$ n) @@ l.at)) cs,
  	Option.map (fun l -> (l.it +$ n) @@ l.at) ca
  )
let shift_block n block = {block with label = block.label +$ n; handlers = shift_handlers n block.handlers}
let shift_env n env = {env with blocks = List.map (shift_block n) env.blocks}
let extend_env block env = {env with blocks = block :: (shift_env 1l env).blocks}


let convert_label env (l : var) : var =
  (lookup_block env l).label @@ l.at

let expand_block_type (env : env) bt : func_type =
  match bt with
  | ValBlockType None -> FuncType ([], [])
  | ValBlockType (Some t) -> FuncType ([], [t])
  | VarBlockType x -> lookup_type env x

let convert_block_type (env : env) ts1 ts2 at : block_type =
  let ft = FuncType (ts1, ts2 @ [RefType ExnRefType]) in
  if ft = FuncType ([], [RefType ExnRefType]) then
    ValBlockType (Some (RefType ExnRefType))
  else
	let y = Lib.List32.length !(env.types) in
    env.types := !(env.types) @ [ft @@ at];
    VarBlockType (y @@ at)

let rec convert_instr env (e : instr) : instr list =
  match e.it with
  | Br l ->
    [Br (convert_label env l) @@ l.at]
  | BrIf l ->
    [BrIf (convert_label env l) @@ l.at]
  | BrTable (ls, l) ->
    [BrTable (List.map (convert_label env) ls, convert_label env l) @@ l.at]
  | Rethrow_old l ->
    let block = lookup_block env l in
    block.used := true;
    [LocalGet (block.exnref @@ l.at) @@ e.at; Rethrow @@ e.at]
  | Block (bt, es) ->
    [Block (bt, convert_block env es) @@ e.at]
  | Loop (bt, es) ->
    [Loop (bt, convert_block env es) @@ e.at]
  | If (bt, es1, es2) ->
    [If (bt, convert_block env es1, convert_block env es2) @@ e.at]
  | Try (bt, cs, ca, es) ->
    [Try (bt, cs, ca, convert_block env es) @@ e.at]
  | TryDelegate_old (bt, es, l) ->
    let block = lookup_block env l in
    if block.handlers = ([], None) then
      failwith ("unsupported delegate at " ^ string_of_region e.at);
    let cs, ca = block.handlers in
    [Try (bt, cs, ca, convert_block env es) @@ e.at]
  | TryCatch_old (bt, es, cs, ca) ->
    let n = Lib.List32.length cs +$ Lib.List32.length (Option.to_list ca) in
    let env' = shift_env (n +$ 1l) env in
    let xs, ess = List.split cs in
    let ess' = List.map (convert_catch env' e.at) ess in
    let eso' = Option.map (convert_catch env' e.at) ca in
    let cs' = Lib.List32.mapi (fun i x -> (x, i @@ x.at)) xs in
    let ca' = Option.map (fun _ -> (n -$ 1l) @@ e.at) eso' in
    let block = {label = 0l; exnref = -1l; used = ref false; handlers = shift_handlers 1l (cs', ca')} in
    let es' = List.concat_map (convert_instr (extend_env block env')) es in
    let FuncType (ts1, _) = expand_block_type env bt in
    let body =
      [ Try (bt, cs', ca', es') @@ e.at;
        Br (n @@ e.at) @@ e.at
      ]
    in
    let catches, _ =
      List.fold_left (fun (inner, n) (x, es') ->
      	let n' = n -$ 1l in
      	let FuncType (ts2, _) = lookup_tag env x in
      	[Block (convert_block_type env ts1 ts2 x.at, inner) @@ e.at] @
      	es' @ [Br (n' @@ x.at) @@ e.at], n'
      ) (body, n) (List.combine xs ess')
    in
    let catch_all =
      Option.fold ~none:catches ~some:(fun es' ->
      	[Block (convert_block_type env ts1 [] e.at, catches) @@ e.at] @ es'
      ) eso'
    in
    [Block (bt, catch_all) @@ e.at]
  | _ ->
    [e]

and convert_block env (es : instr list) : instr list =
  let block = {label = 0l; exnref = -1l; used = ref false; handlers = [], None} in
  List.concat_map (convert_instr (extend_env block env)) es

and convert_catch env at (es : instr list) : instr list =
  let env' = {env with nest = env.nest +$ 1l} in
  let block = {label = 0l; exnref = env.locals +$ env.nest; used = ref false; handlers = [], None} in
  let es' = List.concat_map (convert_instr (extend_env block env')) es in
  if !(block.used) then
  ( env.maxnest := max !(env.maxnest) env'.nest;
    (LocalSet (block.exnref @@ at) @@ at) :: es'
  )
  else
    (Drop @@ at) :: es'


let convert_func env (f : func) : func =
  let FuncType (ts, _) = lookup_type env f.it.ftype in
  let nlocals = Lib.List32.length ts +$ Lib.List32.length f.it.locals in
  let env' = {env with locals = nlocals; maxnest = ref 0l} in
  let body = convert_block env' f.it.body in
  let locals = Lib.List32.make !(env'.maxnest) (RefType ExnRefType) in
  {f.it with locals = f.it.locals @ locals; body} @@ f.at

let convert_module (m : module_) : module_ =
  let types = ref m.it.types in
  let import_tags =
    List.filter_map (fun im ->
      match im.it.idesc.it with
      | TagImport x -> Some (lookup_type' types x)
      | _ -> None
    ) m.it.imports
  in
  let defined_tags =
    List.map (fun tg -> lookup_type' types tg.it.tgtype) m.it.tags
  in
  let env =
    { blocks = []; locals = 0l; nest = 0l; maxnest = ref 0l;
      types; tags = import_tags @ defined_tags;
    }
  in
  let funcs = List.map (convert_func env) m.it.funcs in
  {m.it with funcs; types = !types} @@ m.at
