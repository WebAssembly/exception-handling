open Types

type tagaddr
type tag
type t = tag

val alloc : func_type -> tag
val type_of : tag -> func_type
val addr_of : tag -> tagaddr
