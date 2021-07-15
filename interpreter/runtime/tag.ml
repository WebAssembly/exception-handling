open Types

type tagaddr = int
type tag = {ty : func_type; addr : tagaddr}
type t = tag

let addr = ref 0

let alloc ty =
   let cur_addr = !addr in
   incr addr;
   {ty; addr = cur_addr}

let type_of tg =
  tg.ty

let addr_of tg =
  tg.addr
