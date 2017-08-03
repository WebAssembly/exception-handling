(module
 (exception $empty_exception (func))
 
 (func (export "throw_unconditional")
       (throw 0))

 (func (export "try_catch_all") (result i32)
       (try i32
	(i32.const 1)
	(catch_all
	 (i32.const 0))))
 
  (func (export "try_catch_all_throw") (result i32)
       (try i32
	(throw 0)
	(catch_all
	 (i32.const 0)))))

(assert_trap (invoke "throw_unconditional") "webassembly exception")
(assert_return (invoke "try_catch_all") (i32.const 1))
(assert_return (invoke "try_catch_all_throw") (i32.const 0))
