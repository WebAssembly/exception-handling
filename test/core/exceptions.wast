;; Test exception handling support

(module
  (event)
  (event (param i32))
)

(assert_invalid
  (module (event (result i32)))
  "non-empty event result type"
)
