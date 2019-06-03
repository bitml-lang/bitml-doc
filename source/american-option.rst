""""""""""""""""""""""""""""""""""""""""""""""""""""""""
American Option
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

An option is a financial contract that allows a participant to exercise a choice
between to subcontracts. 
We implement in BitML the American flavour, where the participant can choose anytime 
before a given deadline.

We start by defining the parametric contract :bitml:`(ExecuteBefore t Contract)`.
It takes two parameters: a deadline ``t``, expressed as block number,
and the ``Contract`` which has to be executed before ``t``.
After the deadline, the balance of the contract can be split between the participants.

Then, we define the parametric contract :bitml:`(AmericanOption Part t Contract1 Contract2)`.
It takes the participant ``Part`` who can choose which branch to take,
a deadline ``t``, and two subcontract, ``Contract1`` and ``Contract2``.
``Part`` can choose before ``t`` to proceed either with ``Contract1`` or ``Contract2``.

Finally, in the :bitml:`(contract ...)` expression, 
we instantiate the american option with
:bitml:`(AmericanOption "A" 1550000 (withdraw "A") (withdraw "I"))`.
We also check if the contract is liquid, assuming that Alice's
strategy is to authorize either branch, 
using :bitml:`check-liquid (strategy "A" (do-auth)))`.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "I" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(debug-mode)

	(define (txA) "tx:0200000001fbcee70062cab1cbe78f158851ee2351b3ce7d549201ac9f87c961225fb7ce4600000000e5483045022100fff909e25bcc800deebce554eb24b68080f2b02290b41076ad5cfb8b026453740220725b65455de27a643d74ac2deeccc3cb2bb3ba5c486bd19a2fc7c9034228e0f801483045022100fd976972a047c57e22b791c19d1ffdad25a9fb5240278cb923626d0285f6de0c02200820d34a98f7c7cc658412ec7053b3f14709ff86fd5b4532a46419181cfbbbaf014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff011a760c00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0")
	(define (txFee) "tx:0200000001c75e1b501f7a1691b16d06398b4235ab35e11ccda3c3f9160d68739c84d435ed00000000e4483045022100ad5f0022e6ae8e789a97ca9497b8d307690b96ddbfcdf822711b1983b328d26702204f276374584292322c1ad33dc7b67600673ace464e9c60990de7a0123933803c014730440220055c42ae93321b4061055c782be11d3392c84ff34b1d4fbbe3a9e208f63518170220231d7712a4d36e5397264bfc8db89fd1d13d64937ee886fb9872f260bf979760014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0")

	;; parties agree to execute the Contract before t
	(define (ExecuteBefore t Contract)
	  (choice
	   Contract
	   (after t (split (0.00408333 -> (withdraw "A"))
	                   (0.00408333 -> (withdraw "I"))))))

	;; Part can choose at time t whether to execute Contract1 or Contract2
	(define (AmericanOption Part t Contract1 Contract2)
	  (choice
	   (auth Part (tau (ref (ExecuteBefore t Contract1))))
	   (auth Part (tau (ref (ExecuteBefore t Contract2))))))

	(contract
	 (pre (deposit "A" 0.00816666 (ref (txA)))
	      (deposit "A" 0.00453333 (ref (txFee))))
	 
	 (ref (AmericanOption "A" 1550000 (withdraw "A") (withdraw "I")))
	 
	 (check-liquid
	  (strategy "A" (do-auth))))

For the sake of simplicity, this contract is executed without separating Alice's view from Bob's.
For an example of how the two participant independently execute the contract, 
refer to the :ref:`Timed Commitment` example.

This is the contract compiled in Balzac, completed with the signatures required to execute the contract.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-liquid (strategy A (do-auth)))

	Result: true
	Model checking time: 108.0 ms
	=============================================================================*/
	
	const privA = key:... //removed
	const privI = key:... //removed

	const pubkeyI8 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA9 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA3 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI2 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA1 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA5 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI4 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyI10 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA7 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI6 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyI = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	transaction Tinit { 
	 input = [ tx:0200000001fbcee70062cab1cbe78f158851ee2351b3ce7d549201ac9f87c961225fb7ce4600000000e5483045022100fff909e25bcc800deebce554eb24b68080f2b02290b41076ad5cfb8b026453740220725b65455de27a643d74ac2deeccc3cb2bb3ba5c486bd19a2fc7c9034228e0f801483045022100fd976972a047c57e22b791c19d1ffdad25a9fb5240278cb923626d0285f6de0c02200820d34a98f7c7cc658412ec7053b3f14709ff86fd5b4532a46419181cfbbbaf014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff011a760c00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sig(privA); 
	 tx:0200000001961c3539383d133a2d08606f2606b5db969a4a44e29f7e2e07cafcb95dc001fb00000000e347304402202960aa1cb055984f522b6ce3f0516c28bb1b732752edb8e2601651ac8bf178200220402b32a19d8be4fca5cb4e7b39a2ca9f3c08b9bb8aa7377929b83ae1dcc9acb10147304402207d34f6bb8690412560913a9f11e1cd4d1b37a9bb5dd1e877c8a46f062aa19bf002206da20009c6dc5ac2ff4a78550f7f0be6f61bc7a924770266602faff973fe2e0c014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sig(privA) ] 
	 output = 0.01239998 BTC : fun(sA, sI) . (( versig(pubkeyA1, pubkeyI2; sA, sI) ||
	 versig(pubkeyA3, pubkeyI4; sA, sI) )) 
	}

	transaction T1 { 
	 input = [ Tinit@0: sig(privA) sig(privI) ] 
	 output = 0.01209998 BTC : fun(sA, sI) . versig(pubkeyA5, pubkeyI6; sA, sI) || versig(pubkeyA7, pubkeyI8; sA, sI) 
	}

	transaction T2 { 
	 input = [ T1@0:  sig(privA) sig(privI) ] 
	 output = 0.01179998 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T3 { 
	 input = [ T1@0: sig(privA) sig(privI) ] 
	 output = [ 0.00589999 BTC : fun(sA, sI) . ((versig(pubkeyA5, pubkeyI6; sA, sI)));
		0.00589999 BTC : fun(sA, sI) . ((versig(pubkeyA9, pubkeyI10; sA, sI))) ] 
	 absLock = block 1550000
	}

	transaction T4 { 
	 input = [ T3@0:  sig(privA) sig(privI) ] 
	 output = 0.00559999 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T5 { 
	 input = [ T3@1:  sig(privA) sig(privI) ] 
	 output = 0.00559999 BTC : fun(x) . versig(pubkeyI; x) 
	 
	}

	transaction T6 { 
	 input = [ Tinit@0: sig(privA) sig(privI) ] 
	 output = 0.01209998 BTC : fun(sA, sI) . versig(pubkeyA9, pubkeyI10; sA, sI) || versig(pubkeyA7, pubkeyI8; sA, sI) 
	}

	transaction T7 { 
	 input = [ T6@0:  sig(privA) sig(privI) ] 
	 output = 0.01179998 BTC : fun(x) . versig(pubkeyI; x) 
	 
	} 

	transaction T8 { 
	 input = [ T6@0: sig(privA) sig(privI) ] 
	 output = [ 0.00589999 BTC : fun(sA, sI) . ((versig(pubkeyA5, pubkeyI6; sA, sI)));
		0.00589999 BTC : fun(sA, sI) . ((versig(pubkeyA9, pubkeyI10; sA, sI))) ] 
	 absLock = block 1550000
	}

	transaction T9 { 
	 input = [ T8@0:  sig(privA) sig(privI) ] 
	 output = 0.00559999 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T10 { 
	 input = [ T8@1:  sig(privA) sig(privI) ] 
	 output = 0.00559999 BTC : fun(x) . versig(pubkeyI; x) 
	 
	}

	eval Tinit, T1, T2

We have executed the compiled contract on the Bitcoin testnet. The hash of the transactions are the following:

========================== ============ =======================================================================================================================================================================
Phase                       Tx name      Tx id  	  														  
========================== ============ =======================================================================================================================================================================
Init                        Tinit        `8aacdd349718c6ee472853783c0e494954604f5ef45a942603ac8a0f10dda50a <https://chain.so/tx/BTCTEST/8aacdd349718c6ee472853783c0e494954604f5ef45a942603ac8a0f10dda50a>`_  
choice                      T1           `ab0a5bd26aff3871cdb7ad4e7228a30dac2df05ff9409226cd39131e7e9d4bce <https://chain.so/tx/BTCTEST/ab0a5bd26aff3871cdb7ad4e7228a30dac2df05ff9409226cd39131e7e9d4bce>`_
withdraw "A"                T2           `62d5f294d37885674deabece19dae59cfc6724f9ba3a17280179185b92c8abd4 <https://chain.so/tx/BTCTEST/62d5f294d37885674deabece19dae59cfc6724f9ba3a17280179185b92c8abd4>`_
========================== ============ =======================================================================================================================================================================