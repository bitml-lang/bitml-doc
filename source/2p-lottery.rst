""""""""""""""""""""""""""""
Two players lottery
""""""""""""""""""""""""""""

This contract models a lottery, where Alice and Bob bet 0.001 BTC each, and the winner, 
chosen uniformly at random, gets 0.002 bitcoins. 
To determine the winner, each player secretly flips a coin: 
if the two sides are equal, the winner is the first player, otherwise it is the second player.
The participants are required to put a deposit of 0.003 BTC each: 0.001 BTC for the bet,
and 0.002 BTC as a security deposit.

The contract split its balance in three sub-contracts.
In the first one, if Bob does not reveal before block 1500000 is added to the blockchain, 
then Alice can get 0.002 bitcoins. 
The second subcontract is similar, inverting the roles. 
To achieve fairness, we require secrets to be 0 or 1. 
The third subcontract pays 0.002 bitcoins to the winner.




.. code-block:: bitml

	#lang bitml

	(debug-mode)

	(auto-generate-secrets)

	(participant "A" "029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced")
	(participant "B" "022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30")

	(contract (pre
	           (deposit "A" 0.003 "txA@0")(secret "A" a "b472a266d0bd89c13706a4132ccfb16f7c3b9fcb")
	           (deposit "B" 0.003 "txB@0")(secret "B" b "c51b66bced5e4491001bd702669770dccf440982"))
	         
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

	          (check-liquid))



.. code-block:: balzac

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
	 input = [ tx:020000000001013798d4b82e0e97c29bba04a3c12cb66ab01961b6a6fb36dc38a50afca915cc9701000000171600146f59f2c1c3830564a2582c4f9782cddd81715276feffffff02e0930400000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88acebd816000000000017a914615a97ecc0a1656e57d5d250cc5f3cfedcf3e9da87024730440220732d81a6b88e65c9cc53b61a686b3cc461aeb5e3991351845aa3978b13895d4202203cc2e70236ca77bad1e4cb3e396b29f04c854935393744fe7d75d22b49a2a831012102e5712f5d5743019d4daae6df14ca027fb72fd4dbcf8ad0dba315fc1b77bb4afb42241700@0:sig(privB); 
	 tx:0200000000010191a7f4a73aa5fdebb4cc9fe96ec2a0e390674b9fa106fd0d9ece4af9c99c0e71010000001716001439a5abf7ab08b415c578e38356ad79ea1c3afc8cfeffffff02e7d816000000000017a914e9ce238665f09c3d8ac0e7bfa995c64c3722405787e0930400000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac0247304402204d97c78a96890586fb8de0d7357e76a2ac36934c90bfdd28d478758820cb3a430220634701e4d2722527f5c3d2d96e850643927e1f6fed91f38dfe5c6bc5d1a4ef90012102ffa6f666d618e371737cc5d2c1443d7c89c1b68e764a2601973676e2d64b9fe841241700@1:sig(privA); 
	 tx:0200000001a6ebe7f6d440c1c5fec95964ebacc3b3043b46961ae6e16d8dc9b4c8c8585f1500000000e5483045022100ad948808d7adc6eb210c465773887fbfeefc50bb037c77fa6702560980a9dc8402205a1a57b2209c4c95a87ca56be6101162ef4a30165c922f6bcd0af6d5db3bdf1701483045022100aaa0961dd1529955ad02ce8751500fd95d0bbd1fd360fb291443cc246f26f28d02205b80e606edb4dcc34e22e0989192d71cbd81fe7a4f2604628cca5f980e6744c4014c516b6b006c766c766b7c6b5221034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe152aeffffffff0180de0f00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac00000000@0:sig(privB) ] 
	 output = 0.0161 BTC : fun(sB, sA) . (( versig(pubkeyB1, pubkeyA2; sB, sA) )) 
	}
	
	transaction T1 { 
	 input = [ Tinit@0: sig(privB) sig(privA) ] 
	 output = [ 0.002 BTC : fun(b:string, sB, sA) . (((between((size(b) - 128),0,2) && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB3, pubkeyA4; sB, sA)) ||
	 versig(pubkeyB5, pubkeyA6; sB, sA)));
		0.002 BTC : fun(a:string, sB, sA) . (((hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && versig(pubkeyB7, pubkeyA8; sB, sA)) ||
	 versig(pubkeyB9, pubkeyA10; sB, sA)));
		0.002 BTC : fun(a:string, b:string, sB, sA) . (((size(a) == size(b) && hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB11, pubkeyA12; sB, sA)) ||
	 (size(a) != size(b) && hash160(a) == hash:b472a266d0bd89c13706a4132ccfb16f7c3b9fcb && size(a) >= 128 && hash160(b) == hash:c51b66bced5e4491001bd702669770dccf440982 && size(b) >= 128 && versig(pubkeyB13, pubkeyA14; sB, sA)) ||
	 versig(pubkeyB15, pubkeyA16; sB, sA))) ] 
	}

	transaction T2 { 
	 input = [ T1@0:sec_b  sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(sB, sA) . versig(pubkeyB17, pubkeyA18; sB, sA) 
	}	

	transaction T3 { 
	 input = [ T2@0:   sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}	

	transaction T4 { 
	 input = [ T1@0: "" sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyA; x) 
	 absLock = block 1500000 
	}

	transaction T5 { 
	 input = [ T1@1:sec_a  sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(sB, sA) . versig(pubkeyB19, pubkeyA20; sB, sA) 
	}

	transaction T6 { 
	 input = [ T5@0:   sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}

	transaction T7 { 
	 input = [ T1@1: ""  sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyB; x) 
	 absLock = block 1500000 
	}

	transaction T8 { 
	 input = [ T1@2:sec_a sec_b  sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(sB, sA) . versig(pubkeyB19, pubkeyA20; sB, sA) 
	}	

	transaction T9 { 
	 input = [ T8@0:   sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}	

	transaction T10 { 
	 input = [ T1@2:sec_a sec_b  sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(sB, sA) . versig(pubkeyB17, pubkeyA18; sB, sA) 
	}	

	transaction T11 { 
	 input = [ T10@0:   sig(privB) sig(privA) ] 
	 output = 0.002 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

	transaction T12 { 
	 input = [ T1@2: "" ""  sig(privB) sig(privA) ] 
	 output = [ 0.001 BTC : fun(sB, sA) . ((versig(pubkeyB19, pubkeyA20; sB, sA)));
		0.001 BTC : fun(sB, sA) . ((versig(pubkeyB17, pubkeyA18; sB, sA))) ] 
	 absLock = block 1500000
	}	

	transaction T13 { 
	 input = [ T12@0:   sig(privB) sig(privA) ] 
	 output = 0.001 BTC : fun(x) . versig(pubkeyA; x) 
	 
	}	

	transaction T14 { 
	 input = [ T12@1:   sig(privB) sig(privA) ] 
	 output = 0.001 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

