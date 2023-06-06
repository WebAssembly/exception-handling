;; Test rethrow instruction.

(module
  (tag $e0)
  (tag $e1)

  (func (export "catch-rethrow-0")
    (try
      (do (throw $e0))
      (catch $e0 (rethrow))
    )
  )

  (func (export "catch-rethrow-1") (param i32) (result i32)
    (try (result i32)
      (do (throw $e0))
      (catch $e0
        (if (param exnref) (i32.eqz (local.get 0))
          (then (rethrow))
          (else (drop))
        )
        (i32.const 23)
      )
    )
  )

  (func (export "catchall-rethrow-0")
    (try
      (do (throw $e0))
      (catch_all (rethrow))
    )
  )

  (func (export "catchall-rethrow-1") (param i32) (result i32)
    (try (result i32)
      (do (throw $e0))
      (catch_all
        (if (param exnref) (i32.eqz (local.get 0))
          (then (rethrow))
          (else (drop))
        )
        (i32.const 23)
      )
    )
  )

  (func (export "rethrow-nested") (param i32) (result i32)
    (local $exn1 exnref)
    (local $exn2 exnref)
    (try (result i32)
      (do (throw $e1))
      (catch $e1
        (local.set $exn1)
        (try (result i32)
          (do (throw $e0))
          (catch $e0
            (local.set $exn2)
            (if (i32.eq (local.get 0) (i32.const 0)) (then (rethrow (local.get $exn1))))
            (if (i32.eq (local.get 0) (i32.const 1)) (then (rethrow (local.get $exn2))))
            (i32.const 23)
          )
        )
      )
    )
  )

  (func (export "rethrow-recatch") (param i32) (result i32)
    (local $e exnref)
    (try (result i32)
      (do (throw $e0))
      (catch $e0
        (local.set $e)
        (try (result i32)
         (do (if (i32.eqz (local.get 0)) (then (rethrow (local.get $e)))) (i32.const 42))
         (catch $e0 (drop) (i32.const 23))
        )
      )
    )
  )

  (func (export "rethrow-stack-polymorphism")
    (local $e exnref)
    (try (result f64)
      (do (throw $e0))
      (catch $e0 (local.set $e) (i32.const 1) (rethrow (local.get $e)))
    )
    (unreachable)
  )
)

(assert_exception (invoke "catch-rethrow-0"))

(assert_exception (invoke "catch-rethrow-1" (i32.const 0)))
(assert_return (invoke "catch-rethrow-1" (i32.const 1)) (i32.const 23))

(assert_exception (invoke "catchall-rethrow-0"))

(assert_exception (invoke "catchall-rethrow-1" (i32.const 0)))
(assert_return (invoke "catchall-rethrow-1" (i32.const 1)) (i32.const 23))
(assert_exception (invoke "rethrow-nested" (i32.const 0)))
(assert_exception (invoke "rethrow-nested" (i32.const 1)))
(assert_return (invoke "rethrow-nested" (i32.const 2)) (i32.const 23))

(assert_return (invoke "rethrow-recatch" (i32.const 0)) (i32.const 23))
(assert_return (invoke "rethrow-recatch" (i32.const 1)) (i32.const 42))

(assert_exception (invoke "rethrow-stack-polymorphism"))

(assert_invalid (module (func (rethrow))) "type mismatch")
(assert_invalid (module (func (block (rethrow)))) "type mismatch")
