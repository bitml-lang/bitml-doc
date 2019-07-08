====================================
Court-seized bitcoins
====================================

This series of smart contracts 
is designed to be used in the hypothetical case
where an amount of bitcoins,
seized from someone suspected of illegal activities,
is meant to be managed on-chain.

Recently, an italian court `seized an amount of bitcoins <https://news.bitcoin.com/bitgrail-bitcoin-assets-taken-by-italian-government-victims-still-fuming/>`_,
but, needless to say, the case was not handled with a smart contract.


++++++++++++++++++++++++++++++++++++++
Step 1 - Basic contract
++++++++++++++++++++++++++++++++++++++

In the basic contract, a jury decides if the defendant is innocent.
If they rule in favour of the defendant,
the seized bitcoins must return to the him.
There is no need for the entire jury to judge the defendant innocent, the majority of members is sufficient.

Actors:

	* ``A``, ``B``, ``C``: members of the jury
	* ``S``: defendant

The contract implements the flow described above.

We also verify that if two jurors agree to return the bitcoins to ``S``,
the contract is liquid.

.. code-block:: bitml
	
	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "021927aa11df2776adc8fde8f36c4f7116dbfb466d6c2cd500ae3eabc0fcfb0a33")
	(participant "C" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(participant "S" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f829")

	(debug-mode)

	(contract
	 (pre (deposit "A" 1 "txid:something@0"))
	 
	 (choice
	  (auth "A" "B" (withdraw "S"))
	  (auth "A" "C" (withdraw "S"))
	  (auth "B" "C" (withdraw "S")))
	 
	 (check-liquid
	  (strategy "A" (do-auth))
	  (strategy "B" (do-auth)))
	 )

.. note::
	
	If you only care if a participant authorizes something, and not what particular contract she authorize,
	you can omit the contract from the strategy.
	Example: in :bitml:`(strategy "A" (do-auth (withdraw "S")))`, you can omit :bitml:`(withdraw "S")`.

++++++++++++++++++++++++++++++++++++++
Step 2 - Extend contract
++++++++++++++++++++++++++++++++++++++


Actors:

	* ``A``, ``B``, ``C``: jurors 
	* ``S``: defendant
	* ``T``: storage
	* ``Cur``: curator


The contract is extended with one more step.
After two jurors agree that the defendant is innocent, the balance is split in two parts:

 * 0.9 BTC, which can return to the defendant after block 160000000. At any time before the deadline, the curator can oppose the jury decision and send the bitcoins to the the trusted storage service 
 * 0.1 BTC, which goes to the curator as a service fee.

We verify that: if two members of the jury and the curator agree to return the bitcoins to ``S``,
the contract is liquid;
the curator gets 0.1 BTC if two members of the jury agree.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "021927aa11df2776adc8fde8f36c4f7116dbfb466d6c2cd500ae3eabc0fcfb0a33")
	(participant "C" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(participant "T" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f819")
	(participant "Cur" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f819")
	(participant "S" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f829")

	(debug-mode)

	(define (Veto)
	  (split 
	   (0.1 -> (withdraw "Cur"))
	   (0.9 -> (choice
	            (auth "Cur" (withdraw "T"))
	            (after 10 (withdraw "S"))))))

	(contract
	 (pre (deposit "A" 1 "txid:something@0"))
	 
	 (choice
	  (auth "A" "B" (ref (Veto)))
	  (auth "A" "C" (ref (Veto)))
	  (auth "B" "C" (ref (Veto))))
	 
	 (check-liquid
	  (strategy "A" (do-auth))
	  (strategy "B" (do-auth)))

	 (check "Cur" has-at-least 0.1
	        (strategy "A" (do-auth))
	        (strategy "B" (do-auth)))
	 )

++++++++++++++++++++++++++++++++++++++
Step 3 - The final boss
++++++++++++++++++++++++++++++++++++++

Actors:

	* ``A1``, ``B1``, ``C1``: jurors of the first jury 
	* ``A2``, ``B2``, ``C2``: jurors of the second jury 
	* ``S``: defendant
	* ``Cur``: curator
	* ``T``: storage

This contract is similar to the second one, but if the curator opposes the decision of the jury,
there is another round of judgment. The second round is performed by a second jury.
If the curator opposes the decision of the second jury, the seized bitcoin goes to the trusted storage service.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "021927aa11df2776adc8fde8f36c4f7116dbfb466d6c2cd500ae3eabc0fcfb0a33")
	(participant "C" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(participant "A1" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B1" "021927aa11df2776adc8fde8f36c4f7116dbfb466d6c2cd500ae3eabc0fcfb0a33")
	(participant "C1" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(participant "Cur" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f819")
	(participant "S" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f829")
	(participant "T" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f229")


	(debug-mode)

	(define (Round1)
	  (split 
	   (0.1 -> (withdraw "Cur"))
	   (0.9 -> (choice
	            (auth "Cur" (ref (Round2)))
	            (after 10 (withdraw "S"))))))

	(define (Round2)
	  (tau (choice
	        (auth "A" "B" (ref (Veto)))
	        (auth "A" "C" (ref (Veto)))
	        (auth "B" "C" (ref (Veto))))))

	(define (Veto)
	  (tau (choice
	        (auth "Cur" (withdraw "T"))
	        (after 20 (withdraw "S")))))

	(contract
	 (pre (deposit "A" 1 "txid:something@0"))
	 
	 (choice
	  (auth "A" "B" (ref (Round1)))
	  (auth "A" "C" (ref (Round1)))
	  (auth "B" "C" (ref (Round1))))
	 
	 )


++++++++++++++++++++++++++++++++++++++++++++++
Extra step - working with Balzac transactions
++++++++++++++++++++++++++++++++++++++++++++++

In this last step, we implement a set of functionalities 
which is not expressible in BitML.
Hence, we have to work with low-level `Balzac <https://editor.balzac-lang.xyz/>`_ transactions.

Transaction ``TInit`` locks the seized bitcoin. 
It can be redeemed supplying two out of three
signatures of the jurors AND the signature of the curator, but only after ``2019-06-14``.
The transaction can also be redeemed by the curator alone, so she has until Friday to oppose the decision of the jury.
The identity of the defendant is not known in advance,
so his public key must be a parameter of the transaction that returns the seized bitcoin to him.

Transaction ``T1`` returns the seized bitcoin to the defendant.
Note that we don't know yet his identity, so we supply his
public key as a parameter.

Transaction ``T2`` can be used by the Curator to move the bitcoin directly to the trusted storage service.

.. code-block:: balzac

	const deadline = 2019-06-14

	const pubkeyB = pubkey:03cf4d421345caf86c64554b3b5bd25346a115404977f82de81d281a2825629e0d
	const pubkeyA = pubkey:02c44cefb7238a9c0be51d2e7a84ae7cde17af2280b74971ac90a98d0eb1718c99
	const pubkeyC = pubkey:03b6ef11dfdb271265c814938e17b9a53100651741f99f3b59a3291a79f665ae78
	const pubkeyCur = pubkey:031816ff0d211cc5d1a622777a6e0b10c0b47c43878698e8c515c129ba9ad6e8a9
	const pubkeyCur2 = pubkey:031e07b49510143758597198e5f86bebf26ab453446583a0ea8c8954aaae2f06e3

	const pubkeyT = pubkey:03860d4170fe9ad3f474e18c897a12c1cb3bdeb4bfa2ce6f7c8d99bc81f5c9cef1

	const privKeyA = key:cW85H1zXaQcuv3xbVwJYV2fk53R93RyWxr6haLQXg6CCcdYE6Hwp
	const privKeyB = key:cSaAjg2jRhatr4tjVQ2ax9pe5tH2gR8vAirLVnPtPqm22upvfSGe
	const privKeyC = key:cN14mnfwoF1y4zFkCQXbyf2C7GHYwxpKDbGRiTsusgBhz2fwxajq
	const privKeyCur = key:cPkoJhyv4tXPPNmB8YWeTMHEygnLnWhJwRT4J1BFF16mn6j22qDy
	const privKeyCur2 = key:cT5PtoLpfkSNdBmNWdBhwPpXyJySp91hgT9AyxH1z6KnG7EigwTG

	const privKeyT = key:cNoGEsgNT1k2CedvwpKuPxrCYsLpwgG254n1FwwJZCGRHnEiPV8y


	transaction Tinit { 
	 input = _
	 output = 1 BTC : fun(s1, s2, sCur) .
	 versig(pubkeyCur; sCur) ||
	 checkDate deadline: 
	 versig(pubkeyCur2; sCur) &&
	 (versig(pubkeyA, pubkeyB, pubkeyC; s1, s2))
	}

	transaction T1(pubKeyS) {
	    input = Tinit@0 :  sig(privKeyA) sig(privKeyB) sig(privKeyCur2)
	    output = 1 BTC : fun(sS) . versig(pubKeyS; sS)
	}

	transaction T2 {
	    input = Tinit@0 : _ _ sig(privKeyCur)
	    output = 1 BTC : fun(sS) . versig(pubkeyT; sS)
	}

	eval Tinit,T1(pubkey:03101e19883cef323b85a53ce580bb5c7545ff024294c74cf2ee7931ab09c931b2),T2

