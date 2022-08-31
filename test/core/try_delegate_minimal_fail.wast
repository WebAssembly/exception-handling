;; This test fails with the first approach to changing the position of the
;; delegate label. We could ommit the outermost try-catch_all, and get the
;; error:
;;
;;   uncaught exception: uncaught exception with args ([])
;;
;; As it is now, the error is:
;;
;;   Result: 27 : i32
;;   Expect: 2 : i32
;;   ../test/core/try_delegate_minimal_fail.wast:22.1-22.77: assertion failure: wrong return values
;;
;; These errors indicate that the delegated exception escaped its target and was
;; caught by the one surrounding it.


(module
  (tag $tag)
  (func (export "delegate-throw-direct") (param i32) (result i32)
    (try $outermost (result i32)
      (do
        (try $innermost (result i32)
          (do
            (try (result i32)
              (do
                (local.get 0)
                (if (then (throw $tag)) (else))
                (i32.const 1))
              (delegate $innermost)))  ;; delegate 0
          (catch $tag (i32.const 2)))) ;; end innermost
      (catch $tag (i32.const 27)))))   ;; end outermost

(assert_return (invoke "delegate-throw-direct" (i32.const 1)) (i32.const 2))
