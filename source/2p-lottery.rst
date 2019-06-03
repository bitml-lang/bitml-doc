""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Two players lottery (with collaterals)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

We specify in BitML the 2-players lottery described in Andrychowicz et al paper `Secure Multiparty Computations on Bitcoin <https://ieeexplore.ieee.org/document/6956580/>`_. The lottery involves 2 players, Alice and Bob, who bet 0.001 BTC each. The winner, chosen uniformly at random, gets 0.002 BTC. To determine the winner, each player secretly flips a coin: 
if the two sides are equal, the winner is the first player, otherwise it is the second player. To ensure fairness, the players put a deposit of 0.003 BTC each: 0.001 BTC for the bet, and 0.002 BTC as a collateral.

The contract splits its balance in three sub-contracts.
In the first one, if Bob does not reveal before block 1500000 is added to the blockchain, then Alice can get 0.002 bitcoins. 
The second subcontract is similar, inverting the roles. 
To achieve fairness, we require secrets to be 0 or 1. 
The third subcontract pays 0.002 bitcoins to the winner.


.. code-block:: bitml

	#lang bitml

	(debug-mode)

	(define (txA) "tx:02000000000101124327402f588c4b46cfa8b1670495bd9f6f57b969212af5b8afe5da191e349f0000000017160014ca98e2fc277b25dfe48db007419b4b6f7eff7cb2feffffff0205f717000000000017a914ffe4b939f7384b08ec04b2f605b0dca4413af16a87e0930400000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac024730440220197c12bf078c2bbc8f86ce93cb42042e3d528ee62de5647c1827229fe9b809ef02205e6faf5a1af59aefe493055e2cdc9d435e3524bba1cc9179e343aa8ae311de30012102a0a9937b3273031c28c1c1c4f87d7d89e4d6f973bdb00e6447a708d2c91991b2cd271700@1")
	(define (txB) "tx:02000000000101bb536c381e14e1edf2d460d2e0a9ed649da2b61733d0a5d101489c5ba7fba8400100000017160014023b9558d3736f47b3ff16dcb66800ae89fc681dfeffffff025c8c3e000000000017a9140cd0faeac9fd6f23f57e206d170cd9df909e9ac987e0930400000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac02473044022059ed91550240d9da58e3cef4dabc2b2719ce36c5e05a7af35c6c321fd914c5e70220149e461c53c155706ad6b27bf1f6b08f40a2ad3a2f4c23d41481df840caafce7012102407baf142709a99a67a19c6e9ea8af329e5b1cd6ba1d178f0a5fce3a94db8eb9e1271700@1")
	(define (txFee) "tx:02000000000101cc1a7d72cd7c5f64d2e0f34a0f929532b11e18a0802a2cd9d2503fd60b19585e00000000171600149e7b7e6acb6c7d0b613bb3c72f55afc723686683feffffff0240420f00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88acfedd33000000000017a914677fd79b9ab537dea966e328afa6fb27d8e9aa3b870247304402201bf5adf5fdea7f1939798fb5acd8a5e75aecddee47a0d101f1113ba5f4a28a3e02205461cd71f3e757d92a0d0635937a13e219508c1be7464473b717e92cf622d642012103fa6e338afbb1bd9ffe0abc107dc15eb38811babac4d2a67fa6b78a2bd38a0809e1271700@0")

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(contract (pre
	           (deposit "A" 0.003 (ref (txA)))(secret "A" a "b472a266d0bd89c13706a4132ccfb16f7c3b9fcb")
	           (deposit "B" 0.003 (ref (txB)))(secret "B" b "c51b66bced5e4491001bd702669770dccf440982")
	           (fee "B" 0.01 (ref (txFee))))
	         
	          (split
	           (0.002 -> (choice
	                  (revealif (b) (pred (between b 0 1)) (withdraw "B"))
	                  (after 1500000 (withdraw "A"))))
	           (0.002 -> (choice
	                  (reveal (a) (withdraw "A"))
	                  (after 1500000 (withdraw "B"))))
	           (0.002 -> (choice
	                  (revealif (a b) (pred (= a b)) (withdraw "A"))
	                  (revealif (a b) (pred (!= a b)) (withdraw "B"))
	                  (after 1500000 (split (0.001 -> (withdraw "A")) (0.001 -> (withdraw "B")))))))
			  
	          (auto-generate-secrets)
	          (check-liquid))

For the sake of simplicity, this contract is executed without separating Alice's view from Bob's.
For an example of how the two participant independently execute the contract, 
refer to the :ref:`Timed Commitment` example.

This is the contract compiled in Balzac, completed with the signatures 
and the secret required to execute the contract.

.. code-block:: balzac

	const privA = _ // removed
	const privB = _ // removed

	const sec_a:string = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
	const sec_b:string = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"


	const pubkeyB3 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA18 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA14 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB1 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA2 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB17 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA12 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA10 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB9 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA8 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA6 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB7 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB19 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA20 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA4 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyA16 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB5 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB13 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB15 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyB11 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const pubkeyB = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809
	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1

	transaction Tinit { 
	 input = [ 
	 tx:02000000000101bb536c381e14e1edf2d460d2e0a9ed649da2b61733d0a5d101489c5ba7fba8400100000017160014023b9558d3736f47b3ff16dcb66800ae89fc681dfeffffff025c8c3e000000000017a9140cd0faeac9fd6f23f57e206d170cd9df909e9ac987e0930400000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac02473044022059ed91550240d9da58e3cef4dabc2b2719ce36c5e05a7af35c6c321fd914c5e70220149e461c53c155706ad6b27bf1f6b08f40a2ad3a2f4c23d41481df840caafce7012102407baf142709a99a67a19c6e9ea8af329e5b1cd6ba1d178f0a5fce3a94db8eb9e1271700@1:sig(privB); 
	 tx:02000000000101124327402f588c4b46cfa8b1670495bd9f6f57b969212af5b8afe5da191e349f0000000017160014ca98e2fc277b25dfe48db007419b4b6f7eff7cb2feffffff0205f717000000000017a914ffe4b939f7384b08ec04b2f605b0dca4413af16a87e0930400000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac024730440220197c12bf078c2bbc8f86ce93cb42042e3d528ee62de5647c1827229fe9b809ef02205e6faf5a1af59aefe493055e2cdc9d435e3524bba1cc9179e343aa8ae311de30012102a0a9937b3273031c28c1c1c4f87d7d89e4d6f973bdb00e6447a708d2c91991b2cd271700@1:sig(privA);
	 tx:02000000000101cc1a7d72cd7c5f64d2e0f34a0f929532b11e18a0802a2cd9d2503fd60b19585e00000000171600149e7b7e6acb6c7d0b613bb3c72f55afc723686683feffffff0240420f00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88acfedd33000000000017a914677fd79b9ab537dea966e328afa6fb27d8e9aa3b870247304402201bf5adf5fdea7f1939798fb5acd8a5e75aecddee47a0d101f1113ba5f4a28a3e02205461cd71f3e757d92a0d0635937a13e219508c1be7464473b717e92cf622d642012103fa6e338afbb1bd9ffe0abc107dc15eb38811babac4d2a67fa6b78a2bd38a0809e1271700@0:sig(privB) ] 
	 output = 0.01569999 BTC : fun(sB, sA) . (( versig(pubkeyB1, pubkeyA2; sB, sA) )) 
	}

	transaction T1 { 
	 input = [ Tinit@0: sig(privB) sig(privA) ] 
	 output = [ 0.00513333 BTC : fun(b:string, sB, sA) . (((between((size(b) - 128),0,2) && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB3, pubkeyA4; sB, sA)) ||
	 versig(pubkeyB5, pubkeyA6; sB, sA)));
		0.00513333 BTC : fun(a:string, sB, sA) . (((hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && versig(pubkeyB7, pubkeyA8; sB, sA)) ||
	 versig(pubkeyB9, pubkeyA10; sB, sA)));
		0.00513333 BTC : fun(a:string, b:string, sB, sA) . (((size(a) == size(b) && hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB11, pubkeyA12; sB, sA)) ||
	 (size(a) != size(b) && hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB13, pubkeyA14; sB, sA)) ||
	 versig(pubkeyB15, pubkeyA16; sB, sA))) ] 
	}

	transaction T2 { 
	 input = [ T1@0:sec_b  sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(sB, sA) . versig(pubkeyB17, pubkeyA18; sB, sA) 
	}

	const sigBT3 : signature = _ 
	const sigAT3 : signature = _ 

	transaction T3 { 
	 input = [ T2@0:   sig(privB) sig(privA) ] 
	 output = 0.00453333 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	transaction T4 { 
	 input = [ T1@0: ""  sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(x) . versig(pubkeyA; x) 
	 absLock = block 1500000 
	}

	transaction T5 { 
	 input = [ T1@1:sec_a  sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(sB, sA) . versig(pubkeyB19, pubkeyA20; sB, sA) 
	}

	const sigBT6 : signature = _ 
	const sigAT6 : signature = _ 

	transaction T6 { 
	 input = [ T5@0:  sig(privB) sig(privA) ] 
	 output = 0.00453333 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T7 { 
	 input = [ T1@1: "" sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(x) . versig(pubkeyB; x) 
	 absLock = block 1500000 
	}

	transaction T8 { 
	 input = [ T1@2:sec_a sec_b  sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(sB, sA) . versig(pubkeyB19, pubkeyA20; sB, sA) 
	}

	transaction T9 { 
	 input = [ T8@0:   sig(privB) sig(privA) ] 
	 output = 0.00453333 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T10 { 
	 input = [ T1@2:sec_a sec_b  sig(privB) sig(privA) ] 
	 output = 0.00483333 BTC : fun(sB, sA) . versig(pubkeyB17, pubkeyA18; sB, sA) 
	}

	transaction T11 { 
	 input = [ T10@0:  sig(privB) sig(privA) ] 
	 output = 0.00453333 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	transaction T12 { 
	 input = [ T1@2: "" "" sig(privB) sig(privA) ] 
	 output = [ 0.00241666 BTC : fun(sB, sA) . ((versig(pubkeyB19, pubkeyA20; sB, sA)));
		0.00241666 BTC : fun(sB, sA) . ((versig(pubkeyB17, pubkeyA18; sB, sA))) ] 
	 absLock = block 1500000
	}

	transaction T13 { 
	 input = [ T12@0:  sig(privB) sig(privA) ] 
	 output = 0.00211666 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T14 { 
	 input = [ T12@1:  sig(privB) sig(privA)] 
	 output = 0.00211666 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	eval Tinit, T1, T2, T3, T5, T6, T8, T9


We have executed the compiled contract on the Bitcoin testnet. The hash of the transactions are the following:

	
========================== ============ ============================================================================================================================================================================================================
Phase                       Tx name      Tx id  	  														  
========================== ============ ============================================================================================================================================================================================================
Init                        Tinit        `e94be8d58c1839e5649ac5a5c50dd114b235bc99338c7766c15e2a1a858fc8e7 <https://chain.so/tx/BTCTEST/e94be8d58c1839e5649ac5a5c50dd114b235bc99338c7766c15e2a1a858fc8e7>`_  
Init                        T1           `72c38df85cb8deb2a89d9af937662ccad7b1c851513ae719b4e6195ae85ec62d <https://chain.so/tx/BTCTEST/72c38df85cb8deb2a89d9af937662ccad7b1c851513ae719b4e6195ae85ec62d>`_
b commitment                T2           `835b2e52bb1b0c903025c86c4469d3f62ab888118bf0f56c7bbc196ffac9e350 <https://chain.so/tx/BTCTEST/835b2e52bb1b0c903025c86c4469d3f62ab888118bf0f56c7bbc196ffac9e350>`_
b commitment                T3           `8155fd05caed8599d35df7c3fde80a17242cff78653b1929a3f761d9a7507701 <https://chain.so/tx/BTCTEST/8155fd05caed8599d35df7c3fde80a17242cff78653b1929a3f761d9a7507701>`_
a commitment                T5           `a8f02fe90ec579aa0530238dd049794e058c4b7e9c2e9948309a6b034ddda73e <https://chain.so/tx/BTCTEST/a8f02fe90ec579aa0530238dd049794e058c4b7e9c2e9948309a6b034ddda73e>`_
a commitment                T6           `08f24c84628641fecf0f33f013dbdc24c507530282cfb3c5eff97c6c2d502e59 <https://chain.so/tx/BTCTEST/08f24c84628641fecf0f33f013dbdc24c507530282cfb3c5eff97c6c2d502e59>`_
Lottery execution           T8           `ed35d4849c73680d16f9c3a3cd1ce135ab35428b39066db191167a1f501b5ec7 <https://chain.so/tx/BTCTEST/ed35d4849c73680d16f9c3a3cd1ce135ab35428b39066db191167a1f501b5ec7>`_
Lottery execution           T9           `f7097c3523aecc62dc97c790f1b276db9fc662f7a4b13fd548093ff11a09d33d <https://chain.so/tx/BTCTEST/f7097c3523aecc62dc97c790f1b276db9fc662f7a4b13fd548093ff11a09d33d>`_
========================== ============ ============================================================================================================================================================================================================

