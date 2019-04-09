==============================
Compiling |langname| contracts
==============================

|langname| is implemented as Racket language. You can use it either through DrRacket 
or through the racket command-line interpreter. In this tutorial we will use DrRacket.


""""""""""""""""""""""""""""""""""
From BitML to Balzac transactions
""""""""""""""""""""""""""""""""""

We start compiling the following contract:

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "02e76d1d57d47b549d9b297e0a3d71d69139cac2698eb1caa033c5e42322e833d8")

	(generate-keys)

	(define txA "tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600@1")

	(contract
	 (pre (deposit "A" 0.01 (ref txA)))         
	 (withdraw "B"))

The contract is a simple transfer of currency: 1 BTC from :bitml:`"A"` deposit is transferred to :bitml:`"B"`.
Paste the code into a DrRacket window, then hit the "Run" button in the upper right corner.

.. Hint::
	Don't forget to specify you are using |langname| by starting your file with :bitml:`#lang bitml` 

.. figure:: _static/img/compiled.png
	:scale: 90 %
	:class: img-border
	:align: center

DrRacket will show the output of the compilation, which contains the transactions of the contract,
expressed in `Balzac <https://blockchain.unica.it/balzac/docs/>`_.

"""""""""""""""""""""""""""""""
From Balzac to Bitcoin
"""""""""""""""""""""""""""""""

Balzac is an high-level language for writing transactions, verifying their correctness, and compiling them into actual Bitcoin transactions.
We exploit Balzac to compile the transaction of the contract, so we can send them to the Bitcoin network.

Here is the compiled output of the previous contract. 

.. code-block:: balzac

	const pubkeyA1 = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB2 = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const pubkeyA = pubkey:0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1
	const pubkeyB = pubkey:034a7192e922118173906555a39f28fa1e0b65657fc7f403094da4f85701a5f809

	const sigA0 : signature = _ //add signature for output txid:2e647d8566f00a08d276488db4f4e2d9f82dd82ef161c2078963d8deb2965e35@1

	const txA = tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600


	transaction Tinit { 
 	  input = [ tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600@1:sigA0 ]
	  output = 0.01 BTC : fun(sA, sB) . versig(pubkeyA1, pubkeyB2; sA, sB) 
	}


	const sigAT1 : signature = _ 
	const sigBT1 : signature = _ 

	transaction T1 { 
	 input = [ Tinit@0:  sigBT1 sigAT1 ] 
	 output = 0.01 BTC : fun(x) . versig(pubkeyB; x) 
	 
	}

Start by pasting it in the `Balzac web editor <https://editor.balzac-lang.xyz/>`_.

.. figure:: _static/img/balzac1.png
	:scale: 90 %
	:class: img-border
	:align: center

To stipulate the contract :bitml:`"A"` have to sign the transaction :balzac:`Tinit` and send it to the Bitcoin network.
Balzac can compute the signature for her, but it needs her public key. So, she adds it:

.. code-block:: balzac
	
	const privkeyA = key:cUnBMKCcvtpuVcfWajJBEF9uQaeNJmcRM6Vasw1vj3ZkiaoAGEuH

Now, she can compute and add the signature to the transaction :balzac:`Tinit`,
with the :balzac:`sig(_)` function.

.. code-block:: balzac
	
	transaction Tinit { 
	 input = [ tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d
	           012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600@1:sig(privkeyA) ]
	 output = 0.01 BTC : fun(sA, sB) . versig(pubkeyA1, pubkeyB2; sA, sB) 
	}

Firstly, :bitml:`"A"` evaluates the transaction :balzac:`Tinit` adding to the bottom of the file:

.. code-block:: balzac

	eval Tinit

then pressing the button "Evaluate".

.. figure:: _static/img/balzac2.png
	:scale: 90 %
	:class: img-border
	:align: center

The last string in the picture above is the serialized transaction that can be published in the Bitcoin network as
described `here <https://blockchain.unica.it/balzac/docs/raw-transactions.html>`_.

.. Warning::
	In this tutorial we work on the Bitcoin testnet. If you want to use the mainnet (at your own risk), add :balzac:`network mainnet` to your Balzac file.