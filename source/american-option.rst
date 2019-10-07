""""""""""""""""""""""""""""""""""""""""""""""""""""""""
American Option
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

An *option* is a financial contract that allows an investor to exercise a choice
between two subcontracts. 
We implement in BitML the *American option*,
where the investor can exercise the choice anytime before a given deadline.

We start by defining the parametric contract :bitml:`(AmericanOption Part t Contract1 Contract2 Default)`.
The parameter of the contract are: a participant ``Part`` who can choose, before deadline ``t``, 
to authorise the either ``Contract1`` or ``Contract2``.
If time ``t`` passes, the contract can proceed as the parameter contract ``Default``.

We exploit the American Option to implement an investment contract between 
an investor ``A`` and an issuer ``I``.
After stipulating the contract, ``A`` can choose whether to invest, or to retract.
If she authorise the contract ``Invest``, 
she immediately pays her 1 BTC deposit to ``I``, expecting to get back 1.1 BTC
from ``I`` after block 160000000.
If she authorise the contract ``Retract``, she does not invest,
but she only gets back 0.95 BTC, paying 0.05 BTC to ``I`` as a fee.
Otherwise, if she doesn't chose before the deadline ``t`` , 
``I`` can invoke the contract ``Default``, 
which returns ``A``'s deposit to her, minus a 0.1 BTC penalty,
which goes to ``I``.

Finally, we verify that the contract is liquid.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "I" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(debug-mode)

	(define (txA) ".")
	(define (txFee) "..")
	(define (txI) "...")


	;; Part can choose at time t whether to execute Contract1 or Contract2
	;; after deadline t, the contract Default can be executed
	;--------------------------------------------------------------
	(define (AmericanOption Part t Contract1 Contract2 Default)
	  (choice
	   (auth Part (tau (ref (Contract1))))
	   (auth Part (tau (ref (Contract2))))
	   (after t (tau (ref (Default))))))

	; Sub-contracts used to instantiate the American Option
	;--------------------------------------------------------------

	;; A chooses not to proceed with the investment,
	;; and gets back her deposit minus a cancellation fee.
	;; I gets gets the fee from A.
	(define (Retract)
	  (split
	   (0.95 -> (withdraw "A"))
	   (0.05 -> (withdraw "I"))))

	;; A chooses to proceed with the investment.
	;; The funds are locked up to a certain time,
	;; then she can withdraw the whole balance
	(define (Invest)
	  (split
	   (1 -> (withdraw "I"))
	   (0 -> (after 160000000 (put (x) (withdraw "A"))))))

	;; A failed to choose whether to invest or retract.
	;; She gets back her deposit minus a penalty.
	;; I gets gets the penalty from A.
	(define (Default)
	  (split
	   (0.9 -> (withdraw "A"))
	   (0.1 -> (withdraw "I"))))
	;--------------------------------------------------------------

	(contract
	 (pre (deposit "A" 1 (ref (txA)))
	      (vol-deposit "I" x 1.1 (ref (txI)))
	      (fee "A" 0.01 (ref (txFee))))
	 
	 (ref (AmericanOption "A" 1550000 Retract Invest Default))
	 
	 (check-liquid))

This is the result of the compilation.

.. code-block:: balzac

	const pubkeyA13 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI2 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA11 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA1 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA9 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA7 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI10 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI6 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI8 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA3 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA5 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA15 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI12 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI4 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI14 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI16 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const sigA0 : signature = _ //add signature for output .
	const sigAFee : signature = _ //add signature for output ..

	transaction Tinit { 
	 input = [ .:sigA0; ..:sigAFee ] 
	 output = 1.0097 BTC : fun(sA, sI) . (( versig(pubkeyA1, pubkeyI2; sA, sI) ||
	 versig(pubkeyA3, pubkeyI4; sA, sI) ||
	 versig(pubkeyA5, pubkeyI6; sA, sI) )) 
	}

	const sigAT1 : signature = _ 
	const sigIT1 : signature = _ 


	transaction T1 { 
	 input = [ Tinit@0: sigAT1 sigIT1 ] 
	 output = 1.0094 BTC : fun(sA, sI) . versig(pubkeyA7, pubkeyI8; sA, sI) 
	}

	const sigAT2 : signature = _ 
	const sigIT2 : signature = _ 


	transaction T2 { 
	 input = [ T1@0: sigAT2 sigIT2 ] 
	 output = [ 0.95455 BTC : fun(sA, sI) . ((versig(pubkeyA9, pubkeyI10; sA, sI)));
		0.05455 BTC : fun(sA, sI) . ((versig(pubkeyA11, pubkeyI12; sA, sI))) ] 
	}

	const sigAT3 : signature = _ 
	const sigIT3 : signature = _ 

	transaction T3 { 
	 input = [ T2@0:  sigAT3 sigIT3 ] 
	 output = 0.95425 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigAT4 : signature = _ 
	const sigIT4 : signature = _ 

	transaction T4 { 
	 input = [ T2@1:  sigAT4 sigIT4 ] 
	 output = 0.05425 BTC : fun(x) . versig(pubkeyI; x) 
	 
	}

	const sigAT5 : signature = _ 
	const sigIT5 : signature = _ 


	transaction T5 { 
	 input = [ Tinit@0: sigAT5 sigIT5 ] 
	 output = 1.0094 BTC : fun(sA, sI) . versig(pubkeyA13, pubkeyI14; sA, sI) 
	}

	const sigAT6 : signature = _ 
	const sigIT6 : signature = _ 


	transaction T6 { 
	 input = [ T5@0: sigAT6 sigIT6 ] 
	 output = [ 1.00455 BTC : fun(sA, sI) . ((versig(pubkeyA11, pubkeyI12; sA, sI)));
		0.00455 BTC : fun(sA, sI) . ((versig(pubkeyA15, pubkeyI16; sA, sI))) ] 
	}

	const sigAT7 : signature = _ 
	const sigIT7 : signature = _ 

	transaction T7 { 
	 input = [ T6@0:  sigAT7 sigIT7 ] 
	 output = 1.00425 BTC : fun(x) . versig(pubkeyI; x) 
	 
	}

	const sigx : signature = _ //add signature for output ...
	const sigAT8 : signature = _ 
	const sigIT8 : signature = _ 


	transaction T8 { 
	 input = [ T6@1: sigAT8 sigIT8 ] 
	 output = 1.10425 BTC : fun(sA, sI) . versig(pubkeyA9, pubkeyI10; sA, sI) 
	}

	const sigAT9 : signature = _ 
	const sigIT9 : signature = _ 

	transaction T9 { 
	 input = [ T8@0:  sigAT9 sigIT9 ] 
	 output = 1.10395 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigAT10 : signature = _ 
	const sigIT10 : signature = _ 


	transaction T10 { 
	 input = [ Tinit@0: sigAT10 sigIT10 ] 
	 output = 1.0094 BTC : fun(sA, sI) . versig(pubkeyA11, pubkeyI12; sA, sI) 
	}

	const sigAT11 : signature = _ 
	const sigIT11 : signature = _ 

	transaction T11 { 
	 input = [ T10@0:  sigAT11 sigIT11 ] 
	 output = 1.0091 BTC : fun(x) . versig(pubkeyI; x) 
	 
	}

