.. _BitML in a nuthsell:

=========================
|langname| in a nutshell
=========================

BitML contracts allow two or more participants to exchange
their bitcoins according to complex pre-agreed rules.
Below we illustrate the primitives of BitML through a series of
simple examples
(see [CCS18]_ for a reference to BitML syntax and semantics).

The first step in designing a BitML contract is to declare the involved participants.
For instance, we can declare three participants :bitml:`"A"`, :bitml:`"B"` and :bitml:`"C"` as follows:

.. code-block:: bitml

	(participant "A" "029c5f6f5ef0095f547799cb7861488b9f4282140d59a6289fbc90c70209c1cced")
	(participant "B" "0316589526daa876ef27937e48176da08fc95eaef7315fa20a07114d5fb8866553")
	(participant "C" "03c7e157beee3815300c678840988713c9928d986b26fe0dc2533f304c19268a2f")

	(debug-mode)

Each participant is associated to a public key: for instance, :bitml:`"A"`
has the public key :bitml:`"029c...cced"`.
The command :bitml:`(debug-mode)` is needed to generate auxiliary keys
which are used by the BitML compiler,
instead of declaring them as you are supposed to when executing a contract in 
a real life scenario.


"""""""""""""""""""""""""""""""
Simple payments
"""""""""""""""""""""""""""""""

Assume that :bitml:`"A"` simply wants to donate 1 BTC to :bitml:`"B"`. 
To this purpose, :bitml:`"A"` must first declare that she owns
a transaction output with 1 BTC.
We can define this transaction output as follows:

.. code-block:: bitml

	(define (txA) "tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600@1")

In the definition above, :bitml:`"02000000000102f28b...4297475ed157a9cfc6bdb51600"`
are the bytes of the serialized transaction, and the trailing :bitml:`"@0"` is the index of the output.

The contract advertised by :bitml:`"A"` is the following:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref (txA))))
	 (withdraw "B"))

The contract precondition :bitml:`(pre (deposit "A" 1 (ref (txA))))`
declares that :bitml:`"A"`
agrees to transfer the 1 BTC referenced by the transaction output :bitml:`txA`
under the control of the contract.
The actual contract is :bitml:`(withdraw "B")`:
this just transfers the funds deposited into the contract to :bitml:`"B"`.


In the previous contract, the initial deposit has been provided by a transaction output;
more in general, a contract can gather money from more than one transaction.
For instance, assume that another participant :bitml:`"C"` wants to contribute 1 BTC to the donation.
The contract precondition is modified as follows:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref (txA)))
	      (deposit "C" 1 "tx:020000000193c18c921ed3947b862c746ddfe8a8b7459da00825822e09b95c61aaedc71dbf00000000e347304402204b77785e510ab83746732ce435e28a0e46d415ed0ebb8de407c45c66824530bf02202fdf08cd26b5ce376bcb215fe974dddc413be3b74b87e8beae27b1d812c3869d01473044022071b0ced4dd60799531eefe4e61892602637897a18f69f4e5cec22247c59b6c770220768ecc22e772477c8bbd762366d121b0b3d48a3b91334e1a369bbd848373fde3014c516b6b006c766c766b7c6b52210339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe121034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f80952aeffffffff01a0bb0d00000000001976a914ce07ee1448bbb80b38ae0c03b6cdeff40ff326ba88ac00000000@0"))
	 (withdraw "B"))


"""""""""""""""""""""""""""""""""""""
Procrastinating payments
"""""""""""""""""""""""""""""""""""""

Assume now that :bitml:`"A"` wants to donate 1 BTC to :bitml:`"B"`,
but only after a certain time :bitml:`t`.
For instance, the 1 BTC could be a birthday present to be withdrawn
only after the birthday date; or the amount of a rent to the landlord,
to be paid only after the 1st of the month.
We represent the time :bitml:`t` as a `block height <https://bitcoin.org/en/glossary/block-height>`_.
For instance, we set :bitml:`t` to 500000
(note that the block at this height was actually mined on  
`2017-12-18 <https://www.blockchain.com/btc/block-height/500000>`_).

To craft this contract we use the primitive :bitml:`after height contract`,
which locks the :bitml:`contract` until
the block at the given :bitml:`height` is appended to the blockchain.
We also reuse the transaction output :bitml:`txA` from the previous example:

.. code-block:: bitml

	(define (d) 500000)

	(contract
	 (pre (deposit "A" 1 (ref (txA))))
	 (after (ref (t)) (withdraw "B")))

This contract ensures that only after
the block at height :bitml:`t` has been appended to the blockchain,
:bitml:`"B"` will be able to redeem 1 BTC from the contract,
by performing the action :bitml:`(withdraw "B")`.

The following contract allows :bitml:`"A"` to recover her deposit if
:bitml:`"B"` has not withdrawn within a given deadline :bitml:`t1` > :bitml:`t`:

.. code-block:: bitml

	(define (t) 500000)
	(define (t1) 510000)

	(contract
	 (pre (deposit "A" 1 (ref (txA))))

	 (choice
	 	(after (ref (t)) (withdraw "B"))
	 	(after (ref (t1)) (withdraw "A"))))

The contract allows two (mutually exclusive) behaviours: 
either :bitml:`"A"` or :bitml:`"B"` can withdraw 1 BTC. 
Before the deadline :bitml:`t` no one can withdraw; 
after :bitml:`t` (but before :bitml:`t1`) only :bitml:`"B"` can withdraw,
while after the :bitml:`t1` both withdraw actions are enabled,
so the first one who performs their withdraw will get the money.


"""""""""""""""""""""""""""""""""""""
Authorizing payments
"""""""""""""""""""""""""""""""""""""
Assume that :bitml:`"A"` is willing to pay 1 BTC to :bitml:`"A"`, 
but only if an :bitml:`"Oracle"` gives his authorization.
We can use the authorization primitive :bitml:`auth Participant Contract` as follows:

.. code-block:: bitml

	(contract
	 (pre (deposit "A" 1 (ref (txA))))
	 (auth "Oracle" (withdraw "B")))

This contract ensures that :bitml:`(withdraw "B")` 
is performed whenever :bitml:`"Oracle"` authorizes it.

We can play with authorizations and summations to construct more complex
contracts. For instance, assume we want to design an *escrow* contract, which
allows :bitml:`"A"` to buy an item from :bitml:`"B"`, authorizing the payment only after she gets the
item. Further, :bitml:`"B"` can authorize a full refund to :bitml:`"A"`, in case there is some problem
with the item. A naïve attempt to model this contract is the following:


.. code-block:: bitml

	(define (Naive-escrow) 
	  (choice
	    (auth "A" (withdraw "B"))
	    (auth "B" (withdraw "A"))))

If both participants are honest, everything goes smoothly: when :bitml:`"A"` receives
the item, she authorizes the payment to :bitml:`"B"`, otherwise :bitml:`"B"` authorizes the refund.
The problem with this contract is that, if neither :bitml:`"A"` nor :bitml:`"B"` give the authorization,
the money in the contract is frozen. To cope with this issue, we can refine the
escrow contract, by introducing a trusted arbiter :bitml:`"O"` which resolves the dispute:

.. code-block:: bitml

	(define (Oracle-escrow) 
	  (choice
	    (auth "A" (withdraw "B")) ; same as
	    (auth "B" (withdraw "A")) ; Naive-escrow
	    (auth "O" (withdraw "A"))
	    (auth "O" (withdraw "B"))))

	(contract
	 (pre (deposit "A" 1 (ref (txA))))
	 (ref (Oracle-escrow)))

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

	(define (Pay-split) 
	  (split
	    (0.5 -> (withdraw "B1"))
	    (0.5 -> (withdraw "B2"))))


The split construct splits the contract in two or more parallel subcontracts,
each with its own balance. Of course, the choice of their balances must be less
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
	 (pre (deposit "A" 1 (ref (txA))))
	 (choice
	   (auth "I" (split (0.1 -> (withdraw "I")) 
	                    (0.5 -> (withdraw "B"))))
	    (after (ref (d)) (withdraw "A"))))


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

	(pre (deposit "A" 1 (ref (txA1)))
	     (vol-deposit "A" x 1 (ref (txA2))))


gives :bitml:`"A"` the possibility of contributing 1 BTC during the contract execution. 
However, :bitml:`"A"` can choose instead to spend her volatile deposit outside the contract.
The variable :bitml:`x` is a handle to the volatile deposit, which can be used as follows:

.. code-block:: bitml

	(define (Pay?)
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
	 (pre (deposit "A1" 2 (ref (txA1)))
	      (vol-deposit "A2" x 1 (ref (txA2))))
	 (choice
	   (put (x) (split (2 -> (withdraw "B")) 
	                   (1 -> (withdraw "A1"))))
	    (after 700000 (withdraw "B"))))


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

	(pre (secret "A" a "f9292914bfd27c426a23465fc122322abbdb63b7")

where :bitml:`"A"` is the participant who owns the secret, :bitml:`a` is its *name*,
and :bitml:`"f9292914bfd27c426a23465fc122322abbdb63b7"` is its :balzac:`hash160` hash.
We never denote the value of the secret
itself. A basic contract which exploits this feature is the following:

.. code-block:: bitml

	(define (PaySecret)
	  (reveal (a) (pred (> a 1)) (withdraw "A")))

This contract asks :bitml:`"A"` to commit to a secret of length greater than one,
as stated in the predicate :bitml:`(pred (> a 1))`.
After revealing :bitml:`a`, it allows
:bitml:`"A"` to redeem 1 BTC upon revealing the secret. Until then, the deposit is frozen.

Note that we never refer to the value itself of the secret, rather we use its length.
After compiling to Bitcoin, the actual length of the secret will be increased by η,
where η is a security parameter, large enough to avoid brute-force preimage attack.
