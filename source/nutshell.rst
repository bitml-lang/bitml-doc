=========================
|langname| in a nutshell
=========================

We illustrate Bitcoin smart contracts in BitML through a series of examples.
Contracts allow two or more participants (denoted as :bitml:`"A"`, :bitml:`"B"`, ...)
to exchange their bitcoins according to the rules they define.

"""""""""""""""""""""""""""""""
Direct payment
"""""""""""""""""""""""""""""""

Assume that :bitml:`"A"` wants to give 1 BTC to :bitml:`"B"` through a contract. 
To this purpose, :bitml:`"A"` must first declare that she owns 1 BTC, and
that she agrees to transfer it under the control of the contract,
using the precondition :bitml:`(pre (deposit "A" 1 "txA@0"))`.
The contract is the following:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 "txA@0"))
	 (withdraw "B"))

The computation of the contract 