(* Example: Fibonacci numbers *)
(* fib : int -> int *)
let rec fib (n : int) : int =
  if n < 2 then n
  else fib (n - 1) + fib (n - 2)

let () = print_endline (string_of_int (fib 10))
