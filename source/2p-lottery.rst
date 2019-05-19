""""""""""""""""""""""""""""
Two players lottery (with collaterals)
""""""""""""""""""""""""""""

We specify in BitML the 2-players lottery described in Andrychowicz et al.' paper `Secure Multiparty Computations on Bitcoin <https://ieeexplore.ieee.org/document/6956580/>`_. The lottery involves 2 players, Alice and Bob, who bet 0.001 BTC each. The winner, chosen uniformly at random, gets 0.002 BTC. To determine the winner, each player secretly flips a coin: 
if the two sides are equal, the winner is the first player, otherwise it is the second player. To ensure fairness, the players put a deposit of 0.003 BTC each: 0.001 BTC for the bet, and 0.002 BTC as a collateral.

The contract splits its balance in three sub-contracts.
In the first one, if Bob does not reveal before block 1500000 is added to the blockchain, then Alice can get 0.002 bitcoins. 
The second subcontract is similar, inverting the roles. 
To achieve fairness, we require secrets to be 0 or 1. 
The third subcontract pays 0.002 bitcoins to the winner.


.. code-block:: bitml

	#lang bitml

	(debug-mode)

	(define (txA) "tx:0200000000010141e7f4e9af6c149629ceed2468e362eb147b6f169cb0a9c2997fbe0a227efb890000000017160014e4f5f50ae873bd1c23e82fdc3808ec3b485b132dfeffffff02e0930400000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac5f4412000000000017a914662af7dba12353d03d049ad01547b5c2abf33301870247304402207927d83ffed60ce2f7b5e94f939833eca7679b814b30b36c8ffb5586475f468002206e114af2510e0a7aff1325f6d34ed9573b30ef877cbaad8aa4d97d537ddf149e012102e6cd568374f4b7d4cd97794c186384c7ecdaa9b3e79aa4aa2b8d5397583828d443241700@0")
	(define (txB) "tx:0200000000010113158418e1582ced019932d6b07d03ea2e0ebb3bee880ecaa663638fa4877258010000001716001418442f1d465df7e2d1257c0550d9bd2401f9557efeffffff02634412000000000017a91472d4d57afe9d8430f661f0240bf9d47ec545f8b787e0930400000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac024730440220105ba58827697fff2245736bb9ac6581026c8de2fa7a8c4c72c21459568fdf6402204e8b127df854d22402504f862078d1c261c9da2f916b5f2a1d8ccd232355b807012103dbe6085de318d9ec7793bd7770cad6bc5fa6a7bbea37b5739fb1a1a8bc512e9c43241700@1")
	(define (txFee) "tx:02000000000101cf1b6c003e090a079c2b814cce0152d93052b6c900c555a5e0bd372e8c240bc72100000017160014045e674e5834b6034e2de314c22c3ab66470962dfeffffff0240420f00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac78d513000000000017a914f5fed12c4365464ec88861634917f7d64478570c87024730440220770314f0713d39da943b17dc25d587f003f0c96bc795e8a75f1289d64a1a31c402204d082478efde292031388cb137105f4bdf292dd8da74976ec1b15f148cb9897801210344a74576f947f7a35d9585f8efc89c9699d855a5cfb7e208332bf866ea6a61d443241700@0")

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

	          (check-liquid))


Compiled transactions:


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
	 input = [ 
	 tx:0200000000010113158418e1582ced019932d6b07d03ea2e0ebb3bee880ecaa663638fa4877258010000001716001418442f1d465df7e2d1257c0550d9bd2401f9557efeffffff02634412000000000017a91472d4d57afe9d8430f661f0240bf9d47ec545f8b787e0930400000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac024730440220105ba58827697fff2245736bb9ac6581026c8de2fa7a8c4c72c21459568fdf6402204e8b127df854d22402504f862078d1c261c9da2f916b5f2a1d8ccd232355b807012103dbe6085de318d9ec7793bd7770cad6bc5fa6a7bbea37b5739fb1a1a8bc512e9c43241700@1:sig(privB); 
	 tx:0200000000010141e7f4e9af6c149629ceed2468e362eb147b6f169cb0a9c2997fbe0a227efb890000000017160014e4f5f50ae873bd1c23e82fdc3808ec3b485b132dfeffffff02e0930400000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac5f4412000000000017a914662af7dba12353d03d049ad01547b5c2abf33301870247304402207927d83ffed60ce2f7b5e94f939833eca7679b814b30b36c8ffb5586475f468002206e114af2510e0a7aff1325f6d34ed9573b30ef877cbaad8aa4d97d537ddf149e012102e6cd568374f4b7d4cd97794c186384c7ecdaa9b3e79aa4aa2b8d5397583828d443241700@0:sig(privA); 
	 tx:02000000000101cf1b6c003e090a079c2b814cce0152d93052b6c900c555a5e0bd372e8c240bc72100000017160014045e674e5834b6034e2de314c22c3ab66470962dfeffffff0240420f00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac78d513000000000017a914f5fed12c4365464ec88861634917f7d64478570c87024730440220770314f0713d39da943b17dc25d587f003f0c96bc795e8a75f1289d64a1a31c402204d082478efde292031388cb137105f4bdf292dd8da74976ec1b15f148cb9897801210344a74576f947f7a35d9585f8efc89c9699d855a5cfb7e208332bf866ea6a61d443241700@0:sig(privB) ] 
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

	 eval Tinit, T1, T2, T3, T5, T6, T8, T9


We have executed the compiled contract on the Bitcoin testnet. The hash of the transactions are the following:

	
========================== ============ ====================================================================
Phase                       Tx name      Tx id  	  														  
========================== ============ ====================================================================
Init                        Tinit        02974b61832dced6ca3aebbdc536764097dca95036e04d0ff42ec0cd9ca518b  
Init                        T1           3e9aa8d9b7e829d03e083b23cfbe21fbb41e524f509e895348ac099eb048ab4f
b commitment                T2           
b commitment                T3           
a commitment                T5           fb01c05db9fcca072e7e9fe2444a9a96dbb506266f60082d3a133d3839351c96
a commitment                T6           72319a786a474703215941bf8cae551b4a1caa1cf712f184409f393383f2993a
Lottery execution           T8
Lottery execution           T9
========================== ============ ====================================================================

