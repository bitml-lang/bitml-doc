===============================
Auction
===============================

This is an auction contract between a seller ``S``, and two bidders, ``A`` and ``B``.
``S`` is selling an item with a "buy me now" price of 2 BTC, and the bidders can bid 1 or 2 BTC.

At the beginning of the contract, each bidder has the possibility to start the auction, bidding 1 BTC.
If no one bids before the deadline of block 155000000, the auction is voided and the deposits are sent back to the owners.
Otherwise, if ``A`` or ``B`` bid, the auction is now running and the contract progresses as defined in :bitml:`(RunningAuction1 hB lB)`.

From now on, the participant who bid is referred as ``hB`` (highest bidder), the other one as ``lB`` (lowest bidder).
Now, if ``lB`` forfeits, so ``hB`` wins the auction and has to pay 1 BTC to ``S``. 
Otherwise, ``A`` or ``B`` can raise the bid to 2 BTC. The first one to do so wins, and has to pay 2 BTC to ``S``. 
If no action is done before the deadline of block 155100000, ``hB`` wins.

We verify the strategy-less liquidity of this contract, which holds.

.. code-block:: bitml

	#lang bitml

	(debug-mode)

	(participant "A" "029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced")
	(participant "B" "022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30")
	(participant "S" "022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30") ; seller

	; auction with 2 rounds
	; possible bets 1, 2
	; 2 is the "buy me now" price

	; hB = highest bidder, lB = lowest bidder
	(define (RunningAuction1 hB lB)
	  (tau (choice
	        (auth "A" (ref (WonAuction2 "A" "B")))        ; A wins!
	        (auth "B" (ref (WonAuction2 "B" "A")))        ; B wins!
	        (auth lB (ref (WonAuction1 hB lB)))           ; lB forfeits
	        (after 155100000 (ref (WonAuction1 hB lB)))          ; hB wins - timeout
	        ))
	  )

	(define (WonAuction1 hB lB)
	  (tau (split (1 -> (withdraw "S")) (1 -> (withdraw hB)) (2 -> (withdraw lB)))))

	(define (WonAuction2 hB lB)
	  (tau (split (2 -> (withdraw "S")) (2 -> (withdraw lB)))))


	(contract (pre
	           (deposit "A" 2 "txA@0")
	           (deposit "B" 2 "txB@0"))

	          (choice
	           (auth "A" (ref (RunningAuction1 "A" "B")))  ; A bids first
	           (auth "B" (ref (RunningAuction1 "B" "A")))  ; B bids first
	           (after 155000000 (split (2 -> (withdraw "A")) (2 -> (withdraw "B"))))
	           )

	          (check-liquid)
	          )

These are the compiled transactions.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-liquid)

	WARNING: Using default secrets 
	(())

	Result: true
	Model checking time: 4965.0 ms
	=============================================================================*/


	const pubkeyS6 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB37 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB28 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA44 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS21 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS9 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB34 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA29 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyA47 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS33 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB31 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB7 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS18 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS12 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS3 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA35 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS24 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB10 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS48 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA26 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS39 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB13 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB46 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA20 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS27 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA38 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyA41 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyA8 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS45 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB22 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB40 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB16 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA23 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyB4 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA17 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyB43 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB1 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS36 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyB19 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA2 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS30 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA5 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS15 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA32 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyA14 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyB25 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyS42 = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA11 = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced

	const pubkeyB = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30
	const pubkeyA = pubkey:029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced
	const pubkeyS = pubkey:022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30

	const sigB0 : signature = _ //add signature for output txB@0
	const sigA1 : signature = _ //add signature for output txA@0

	transaction Tinit { 
	 input = [ txB@0:sigB0; txA@0:sigA1;  ] 
	 output = 4 BTC : fun(sB, sA, sS) . (( versig(pubkeyB1, pubkeyA2, pubkeyS3; sB, sA, sS) ||
	 versig(pubkeyB4, pubkeyA5, pubkeyS6; sB, sA, sS) ||
	 versig(pubkeyB7, pubkeyA8, pubkeyS9; sB, sA, sS) )) 
	}

	const sigBT1 : signature = _ 
	const sigAT1 : signature = _ 
	const sigST1 : signature = _ 


	transaction T1 { 
	 input = [ Tinit@0: sigBT1 sigAT1 sigST1 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB10, pubkeyA11, pubkeyS12; sB, sA, sS) || versig(pubkeyB13, pubkeyA14, pubkeyS15; sB, sA, sS) || versig(pubkeyB16, pubkeyA17, pubkeyS18; sB, sA, sS) || versig(pubkeyB19, pubkeyA20, pubkeyS21; sB, sA, sS) 
	}

	const sigBT2 : signature = _ 
	const sigAT2 : signature = _ 
	const sigST2 : signature = _ 


	transaction T2 { 
	 input = [ T1@0: sigBT2 sigAT2 sigST2 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB22, pubkeyA23, pubkeyS24; sB, sA, sS) 
	}

	const sigBT3 : signature = _ 
	const sigAT3 : signature = _ 
	const sigST3 : signature = _ 


	transaction T3 { 
	 input = [ T2@0: sigBT3 sigAT3 sigST3 ] 
	 output = [ 2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS))) ] 
	}

	const sigBT4 : signature = _ 
	const sigAT4 : signature = _ 
	const sigST4 : signature = _ 

	transaction T4 { 
	 input = [ T3@0:  sigBT4 sigAT4 sigST4 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT5 : signature = _ 
	const sigAT5 : signature = _ 
	const sigST5 : signature = _ 

	transaction T5 { 
	 input = [ T3@1:  sigBT5 sigAT5 sigST5 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT6 : signature = _ 
	const sigAT6 : signature = _ 
	const sigST6 : signature = _ 


	transaction T6 { 
	 input = [ T1@0: sigBT6 sigAT6 sigST6 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB31, pubkeyA32, pubkeyS33; sB, sA, sS) 
	}

	const sigBT7 : signature = _ 
	const sigAT7 : signature = _ 
	const sigST7 : signature = _ 


	transaction T7 { 
	 input = [ T6@0: sigBT7 sigAT7 sigST7 ] 
	 output = [ 2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS))) ] 
	}

	const sigBT8 : signature = _ 
	const sigAT8 : signature = _ 
	const sigST8 : signature = _ 

	transaction T8 { 
	 input = [ T7@0:  sigBT8 sigAT8 sigST8 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT9 : signature = _ 
	const sigAT9 : signature = _ 
	const sigST9 : signature = _ 

	transaction T9 { 
	 input = [ T7@1:  sigBT9 sigAT9 sigST9 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT10 : signature = _ 
	const sigAT10 : signature = _ 
	const sigST10 : signature = _ 


	transaction T10 { 
	 input = [ T1@0: sigBT10 sigAT10 sigST10 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB37, pubkeyA38, pubkeyS39; sB, sA, sS) 
	}

	const sigBT11 : signature = _ 
	const sigAT11 : signature = _ 
	const sigST11 : signature = _ 


	transaction T11 { 
	 input = [ T10@0: sigBT11 sigAT11 sigST11 ] 
	 output = [ 1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS))) ] 
	}

	const sigBT12 : signature = _ 
	const sigAT12 : signature = _ 
	const sigST12 : signature = _ 

	transaction T12 { 
	 input = [ T11@0:  sigBT12 sigAT12 sigST12 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT13 : signature = _ 
	const sigAT13 : signature = _ 
	const sigST13 : signature = _ 

	transaction T13 { 
	 input = [ T11@1:  sigBT13 sigAT13 sigST13 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT14 : signature = _ 
	const sigAT14 : signature = _ 
	const sigST14 : signature = _ 

	transaction T14 { 
	 input = [ T11@2:  sigBT14 sigAT14 sigST14 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT15 : signature = _ 
	const sigAT15 : signature = _ 
	const sigST15 : signature = _ 


	transaction T15 { 
	 input = [ T1@0: sigBT15 sigAT15 sigST15 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB37, pubkeyA38, pubkeyS39; sB, sA, sS) 
	}

	const sigBT16 : signature = _ 
	const sigAT16 : signature = _ 
	const sigST16 : signature = _ 


	transaction T16 { 
	 input = [ T15@0: sigBT16 sigAT16 sigST16 ] 
	 output = [ 1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS))) ] 
	}

	const sigBT17 : signature = _ 
	const sigAT17 : signature = _ 
	const sigST17 : signature = _ 

	transaction T17 { 
	 input = [ T16@0:  sigBT17 sigAT17 sigST17 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT18 : signature = _ 
	const sigAT18 : signature = _ 
	const sigST18 : signature = _ 

	transaction T18 { 
	 input = [ T16@1:  sigBT18 sigAT18 sigST18 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT19 : signature = _ 
	const sigAT19 : signature = _ 
	const sigST19 : signature = _ 

	transaction T19 { 
	 input = [ T16@2:  sigBT19 sigAT19 sigST19 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT20 : signature = _ 
	const sigAT20 : signature = _ 
	const sigST20 : signature = _ 


	transaction T20 { 
	 input = [ Tinit@0: sigBT20 sigAT20 sigST20 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB10, pubkeyA11, pubkeyS12; sB, sA, sS) || versig(pubkeyB13, pubkeyA14, pubkeyS15; sB, sA, sS) || versig(pubkeyB40, pubkeyA41, pubkeyS42; sB, sA, sS) || versig(pubkeyB43, pubkeyA44, pubkeyS45; sB, sA, sS) 
	}

	const sigBT21 : signature = _ 
	const sigAT21 : signature = _ 
	const sigST21 : signature = _ 


	transaction T21 { 
	 input = [ T20@0: sigBT21 sigAT21 sigST21 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB22, pubkeyA23, pubkeyS24; sB, sA, sS) 
	}

	const sigBT22 : signature = _ 
	const sigAT22 : signature = _ 
	const sigST22 : signature = _ 


	transaction T22 { 
	 input = [ T21@0: sigBT22 sigAT22 sigST22 ] 
	 output = [ 2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS))) ] 
	}

	const sigBT23 : signature = _ 
	const sigAT23 : signature = _ 
	const sigST23 : signature = _ 

	transaction T23 { 
	 input = [ T22@0:  sigBT23 sigAT23 sigST23 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT24 : signature = _ 
	const sigAT24 : signature = _ 
	const sigST24 : signature = _ 

	transaction T24 { 
	 input = [ T22@1:  sigBT24 sigAT24 sigST24 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT25 : signature = _ 
	const sigAT25 : signature = _ 
	const sigST25 : signature = _ 


	transaction T25 { 
	 input = [ T20@0: sigBT25 sigAT25 sigST25 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB31, pubkeyA32, pubkeyS33; sB, sA, sS) 
	}

	const sigBT26 : signature = _ 
	const sigAT26 : signature = _ 
	const sigST26 : signature = _ 


	transaction T26 { 
	 input = [ T25@0: sigBT26 sigAT26 sigST26 ] 
	 output = [ 2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS))) ] 
	}

	const sigBT27 : signature = _ 
	const sigAT27 : signature = _ 
	const sigST27 : signature = _ 

	transaction T27 { 
	 input = [ T26@0:  sigBT27 sigAT27 sigST27 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT28 : signature = _ 
	const sigAT28 : signature = _ 
	const sigST28 : signature = _ 

	transaction T28 { 
	 input = [ T26@1:  sigBT28 sigAT28 sigST28 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT29 : signature = _ 
	const sigAT29 : signature = _ 
	const sigST29 : signature = _ 


	transaction T29 { 
	 input = [ T20@0: sigBT29 sigAT29 sigST29 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB46, pubkeyA47, pubkeyS48; sB, sA, sS) 
	}

	const sigBT30 : signature = _ 
	const sigAT30 : signature = _ 
	const sigST30 : signature = _ 


	transaction T30 { 
	 input = [ T29@0: sigBT30 sigAT30 sigST30 ] 
	 output = [ 1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS))) ] 
	}

	const sigBT31 : signature = _ 
	const sigAT31 : signature = _ 
	const sigST31 : signature = _ 

	transaction T31 { 
	 input = [ T30@0:  sigBT31 sigAT31 sigST31 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT32 : signature = _ 
	const sigAT32 : signature = _ 
	const sigST32 : signature = _ 

	transaction T32 { 
	 input = [ T30@1:  sigBT32 sigAT32 sigST32 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT33 : signature = _ 
	const sigAT33 : signature = _ 
	const sigST33 : signature = _ 

	transaction T33 { 
	 input = [ T30@2:  sigBT33 sigAT33 sigST33 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT34 : signature = _ 
	const sigAT34 : signature = _ 
	const sigST34 : signature = _ 


	transaction T34 { 
	 input = [ T20@0: sigBT34 sigAT34 sigST34 ] 
	 output = 4 BTC : fun(sB, sA, sS) . versig(pubkeyB46, pubkeyA47, pubkeyS48; sB, sA, sS) 
	}

	const sigBT35 : signature = _ 
	const sigAT35 : signature = _ 
	const sigST35 : signature = _ 


	transaction T35 { 
	 input = [ T34@0: sigBT35 sigAT35 sigST35 ] 
	 output = [ 1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB25, pubkeyA26, pubkeyS27; sB, sA, sS)));
		1 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS))) ] 
	}

	const sigBT36 : signature = _ 
	const sigAT36 : signature = _ 
	const sigST36 : signature = _ 

	transaction T36 { 
	 input = [ T35@0:  sigBT36 sigAT36 sigST36 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyS; x) 
	 
	}

	const sigBT37 : signature = _ 
	const sigAT37 : signature = _ 
	const sigST37 : signature = _ 

	transaction T37 { 
	 input = [ T35@1:  sigBT37 sigAT37 sigST37 ] 
	 output = 1 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	const sigBT38 : signature = _ 
	const sigAT38 : signature = _ 
	const sigST38 : signature = _ 

	transaction T38 { 
	 input = [ T35@2:  sigBT38 sigAT38 sigST38 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT39 : signature = _ 
	const sigAT39 : signature = _ 
	const sigST39 : signature = _ 


	transaction T39 { 
	 input = [ Tinit@0: sigBT39 sigAT39 sigST39 ] 
	 output = [ 2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB34, pubkeyA35, pubkeyS36; sB, sA, sS)));
		2 BTC : fun(sB, sA, sS) . ((versig(pubkeyB28, pubkeyA29, pubkeyS30; sB, sA, sS))) ] 
	 absLock = block 10
	}

	const sigBT40 : signature = _ 
	const sigAT40 : signature = _ 
	const sigST40 : signature = _ 

	transaction T40 { 
	 input = [ T39@0:  sigBT40 sigAT40 sigST40 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT41 : signature = _ 
	const sigAT41 : signature = _ 
	const sigST41 : signature = _ 

	transaction T41 { 
	 input = [ T39@1:  sigBT41 sigAT41 sigST41 ] 
	 output = 2 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}