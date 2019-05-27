==============================
Verifying |langname| contracts
==============================

Other than compiling contracts to transactions, the |langname| toolchain
allows to verify contracts before executing them.

A desirable property of smart contracts is **liquidity**, 
which requires that the contract balance is always eventually transferred to some participant. 
In a non-liquid contract, funds can be frozen forever, unavailable to anyone, hence effectively destroyed. 
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

This flavour of liquidity is called **strategy-less**.
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

	(debug-mode)

	(contract
	 (pre 
	   (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	   (deposit "A" 1 "txid:625bc69c467b33e2ad70ea2817874067604eb42dd5835403f54fb6028bc70168@0"))
	 
	 (choice
	  (auth "A" "B" (withdraw "C"))
	  (auth "A" "B" (withdraw "D")))

	 (check-liquid))

During the compilation of the contract, the tool-chain checks if it is liquid. The result is printed before the transactions in a comment-box.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-liquid)

	Result: false
	counterexample({[0 | nil | 'xconf U empty | empty] < (    A, B) : withdraw C + (A, B) : withdraw D, 100000000 satoshi > 'xconf,    
	'C-LockAuthControl} {{A lock withdraw C in 'xconf}[0 | nil | 'xconf U empty    | empty] < Lock((A, B) : withdraw C) + (A, B) : withdraw D, 100000000 satoshi >    
	'xconf,'Rifl} {{A lock withdraw D in 'xconf}[0 | nil | 'xconf U empty |    empty] < Lock((A, B) : withdraw C) + Lock((A, B) : withdraw D), 100000000    satoshi > 'xconf,'Finalize}, {[0 | nil | 'xconf U empty | empty] < Lock((A, B)    : withdraw C) + Lock((A, B) : withdraw D), 100000000 satoshi > 'xconf,    solution})
	Model checking time: 143.0 ms
	=============================================================================*/


As we can see, the contract is not liquid. 
In fact, In order to unlock the funds, :bitml:`"A"` and :bitml:`"B"` must agree on the recipient of the donation,
by giving their authorization on the same branch. This contract would be liquid
only by assuming the cooperation between :bitml:`"A"` and :bitml:`"B"`: indeed, :bitml:`"A"` alone cannot
guarantee that the 2 BTC will eventually be donated, as :bitml:`"B"` can choose a different
recipient, or even refuse to give any authorization. 

We can try to modify the contract to handle this situations by adding a timeout branch
with :bitml:`(after 700000 (split (1 -> (withdraw "A")) (1 -> (withdraw "B"))))`.
The new branch locks the contract until the block number 700000 is appended to the blockchain,
modeling a delay.
After the corresponding time passes, it unlocks and returns their deposits to :bitml:`"A"` and :bitml:`"B"`.

.. code-block:: bitml

    (contract
      (pre 
        (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
        (deposit "A" 1 "txid:625bc69c467b33e2ad70ea2817874067604eb42dd5835403f54fb6028bc70168@0"))
	 
      (choice
        (auth "A" "B" (withdraw "C"))
        (auth "A" "B" (withdraw "D"))
        (after 700000 (split (1 -> (withdraw "A")) (1 -> (withdraw "B")))))

      (check-liquid))

Now the contract is liquid, and the toolchain confirms it.

.. code-block:: balzac
	
	/*=============================================================================
	Model checking result for (check-liquid)

	Result: true
	Model checking time: 322.0 ms
	=============================================================================*/

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

	(debug-mode)

	(contract
	 (pre 
	  (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	  (secret "A" a "f9292914bfd27c426a23465fc122322abbdb63b7"))
		 
	 (choice
	  (reveal (a) (withdraw "A"))
	  (auth "B" (after 700000 (withdraw "B"))))

	 (check-liquid))

We start by checking the strategy-less liquidity. 
As the result of the verification shows, the contract is not liquid.
This is because if neither :bitml:`"A"` reveals her secret nor :bitml:`"B"` gives his authorization, 
the funds will be stuck forever.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-liquid)

	Result: false
	Secrets: a:1 

	counterexample({[0 | 700000 | 'xconf U empty | B, A] <    B : after 700000 : withdraw B + put empty reveal a if True . withdraw A,    100000000 satoshi > 'xconf | {A : a # 1},'C-LockAuthRev} {{A lock-reveal a}[0 |    700000 | 'xconf U empty | B, A] Lock({A : a # 1}) | < B : after 700000 :    withdraw B + put empty reveal a if True . withdraw A, 100000000 satoshi >    'xconf,'Rifl} {{B lock after 700000 : withdraw B in 'xconf}[0 | 700000 |    'xconf U empty | B, A] Lock({A : a # 1}) | < Lock(B : after 700000 :    withdraw B) + put empty reveal a if True . withdraw A, 100000000 satoshi >    'xconf,'Rifl} {{delta 700000}[700000 | nil | 'xconf U empty | B, A] Lock({A    : a # 1}) | < Lock(B : after 700000 : withdraw B) + put empty reveal a if    True . withdraw A, 100000000 satoshi > 'xconf,'Finalize}, {[700000 | nil |    'xconf U empty | B, A] Lock({A : a # 1}) | < Lock(B : after 700000 :    withdraw B) + put empty reveal a if True . withdraw A, 100000000 satoshi >    'xconf,solution})
	Model checking time: 104.0 ms
	=============================================================================*/


The |langname| toolchain allows us to specify the intended behaviour of a participant, called **strategy**.
The security propriety is verified with respect to the specified strategies.

We check if the contract is liquid if the strategy of :bitml:`"A"`
consists in revealing her secret, expressed by :bitml:`(strategy "A" (do-reveal a)))`
as parameter of :bitml:`(check-liquid Strategy ...)`.

We also check the liquidity if :bitml:`"A"` authorizes the second branch of the contract,
with the strategy :bitml:`(strategy "B" (do-auth (auth "B"(after 700000 (withdraw "B")))))`.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(debug-mode)

	(contract
	  (pre 
	   (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	   (secret "A" a "f9292914bfd27c426a23465fc122322abbdb63b7"))
		 
	  (choice
	   (reveal (a) (withdraw "A"))
	   (auth "B" (after 700000  (withdraw "B"))))

	  (check-liquid
	    (strategy "A" (do-reveal a)))
 
	  (check-liquid
	    (strategy "B" (do-auth (auth "B" (after 700000 (withdraw "B")))))))

For both strategies, the contract is liquid.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-liquid (strategy A (do-reveal a)))

	Result: true

	/*=============================================================================
	Model checking result for (check-liquid (strategy B (do-auth (auth B (after 700000 (withdraw B))))))

	Result: true
	Model checking time: 270.0 ms
	=============================================================================*/


"""""""""""""""""""""""""""""""
Quantitative liquidity
"""""""""""""""""""""""""""""""

The previous flavours of liquidity require that no funds remain frozen
within the contract. However, in some cases a participant could accept the fact that a
portion of the funds remain frozen, especially when these funds would be ideally
assigned to other participants. 

In the following contract, :bitml:`"A"` and :bitml:`"B"` put 1 BTC each.
Each of them will get their own BTC back if they reveal their secret.

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809")

	(debug-mode)

	(contract
	  (pre 
	   (deposit "A" 1 "txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1")
	   (deposit "B" 1 "txid:0f795bda36ac661f2b9a626d46049bc14b95b2d0e69f5fb7ccc4c3d767db9f34@1")
	   (secret "A" a "f9292914bfd27c426a23465fc122322abbdb63b7")
	   (secret "B" b "9804ebb0fc4a8329981dd33aaff32b6cb579580a"))
		 
	  (split
	   (1 -> (reveal (a) (withdraw "A")))
	   (1 -> (reveal (b) (withdraw "B"))))

	   (check "A" has-more-than 1
	    (strategy "A" (do-reveal a)))))

In this setting, :bitml:`"A"` is interested in checking if she will get back her bitcoin,
assuming that she reveals her secret. We check it using :bitml:`(check "A" has-more-than 1 (strategy "A" (do-reveal a)))`.

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check A has-more-than 1 (strategy A (do-reveal a)))

	Result: true
	Model checking time: 134.0 ms
	=============================================================================*/

"""""""""""""""""""""""""""""""
Custom LTL queries
"""""""""""""""""""""""""""""""

The following contract is a *timed commitment*, 
where :bitml:`"A"` wants to choose a secret :balzac:`a`, 
and reveal it before the deadline :balzac:`d`; 
if :bitml:`"A"` does not reveal the secret within :balzac:`d`, 
:bitml:`"B"` can redeem the 1 BTC deposit as a compensation.

.. code-block:: bitml

	#lang bitml

	(participant "A" "029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced")
	(participant "B" "022c3afb0b654d3c2b0e2ffdcf941eaf9b6c2f6fcf14672f86f7647fa7b817af30")

	(debug-mode)

	(define (d) 700000)

	(contract
	 (pre (deposit "A" 1 "txA@0")(secret "A" a "f9292914bfd27c426a23465fc122322abbdb63b7"))
	 
	 (choice (reveal (a) (withdraw "A"))
	      (after (ref (d)) (withdraw "B")))

	 (check-query "[]<> (a revealed => A has-deposit>= 100000000 satoshi)")

	 (check-query "[]<> (a revealed \\/ B has-deposit>= 100000000 satoshi)"))

The |langname| toolchain allows us to check custom LTL properties, 
tailored specifically for the contract being verified, using :bitml:`(check-query "query")`. 

In the timed commitment contract, we want the following two properties to be satisfied.

* 	If :bitml:`"A"` reveal her secret, she will get back her deposit. 
	We check this property with :bitml:`(check-query "[]<> (a revealed => A has-deposit>= 100000000 satoshi)")`.

* 	Either :bitml:`"B"` gets to know the secret, or he will get the bitcoin as compensation. 
	We check this property with :bitml:`(check-query "[]<> (a revealed \\/ B has-deposit>= 100000000 satoshi)"))`.

.. note::

	Due to the internal representation of numbers in the model check, all BTC values have to be expressed in **satoshi** when checking custom LTL queries.

The result is true for both queries: 

.. code-block:: balzac

	/*=============================================================================
	Model checking result for (check-query [] (a revealed => <> A has-deposit>= 100000000 satoshi))

	Result: true

	/*=============================================================================
	Model checking result for (check-query []<> (a revealed \/ B has-deposit>= 100000000 satoshi))

	Result: true
	Model checking time: 408.0 ms
	=============================================================================*/

The first LTL property has the same semantic as checking the quantitative liquidity of 1 BTC
if the strategy of :bitml:`"A"` is to reveal her secret, or
:bitml:`(check "A" has-more-than 1 (strategy "A" (do-reveal a)))`.
Instead, the second LTL property cannot be expressed as a combination of liquidity and strategies.

Other that :balzac:`revealed` and :balzac:`has-deposit>=`, you can express your LTL properties with :balzac:`has-deposit`, and :balzac:`has-deposit<=`.