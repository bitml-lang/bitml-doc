====================================
Case study
====================================

Your case study is a custody smart contract that handles some funds
seized from someone suspected of illegal activities.
A jury decides if the defendant is innocent;
if so, the seized bitcoins must return to the defendant.
There is no need for the entire jury to judge the defendant innocent, the majority of members is sufficient.

++++++++++++++++++++++++++++++++++++++
Exercise 1 - basic BitML contract
++++++++++++++++++++++++++++++++++++++

Actors:

	* ``A``, ``B``, ``C``: members of the jury
	* ``S``: defendant

Write a contract that implements the flow described above.

Verify that if two jurors agree to return the bitcoins to ``S``,
the contract is liquid.

.. hint::
	
	If you only care if a participant authorizes something, and not what particular contract she authorize,
	you can omit the contract from the strategy.
	Example: in :bitml:`(strategy "A" (do-auth (withdraw "S")))`, you can omit :bitml:`(withdraw "S")`.

The skeleton of your contracts is the following:

.. code-block:: bitml
	
	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "021927aa11df2776adc8fde8f36c4f7116dbfb466d6c2cd500ae3eabc0fcfb0a33")
	(participant "C" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(participant "S" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f829")

	(debug-mode)

	(contract
	 (pre (deposit "A" 1 "txid:something@0") ;; 1 BTC seized
	 )
	 
	 WRITE YOUR CONTRACT HERE
	 
	 WRITE YOUR QUERY HERE
	 )

++++++++++++++++++++++++++++++++++++++
Exercise 2 - extend BitML contract
++++++++++++++++++++++++++++++++++++++


Actors:

	* ``A``, ``B``, ``C``: jurors 
	* ``S``: defendant
	* ``T``: tribunal
	* ``Cur``: curator


Extend the contract as follows.
After two jurors agree that the defendant is innocent, the balance is split in two parts:

 * 0.9 BTC, which can return to the defendant after block 160000000. At any time before the deadline, the curator can oppose the jury decision and send the bitcoins to the tribunal 
 * 0.1 BTC, which goes to the curator as a service fee.

Verify that if two members of the jury and the curator agree to return the bitcoins to ``S``,
the contract is liquid.

Check that the curator gets 0.1 BTC if two members of the jury agree.

++++++++++++++++++++++++++++++++++++++++++++++
Exercise 3 - working with Balzac transactions
++++++++++++++++++++++++++++++++++++++++++++++

For this exercise, you have to write the `Balzac <https://editor.balzac-lang.xyz/>`_ transactions
of the following contract,
which is a modification of the first one.

Write a transaction which locks the seized bitcoin. 
The transaction can be redeemed supplying two out of three
signatures of the jurors AND the signature of the curator, but only after ``2019-06-14``.
The transaction can also be redeemed by the curator alone, so she has until Friday to oppose the decision of the jury.
The identity of the defendant is not known in advance,
so his public key must be a parameter of the transaction that returns the seized bitcoin to him.

++++++++++++++++++++++++++++++++++++++
Exercise 4 - the final boss
++++++++++++++++++++++++++++++++++++++

Actors:

	* ``A1``, ``B1``, ``C1``: jurors of the first jury 
	* ``A2``, ``B2``, ``C2``: jurors of the second jury 
	* ``S``: defendant
	* ``Cur``: curator
	* ``T``: tribunal

The contract is similar to the second one, but if the curator opposes the decision of the jury,
there is another round of judgment. The second round is performed by a second jury.
If the curator opposes the decision of the second jury, the seized bitcoin goes to the tribunal.

.. hint::

	To avoid to repeat the same piece of code multiple times, you can define a constant
	with :bitml:`(define (ContractName) contract)` and use it anywhere with :bitml:`(ref (ContractName))`.
