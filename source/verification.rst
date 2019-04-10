==============================
Verifying |langname| contracts
==============================


"""""""""""""""""""""""""""""""
Liquidity
"""""""""""""""""""""""""""""""

.. code-block:: bitml

	#lang bitml

	(participant "A" "0339bd7fade9167e09681d68c5fc80b72166fe55bbb84211fd12bde1d57247fbe1")
	(participant "B" "02e76d1d57d47b549d9b297e0a3d71d69139cac2698eb1caa033c5e42322e833d8")

	(generate-keys)

	(define txA "tx:02000000000102f28b8ec15a48abd9cda80d1c770ff9770dc0c549ddb1b8013b9e50a8799614aa000000001716001412a88716720982b693ab2bd2a2fcd4d98bdd2485feffffff08d59c3aeafd6003e6e099adde64f17d6ec7950619c22b50466281afa782e9d4000000001716001433845a8590dbf145b52bdd777103d1ddfdaa9cedfeffffff022fac1f000000000017a914e9f772646a0b6174c936806dab1b882e750ac04a8740420f00000000001976a914ded135b86a7ff97aece531c8b97dc8a3cb3ddc7488ac02473044022060135384eafe9a8021e8b8c46da20e7cd5713d581c3f79b1da3d2f7860a1bfed02206ca1ac1616d7ab778bcbb235b4b24286c2181ec171b8cadeaa9ee5f4f78fd330012102d5f8f263a81427330e7f26ba5832a2cd01e960bf145be2101bc0b6bb0fde8c2d0247304402200e02da2228774b47ff03a5a7c1bf1d070d0cec6cd9a08d6862e1855ba33dfb9f0220011511f10aaefbf402b2944b6a877c1ff9890a7fc3e266bbb74318b4540c555d012103ef2a573fbd46356dcbdbedcecc9aa25dcb500512e2be394297475ed157a9cfc6bdb51600@1")

	(contract
 	  (pre (deposit "A" 0.01 (ref txA)))         
 	  (sum
  	    (auth "A" (withdraw "A"))
  	    (auth "B" (withdraw "B")))

  	  (check-liquid))


"""""""""""""""""""""""""""""""
Liquidity with strategies
"""""""""""""""""""""""""""""""



"""""""""""""""""""""""""""""""
Quantitative liquidity
"""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""
Custom LTL queries
"""""""""""""""""""""""""""""""