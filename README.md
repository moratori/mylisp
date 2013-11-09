lispy
=====

lispもどきもどき. python製です

demo.lispを動かすとわかります

((lambda (n self)
	(if (= n 0)
			1
			(* n (self (- n 1) self)))) 5 

		(lambda (n self)
			(if (= n 0)
					1
					(* n (self (- n 1) self))))) ==> 120
