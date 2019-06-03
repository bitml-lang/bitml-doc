.. _Timed Commitment:

""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Timed commitment
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Assume that Alice wants to choose a secret ``s``, and reveal it after some time --
while guaranteeing that the revealed value corresponds to the chosen secret (or paying
a penalty otherwise). This can be obtained through a timed commitment, a
protocol with applications e.g. in gambling games, where the secret
contains the player move, and the delay in the revelation of the secret is intended
to prevent other players from altering the outcome of the game. 

In the timed commitment below, Alice commits a secret of hash ``b472a266d0bd89c13706a4132ccfb16f7c3b9fcb``,
and has until block 1550000 to reveal it. After block 1550000 is appended to the blockchain,
Bob can redeem Alice's deposit.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(define (txA) "tx:0200000001c75e1b501f7a1691b16d06398b4235ab35e11ccda3c3f9160d68739c84d435ed00000000e4483045022100ad5f0022e6ae8e789a97ca9497b8d307690b96ddbfcdf822711b1983b328d26702204f276374584292322c1ad33dc7b67600673ace464e9c60990de7a0123933803c014730440220055c42ae93321b4061055c782be11d3392c84ff34b1d4fbbe3a9e208f63518170220231d7712a4d36e5397264bfc8db89fd1d13d64937ee886fb9872f260bf979760014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0")
	(define (txFee) "tx:02000000013ea7dd4d036b9a3048992e9c7e4b8c054e7949d08d233005aa79c50ee92ff0a800000000e3483045022100f956e4b07562a209662b42ab0b6d26784de59470d992a542c207e74bf03776d5022071a5089744aa25316d29cb9d1e9bd28f5f50eba6c2c5b57177bf0a17c35308a601463043021f26ce5a6c343fcb5edf3a06dbb95006cbf063393ec7b5beebd16e2c8120c059022015c4afec46a1c04d1dcfbf8e414d9f83d0a008c91b1a96f6b499edec2b8d1d48014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0")

	(debug-mode)

	(contract
	 (pre (deposit "A" 0.00453333 (ref (txA)))
	      (fee "A" 0.00453333 (ref (txFee)))
	      (secret "A" a "b472a266d0bd89c13706a4132ccfb16f7c3b9fcb"))
	 
	 (choice (reveal (a) (withdraw "A"))
	      (after 1550000 (withdraw "B")))

	 (check-liquid))


--------------------------------
Alice's view
--------------------------------

Alice opens the `Balzac Online Editor <https://editor.balzac-lang.xyz/>`_,
and pastes the output of the compiler.
She starts computing her signatures, by first defining her public key ``privA``,
then putting :balzac:`sig(privA)` where the compiler requires her signatures.
She also puts the value of her secret ``00000000...001``.

Then, she evaluates her signatures, using :balzac:`eval sig(privA) of Tinit@0, ...`
at the bottom of the file, and sends them to Bob.
Bob does the same, so Alice receives his signatures and puts them 
in the constant declarations ``sigBT1``, ``sigBT3``, ``sigBT3``.

Now all the transactions are completed and Alice can evaluate them,
and send to the Bitcoin network ``Tinit`` to start the contract,
``T1`` to reveal the secret, and ``T2`` to redeem her deposit.

After ``T1`` added to the blockchain, is not possible to publish 
``T3`` (the transaction that send Alice's deposit to Bob) anymore, 
because they spend the same output ``Tinit@0``.
This is coherent with the specification of the contract, 
because if Alice reveals her secret, Bob shouldn't be able to take her deposit.

.. code-block:: balzac
	
	const privA = _ removed

	const sec_a:string = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"

	const pubkeyA6 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB1 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB3 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB5 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA2 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA4 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1

	const pubkeyB = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1

	transaction Tinit { 
	 input = [ tx:0200000001c75e1b501f7a1691b16d06398b4235ab35e11ccda3c3f9160d68739c84d435ed00000000e4483045022100ad5f0022e6ae8e789a97ca9497b8d307690b96ddbfcdf822711b1983b328d26702204f276374584292322c1ad33dc7b67600673ace464e9c60990de7a0123933803c014730440220055c42ae93321b4061055c782be11d3392c84ff34b1d4fbbe3a9e208f63518170220231d7712a4d36e5397264bfc8db89fd1d13d64937ee886fb9872f260bf979760014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sig(privA); 
	 tx:02000000013ea7dd4d036b9a3048992e9c7e4b8c054e7949d08d233005aa79c50ee92ff0a800000000e3483045022100f956e4b07562a209662b42ab0b6d26784de59470d992a542c207e74bf03776d5022071a5089744aa25316d29cb9d1e9bd28f5f50eba6c2c5b57177bf0a17c35308a601463043021f26ce5a6c343fcb5edf3a06dbb95006cbf063393ec7b5beebd16e2c8120c059022015c4afec46a1c04d1dcfbf8e414d9f83d0a008c91b1a96f6b499edec2b8d1d48014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sig(privA) ] 
	 output = 0.00876666 BTC : fun(a:string, sB, sA) . (( (hash160(a) == hash:9f3df038eeadc0c240fb7f82e31fdfe46804fc7c && size(a) >= 128 && versig(pubkeyB1, pubkeyA2; sB, sA)) ||
	 versig(pubkeyB3, pubkeyA4; sB, sA) )) 
	}

	const sigBT1 : signature = sig:30450221008e8cf2da8535b488dab5234a8a6cc942d4f3dbbf0993a0be77aa5d80f520c1fa02203e407d58fe6dc8eeca8478c9c0c0e43e5cc2b25567716489f8358b157aa9dacc01[pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809] 
	//received from Bob

	transaction T1 { 
	 input = [ Tinit@0:sec_a sigBT1 sig(privA) ] 
	 output = 0.00846666 BTC : fun(sB, sA) . versig(pubkeyB5, pubkeyA6; sB, sA) 
	}

	const sigBT2 : signature = sig:3045022100fff909e25bcc800deebce554eb24b68080f2b02290b41076ad5cfb8b026453740220725b65455de27a643d74ac2deeccc3cb2bb3ba5c486bd19a2fc7c9034228e0f801[pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809] 
	//received from Bob

	transaction T2 { 
	 input = [ T1@0:  sigBT2 sig(privA) ] 
	 output = 0.00816666 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigBT3 : signature = sig:3045022100c58572e8e1818ebbef2111da049a27f93cac791fc9d881acc48e43075382f8fb022032b2ff112f414463f884ccfcf427b4c952826e338779de63c3055d57b6ab89a501[pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809] 
	//received from Bob
	const sigAT3 : signature = _ 

	transaction T3 { 
	 input = [ Tinit@0: "0" sigBT3 sig(privA) ] 
	 output = 0.00846666 BTC : fun(x) . versig(pubkeyB; x) 
	 absLock = block 1550000 
	}

	eval sig(privA) of Tinit@0, sig(privA) of Tinit@1, 
	    sig(privA) of T1, sig(privA) of T2, sig(privA) of T3,
	    Tinit, T1, T2


--------------------------------
Bob's view
--------------------------------

The steps executed by Bob are the dual of the Alice's ones.
Differently from Alice, he cannot publish ``T1`` right away, because he doesn't know the secret.
He wait for Alice to reveal her secret, or until block 155000,
when the timelock on ``T3`` will unlock, and publish it to take Alice's deposit. 


.. code-block:: balzac

	const privB = _ //removed

	const sec_a:string = ""

	const pubkeyA6 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB1 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB3 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB5 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA2 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA4 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1

	const pubkeyB = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1

	const sigA0 : signature = sig:304402204adabfd7e29232148e3fa6a4bd8d3d3dd8fe6d5a9db8c77eec79fb556addb82b0220230c05987f38db659f9d1168ed7083a4ed602d44ba789c5ef903241e4577f6d501[pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1]
	//received from Alice

	const sigAFee : signature = sig:3045022100a81265cba65ad2fd793d241210ab194629efe41126673130cc40297c9d177c250220161c6087dcbb5957c21c2b415312eded883ed80964e6976e2559976e5cf21d6101[pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1]
	//received from Alice

	transaction Tinit { 
	 input = [ tx:0200000001c75e1b501f7a1691b16d06398b4235ab35e11ccda3c3f9160d68739c84d435ed00000000e4483045022100ad5f0022e6ae8e789a97ca9497b8d307690b96ddbfcdf822711b1983b328d26702204f276374584292322c1ad33dc7b67600673ace464e9c60990de7a0123933803c014730440220055c42ae93321b4061055c782be11d3392c84ff34b1d4fbbe3a9e208f63518170220231d7712a4d36e5397264bfc8db89fd1d13d64937ee886fb9872f260bf979760014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sigA0; 
	 tx:02000000013ea7dd4d036b9a3048992e9c7e4b8c054e7949d08d233005aa79c50ee92ff0a800000000e3483045022100f956e4b07562a209662b42ab0b6d26784de59470d992a542c207e74bf03776d5022071a5089744aa25316d29cb9d1e9bd28f5f50eba6c2c5b57177bf0a17c35308a601463043021f26ce5a6c343fcb5edf3a06dbb95006cbf063393ec7b5beebd16e2c8120c059022015c4afec46a1c04d1dcfbf8e414d9f83d0a008c91b1a96f6b499edec2b8d1d48014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff01d5ea0600000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac00000000@0:sigAFee ] 
	 output = 0.00876666 BTC : fun(a:string, sB, sA) . (( (hash160(a) == hash:9f3df038eeadc0c240fb7f82e31fdfe46804fc7c && size(a) >= 128 && versig(pubkeyB1, pubkeyA2; sB, sA)) ||
	 versig(pubkeyB3, pubkeyA4; sB, sA) )) 
	}

	const sigAT1 : signature = sig:304402205f97481078e6b4579798a0233d0451cda9c905ae37adab483229d3034089e08302207ce6d7207a913aab50247f5961347e87802c28eb11a6aa9f45e0f9c92664e8ba01[pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1] 
	//received from Alice

	transaction T1 { 
	 input = [ Tinit@0:sec_a sig(privB) sigAT1 ] 
	 output = 0.00846666 BTC : fun(sB, sA) . versig(pubkeyB5, pubkeyA6; sB, sA) 
	}

	const sigAT2 : signature =  sig:3045022100bcd87e903813a49e9c598c561a952ee26ceec4ac010644c6dd0055a518058c0d02201e35953d7f7c50244a8eeb0b289c387167f2fd9096e7f7f16dcb2501de8e658b01[pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1] 
	//received from Alice

	transaction T2 { 
	 input = [ T1@0:  sig(privB) sigAT2 ] 
	 output = 0.00816666 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	const sigAT3 : signature = sig:304402202c47c0fb3d196074541d30e3d3680e1206f50d7abbf4431436f34423297729ba022022d7f5e5864eee01b721a2db695a58c1b586929f750d299b2a41122d62b247c001[pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1] 
	//received from Alice

	transaction T3 { 
	 input = [ Tinit@0: "0" sig(privB) sigAT3 ] 
	 output = 0.00846666 BTC : fun(x) . versig(pubkeyB; x) 
	 absLock = block 1550000 
	}

	eval sig(privB) of T1, sig(privB) of T2, sig(privB) of T3,
	    Tinit, T3



We have executed the compiled contract on the Bitcoin testnet. The hash of the transactions are the following:

	
========================== ============ ============================================================================================================================================================================================================
Phase                       Tx name      Tx id  	  														  
========================== ============ ============================================================================================================================================================================================================
Init                        Tinit        `139a7b529cb5b91ab54257abf22797b25700430f0cc49bf69324fc1d07827ad2 <https://chain.so/tx/BTCTEST/139a7b529cb5b91ab54257abf22797b25700430f0cc49bf69324fc1d07827ad2>`_  
reveal a                    T1           `46ceb75f2261c9879fac0192547dceb35123ee5188158fe7cbb1ca6200e7cefb <https://chain.so/tx/BTCTEST/46ceb75f2261c9879fac0192547dceb35123ee5188158fe7cbb1ca6200e7cefb>`_
withdraw "A"                T2           `6e1fd285cab75985de9b52a6068e67bc074d80e81baac72bb741004333df1f8e <https://chain.so/tx/BTCTEST/6e1fd285cab75985de9b52a6068e67bc074d80e81baac72bb741004333df1f8e>`_
========================== ============ ============================================================================================================================================================================================================
