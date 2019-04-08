=========================
|langname| in a nutshell
=========================

BitML contracts allow two or more participants (denoted as :bitml:`"A"`, :bitml:`"B"`, ...)
to exchange their bitcoins according to complex pre-agreed rules.

"""""""""""""""""""""""""""""""
Direct payment
"""""""""""""""""""""""""""""""

Assume that :bitml:`"A"` wants to give 1 BTC to :bitml:`"B"` through a contract. 
To this purpose, :bitml:`"A"` must first declare that she owns
a transaction output with 1 BTC.
We define this transaction output as follows:

.. code-block:: bitml

	(define txA "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b@0")

where :bitml:`"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"`
is the transaction identifier, and the trailing :bitml:`"@0"` is the index of the output.
	
The contract is the following:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 "txA@0"))
	 (withdraw "B"))

The precondition :bitml:`(pre (deposit "A" 1 (ref txA)))`
of the contract declares that :bitml:`"A"`
agrees to transfer 1 BTC under the control of the contract.
The actual contract is :bitml:`(withdraw "B")`:
this just transfers the funds deposited into the contract to
participant :bitml:`"B"`.



