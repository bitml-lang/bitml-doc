==============================
Verifying |langname| contracts
==============================

Other than compiling contracts to transactions, the |langname| toolchain
allows to verify contracts before executing them.

A desirable property of smart contracts is liquidity, 
which requires that the contract balance is always eventually transferred to some participant. 
In a non-liquidcontract, funds can be frozen forever, unavailable to anyone, hence effectively destroyed. 
There are many possible flavours of liquidity, depending e.g. on which
participants are assumed to be honest, and on which are their strategies.

The toolchain can also verify arbitrary security proprieties,
expressed as LTL queries.


"""""""""""""""""""""""""""""""
Liquidity
"""""""""""""""""""""""""""""""

In the following contract, :bitml:`"A"` and :bitml:`"B"` contribute 1 BTC each
for a donation of 2 BTC to either :bitml:`"C"` or :bitml:`"D"`.
We want to check if the contract is liquid or not, without supplying any strategy,
i.e. without knowing which branch :bitml:`"A"` and :bitml:`"B"` will authorize.

This flavour of liquidity is called *strategy-less*.
Intuitively, it corresponds to check 
if the contract is liquid for any possible strategy of any participants,
whether they are honest or not.

To check the liquidity of the following contract, 
we add :bitml:`(check-liquid)` at its end.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")
	(participant "C" "034f5ca30056b9dd89132ca8c7583e6d82b69bc17bb2c1dfef9dea9c3467631e6b")
	(participant "D" "037b60c121050e1fa6e7d5cd299ecc66d87330b2996567004f831c63ef0e2a157e")

	(generate-keys)

	(contract
	 (pre 
	   (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	   (deposit "A" 1 "txid:625bc69c467b33e2ad70ea2817874067604eb42dd5835403f54fb6028bc70168@0"))
	 
	 (sum
	  (auth "A" "B" (withdraw "C"))
	  (auth "A" "B" (withdraw "D")))

	 (check-liquid))

During the compilation of the contract, the tool-chain checks if its liquid. The result is printed before the transactions in a comment-box.

.. code-block:: balzac

	/*
	Model checking result for (check-liquid)

	Result: false
	counterexample({[0 | nil | 'xconf U empty | empty] < (    A, B) : withdraw C + (A, B) : withdraw D, 100000000 BTC > 'xconf,    'C-LockAuthControl} {{A lock withdraw C in 'xconf}[0 | nil | 'xconf U empty    | empty] < Lock((A, B) : withdraw C) + (A, B) : withdraw D, 100000000 BTC >    'xconf,'Rifl} {{A lock withdraw D in 'xconf}[0 | nil | 'xconf U empty |    empty] < Lock((A, B) : withdraw C) + Lock((A, B) : withdraw D), 100000000    BTC > 'xconf,'Finalize}, {[0 | nil | 'xconf U empty | empty] < Lock((A, B)    : withdraw C) + Lock((A, B) : withdraw D), 100000000 BTC > 'xconf,    solution})
	*/

	// Model checking time: 143.0 ms

As we can see, the contract is not liquid. 
In fact, In order to unlock the funds, :bitml:`"A"` and :bitml:`"B"` must agree on the recipient of the donation,
by giving their authorization on the same branch. This contract would be liquid
only by assuming the cooperation between :bitml:`"A"` and :bitml:`"B"`: indeed, :bitml:`"A"` alone cannot
guarantee that the 2 BTC will eventually be donated, as :bitml:`"B"` can choose a different
recipient, or even refuse to give any authorization. 

We can try to modify the contract to handle this situations by adding a timeout branch
that returns their deposits to :bitml:`"A"` and :bitml:`"B"`. 

.. code-block:: bitml

    (contract
      (pre 
        (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
        (deposit "A" 1 "txid:625bc69c467b33e2ad70ea2817874067604eb42dd5835403f54fb6028bc70168@0"))
	 
      (sum
        (auth "A" "B" (withdraw "C"))
        (auth "A" "B" (withdraw "D"))
        (after 700000 (split (1 -> (withdraw "A")) (1 -> (withdraw "B")))))

      (check-liquid))

Now the contract is liquid, and the toolchain confirms it.

.. code-block:: balzac
	
	/*
	Model checking result for (check-liquid)

	Result: true
	*/

	// Model checking time: 322.0 ms


"""""""""""""""""""""""""""""""
Liquidity with strategies
"""""""""""""""""""""""""""""""

In the following contract, :bitml:`"A"` can reveal her secret and redeem its deposit.
Otherwise, after a certain amount of time the block number 700000 will be appended to the blockchain,
:bitml:`"B"` can redeem :bitml:`"A"`'s deposit, after providing his authorization to do so. 

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(generate-keys)

	(contract
	 (pre 
	  (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	  (secret "A" a "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"))
		 
	 (sum
	  (reveal (a) (withdraw "A"))
	  (after 700000 (auth "B" (withdraw "B"))))

	 (check-liquid))

We start by checking the strategy-less liquidity. The contract is not liquid, 
because if neither :bitml:`"A"` reveals her secret nor :bitml:`"B"` gives his authorization, 
the funds will be stuck forever.

.. code-block:: balzac

	/*
	Model checking result for (check-liquid)

	Result: false
	Secrets: a:1 

	counterexample({[0 | 700000 | 'xconf U empty | B, A] <    B : after 700000 : withdraw B + put empty reveal a if True . withdraw A,    100000000 BTC > 'xconf | {A : a # 1},'C-LockAuthRev} {{A lock-reveal a}[0 |    700000 | 'xconf U empty | B, A] Lock({A : a # 1}) | < B : after 700000 :    withdraw B + put empty reveal a if True . withdraw A, 100000000 BTC >    'xconf,'Rifl} {{B lock after 700000 : withdraw B in 'xconf}[0 | 700000 |    'xconf U empty | B, A] Lock({A : a # 1}) | < Lock(B : after 700000 :    withdraw B) + put empty reveal a if True . withdraw A, 100000000 BTC >    'xconf,'Rifl} {{delta 700000}[700000 | nil | 'xconf U empty | B, A] Lock({A    : a # 1}) | < Lock(B : after 700000 : withdraw B) + put empty reveal a if    True . withdraw A, 100000000 BTC > 'xconf,'Finalize}, {[700000 | nil |    'xconf U empty | B, A] Lock({A : a # 1}) | < Lock(B : after 700000 :    withdraw B) + put empty reveal a if True . withdraw A, 100000000 BTC >    'xconf,solution})
	*/

	// Model checking time: 104.0 ms

.. code-block:: bitml

	(contract
	 (pre 
	  (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	  (secret "A" a "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"))
		 
	 (sum
	  (reveal (a) (withdraw "A"))
	  (after 700000 (auth "B" (withdraw "B"))))

	 (check-liquid
	  (strategy "A" (do-reveal a))))

.. code-block:: balzac

	/*
	Model checking result for (check-liquid (strategy A (do-reveal a)))

	Result: true
	*/

	// Model checking time: 90.0 ms


"""""""""""""""""""""""""""""""
Quantitative liquidity
"""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""
Custom LTL queries
"""""""""""""""""""""""""""""""