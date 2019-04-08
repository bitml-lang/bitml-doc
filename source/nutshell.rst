=========================
|langname| in a nutshell
=========================

BitML contracts allow two or more participants (denoted as :bitml:`"A"`, :bitml:`"B"`, ...)
to exchange their bitcoins according to complex pre-agreed rules.

"""""""""""""""""""""""""""""""
Direct payment
"""""""""""""""""""""""""""""""

Assume that :bitml:`"A"` wants to give 1 BTC to :bitml:`"B"` through a contract. 
To this purpose, :bitml:`"A"` must first declare that she owns 1 BTC, and
that she agrees to transfer it under the control of the contract.

.. code-block:: bitml
	(define txA "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b@0")
	
using the precondition :bitml:`(pre (deposit "A" 1 (ref txA)))`.
The contract is the following:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 "txA@0"))
	 (withdraw "B"))

The computation of the contract 
