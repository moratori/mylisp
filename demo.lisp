#定数的なのはdefconstで定義する
(defconst lst '(1 2 3 (2 4 (2 4 1 9 8) 2 3 0) 4 5))
(defconst factor 2)
(defconst x 10)
(defconst mult (lambda (x) (lambda (y) (* x y))))


#名前付きの関数は (define fname (arg1 arg2 ...) body) みたいな感じ

#(fact 5) -> 5!
(define fact (n)
	(if (= n 0)
		1
		(* n (fact (- n 1)))))

#(reverse '(1 2 3)) -> (3 2 1)
(define reverse (lst)
	(if (null? lst)
		nil
		(cons (last lst) (reverse (init lst)))))

#(delete '(2 3 4 (5 2 3) 2 9) 2) -> (3 4 (5 3) 9)
(define delete (lst factor)
	(if (null? lst)
		nil
		(if (list? (car lst))
			(cons (delete (car lst) factor) (delete (cdr lst) factor))
  			(if (equal? (car lst) factor)
				(delete (cdr lst) factor)
				(cons (car lst) (delete (cdr lst) factor))))))

#(append '(1 2 3) '(4 5 6)) -> (1 2 3 4 5 6)
(define append (lst1 lst2)
	(if (null? lst2)
		lst1
		(if (null? lst1)
			lst2
			(append (reverse (cons (car lst2) (reverse lst1))) (cdr lst2)))))


#(flatten '(1 2 (3 4 (5 6) 7) 8) ) -> (1 2 3 4 5 6 7 8)
(define flatten (lst)
	(if (null? lst)
		nil
		(if (list? (car lst))
			(append (flatten (car lst)) (flatten (cdr lst)))
			(cons (car lst) (flatten (cdr lst))))))

#(qsort '(2 3 0 -1 9 18)) -> (-1 0 2 3 9 18)
(define qsort (lst)
	(if (null? lst)
		nil
		((lambda (pv)
			(append
				(append
					(qsort (filter (lambda (x) (> pv x)) lst))
					(filter (lambda (x) (= x pv)) lst))
				(qsort(filter (lambda (x)(< pv x)) lst))))(car lst))))



(print lst)
(print (delete lst factor))
(print (reverse lst))
(print (fact x))
(print (append '(1 2 3) '(4 5)))
(print (flatten '(1 2 3 (3.1 3.2 3.3 (3.301 3.31) 3.4) 4 (4.01 4.02 (4.021 4.023) 4.03) 5)))
(print (qsort '(3 2 4 1)))
(print ((mult 3) 2))

#ラムダでfact
(print 
  ((lambda (n self)
	(if (= n 0)
			1
			(* n (self (- n 1) self)))) 5 

		(lambda (n self)
			(if (= n 0)
					1
					(* n (self (- n 1) self))))))
