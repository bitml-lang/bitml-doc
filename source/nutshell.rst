=========================
|langname| in a nutshell
=========================

BitML contracts allow two or more participants (denoted as :bitml:`"A"`, :bitml:`"B"`, ...)
to exchange their bitcoins according to complex pre-agreed rules.

"""""""""""""""""""""""""""""""
Direct payment
"""""""""""""""""""""""""""""""

Assume that :bitml:`"A"` wants to give 1 BTC to :bitml:`"B"` through a contract. 
To this purpose, :bitml:`"A"` first declares that she owns
a transaction output with 1 BTC.
We define this transaction output as follows:

.. code-block:: bitml

	(define txA "txid:4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b@0")

where :bitml:`"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"`
is the transaction identifier, and the trailing :bitml:`"@0"` is the index of the output.
	
The contract is the following:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref txA)))
	 (withdraw "B"))

The precondition :bitml:`(pre (deposit "A" 1 (ref txA)))`
of the contract declares that :bitml:`"A"`
agrees to transfer 1 BTC under the control of the contract.
The actual contract is :bitml:`(withdraw "B")`:
this just transfers the funds deposited into the contract to
participant :bitml:`"B"`.


In the previous contract, the initial deposit has been provided by a transaction output, 
but more in general, a contract can gather money from multiple transactions.
For instance, assume :bitml:`"C"` wants to contribute to the payment. 
We modify the precondition as follows:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref txA))
	      (deposit "C" 1 "txid:999e1c837c76a1b7fbb7e57baf87b309960f5ffefbf2a9b95dd890602272f644@0"))
	 (withdraw "B"))

"""""""""""""""""""""""""""""
Declaring participants
"""""""""""""""""""""""""""""

To compile the previous contract, first we have to declare the participants ad their public keys.

.. code-block:: bitml

	(participant "A" "029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced")
	(participant "B" "0316589526daa876ef27937e48176da08fc95eaef7315fa20a07114d5fb8866553")
	(participant "C" "03c7e157beee3815300c678840988713c9928d986b26fe0dc2533f304c19268a2f")

	(generate-keys)

For each participant, |langname| also need a public key for each piece of the contract
(just :bitml:`(withdraw "B")` in this case). 
We can ask the compiler to take care of them, using :bitml:`(generate-keys)`.


"""""""""""""""""""""""""""""""""""""
Procrastinating payments
"""""""""""""""""""""""""""""""""""""

Assume now that :bitml:`"A"` wants to stipulate a contract where she commits herself to
give 1 BTC to :bitml:`"B"` after a certain block number :bitml:`d`. 
For instance, this contract could represent a
birthday present to be withdrawn only after the birthday date; or the paying of
a rent to the landlord, to be withdrawn only after the 1st of the month. 
:bitml:`"A"` can use the following contract:

.. code-block:: bitml

	(define d 700000)

	(contract
	 (pre (deposit "A" 1 (ref txA)))
	 (after d (withdraw "B")))

This contract locks the deposit until the block number :bitml:`d` is added to the blockchain. 
After then, :bitml:`"B"` can perform action
:bitml:`(withdraw "B")` to redeem 1 BTC from the contract, with no further time limitations.

In the previous contract, if :bitml:`"B"` forgets to withdraw, the money remains within
the contract. The following contract, instead, allows :bitml:`"A"` to recover her money if
:bitml:`"B"` has not withdrawn within a given deadline :bitml:`d1` > :bitml:`d`:

.. code-block:: bitml

	(define d 700000)
	(define d1 705000)

	(contract
	 (pre (deposit "A" 1 (ref txA)))

	 (sum
	 	(after d (withdraw "B"))
	 	(after d1 (withdraw "A"))))

The contract allows two (mutually exclusive) behaviours: 
either :bitml:`"A"` or :bitml:`"B"` can withdraw 1 BTC. 
Before the deadline :bitml:`d` no one can withdraw; 
after :bitml:`d` (but before :bitml:`d1`) only :bitml:`"B"` can withdraw, while after
the :bitml:`d1` both withdraw actions are enabled, so the first one who performs their
withdraw will get the money.

"""""""""""""""""""""""""""""""""""""
Authorizing payments
"""""""""""""""""""""""""""""""""""""
Assume that :bitml:`"A"` is willing to pay 1 BTC to :bitml:`"A"`, 
but only if another participant :bitml:`"O"` gives
his authorization. We can use the following contract:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref txA)))
	 (auth "O" (withdraw "B")))

The semantics of contracts ensures that withdraw :bitml:`"(withdraw "B")"` 
can be performed only if :bitml:`"O"` authorizes it.

We can play with authorizations and summations to construct more complex
contracts. For instance, assume we want to design an *escrow* contract, which
allows :bitml:`"A"` to buy an item from :bitml:`"B"`, authorizing the payment only after she gets the
item. Further, :bitml:`"B"` can authorize a full refund to :bitml:`"A"`, in case there is some problem
with the item. A naïve attempt to model this contract is the following:


.. code-block:: bitml

	(define Naive-escrow 
	  (sum
	    (auth "A" (withdraw "B"))
	    (auth "B" (withdraw "A"))))

If both participants are honest, everything goes smoothly: when :bitml:`"A"` receives
the item, she authorizes the payment to :bitml:`"B"`, otherwise :bitml:`"B"` authorizes the refund.
The problem with this contract is that, if neither :bitml:`"A"` nor :bitml:`"B"` give the authorization,
the money in the contract is frozen. To cope with this issue, we can refine the
escrow contract, by introducing a trusted arbiter :bitml:`"O"` which resolves the dispute:

.. code-block:: bitml

	(define Oracle-escrow 
	  (sum
	    (ref Naive-escrow)
	    (auth "O" (withdraw "A"))
	    (auth "O" (withdraw "B"))))

	(contract
	 (pre (deposit "A" 1 (ref txA)))
	 (ref Oracle-escrow))

The last two branches are used if neither :bitml:`"A"` nor :bitml:`"B"` give their authorizations: in
this case, the arbiter chooses whether to authorize :bitml:`"A"` or :bitml:`"B"` to redeem the deposit.

"""""""""""""""""""""""""""""""""""""
Splitting deposits
"""""""""""""""""""""""""""""""""""""

In all the previous examples, the deposit within the contract is transferred to
a single participant. More in general, deposits can be split in many parts, to
be transferred to different participants. For instance, assume that :bitml:`"A"` wants her
1 BTC deposit to be transferred in equal parts to :bitml:`"B1"` and to :bitml:`"B2"`. 
We can model this behaviour as follows:

.. code-block:: bitml

	(define Pay-split 
	  (split
	    (0.5 -> (withdraw "B1"))
	    (0.5 -> (withdraw "B2"))))


The split construct splits the contract in two or more parallel subcontracts,
each with its own balance. Of course, the sum of their balances must be less
than or equal to the deposit of the whole contract.


We can use split together with the other primitives presented so far to
craft more complex contracts. For instance, assume that :bitml:`"A"` wants pay 0.9 BTC to
:bitml:`"B"`, routing the payment through an intermediary :bitml:`"I"` who can choose whether to
authorize it (in this case retaining a 0.1 BTC fee), or not. Since :bitml:`"A"` does not trust :bitml:`"I"`,
she wants to use a contract to guarantee that: (i) if :bitml:`"I"` authorizes the payment
then 0.9 BTC are transferred to :bitml:`"B"`; (ii) otherwise, :bitml:`"A"` does not lose money. 
We can model this behaviour as follows:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref txA)))
	 (sum
	   (auth "I" (split (0.1 -> (withdraw "I")) 
	                    (0.5 -> (withdraw "B"))))
	    (after d (withdraw "A"))))


The first branch can only be taken if :bitml:`"I"` authorizes the payment: in this case,
:bitml:`"I"` gets his fee, and :bitml:`"B"` gets his payment. Instead, if :bitml:`"I"` denies his authorization, then
:bitml:`"A"` can redeem her deposit after block height :bitml:`d`.


""""""""""""""""""""""""""""""""""""""""""""
Volatile deposits
""""""""""""""""""""""""""""""""""""""""""""


So far, we have seen participants using persistent deposits, that are assimilated
by the contract upon stipulation. Besides these, participants can also use volatile
deposits, which are not assimilated upon stipulation. For instance:

.. code-block:: bitml

	(pre (deposit "A" 1 (ref txA1))
	     (vol-deposit "A" x 1 (ref txA2)))


gives :bitml:`"A"` the possibility of contributing 1 BTC during the contract execution. 
However, :bitml:`"A"` can choose instead to spend her volatile deposit outside the contract.
The variable :bitml:`x` is a handle to the volatile deposit, which can be used as follows:

.. code-block:: bitml

	(define Pay?
	  (put (x) (withdraw "B")))

Since :bitml:`x` is not paid upfront, there is no guarantee that :bitml:`x` will be
available when the contract demands it, as :bitml:`"A"` can spend it for other purposes.

Volatile deposits can be exploited within more complex contracts, to handle
situations where a participant wants to add some funds to the contract. For
instance, assume a scenario where :bitml:`"A1"` and :bitml:`"A2"` want to give :bitml:`"B"` 2 BTC as a present,
paying 1 BTC each. However, :bitml:`"A2"` is not sure a priori she will be able to pay, because
she may need her 1 BTC for more urgent purposes: in this case, :bitml:`"A1"` is willing to
pay an extra bitcoin. We can model this scenario as follows: :bitml:`"A1"` puts 2 BTC as a
persistent deposit, while :bitml:`"A2"` makes available a volatile deposit :bitml:`x` of 1 BTC:

.. code-block:: bitml

	(contract
	 (pre (deposit "A1" 2 (ref txA1))
	      (vol-deposit "A2" x 1 (ref txA2)))
	 (sum
	   (put (x) (split (2 -> (withdraw "B")) 
	                   (1 -> (withdraw "A1"))))
	    (after d (withdraw "B"))))


In the first branch, :bitml:`"A2"` puts 1 BTC in the contract, and the balance is split
between :bitml:`"B"` (who takes 2 BTC, as expected), and :bitml:`"A1"` 
(who takes her extra deposit back). 
The second branch is enabled after :bitml:`d`, and it deals with the case where
:bitml:`"A2"` has not put her deposit by such deadline. In this case, :bitml:`"B"` can redeem 2 BTC,
while :bitml:`"A2"` loses the extra deposit. Note that, in both cases, :bitml:`"B"` will receive 2 BTC.


""""""""""""""""""""""""""""""""""""""
Revealing secrets
""""""""""""""""""""""""""""""""""""""

A useful feature of Bitcoin smart contracts is the possibility for a participant
to choose a secret, and unblock some action only when the secret is revealed.
Further, different actions can be enabled according to the length of the secret.
Secrets must be declared in the contract precondition, as follows:

.. code-block:: bitml

	(pre (secret "A" a "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb")

where :bitml:`"A"` is the participant who owns the secret, :bitml:`a` is its *name*,
and :bitml:`"ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"` is its hash.
We never denote the value of the secret
itself. A basic contract which exploits this feature is the following:

.. code-block:: bitml

	(define PaySecret
	  (reveal (a) (pred (> a 1)) (withdraw "A")))

This contract asks :bitml:`"A"` to commit to a secret of length greater than one,
as stated in the predicate :bitml:`(pred (> a 1))`.
After revealing :bitml:`a`, it allows
:bitml:`"A"` to redeem 1 BTC upon revealing the secret. Until then, the deposit is frozen.

Note that we never refer to the value itself of the secret, rather we use its length.
After compiling to Bitcoin, the actual length of the secret will be increased by η,
where η is a security parameter, large enough to avoid brute-force preimage attack.