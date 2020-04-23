********************
BitML Toolchain
********************

|langname| is a domain-specific language for Bitcoin smart contracts, introduced in [CCS18]_.
The |langname| toolchain implements:

* an **IDE** for developing BitML contracts, integrated in the DrRacket IDE [RACKET]_;
* a **compiler** which translates |langname| contracts into *standard* Bitcoin transaction. The compiler is *computationally sound*, meaning that computational attacks (i.e., at the level of Bitcoin transactions) can be detected at the symbolic level of the BitML semantics;
* a **model checker** which verifies security properties of BitML contracts, like their *liquidity* (i.e., funds never remain frozen in a contract [POST19]_), and custom LTL properties. The model checker is based on Maude [MAUDE]_.

We published a paper [ESEC]_ describing out toolchain, 
accompanied by a short video `demonstration <https://www.youtube.com/watch?v=bxx3bM5Pm6c>`_.
We also presented the BitML toolchain at `Scaling Bitcoin 2019 <https://telaviv2019.scalingbitcoin.org/>`_ (`video <https://youtu.be/-gdfxNalDIc?t=5540>`_).

The |langname| toolchain is developed by the `Blockchain@Unica group <http://blockchain.unica.it/>`_
of the `University of Cagliari <https://www.unica.it/unica/en/homepage.page>`_.
The project is open source, and you are welcome to contribute to its
`repositories <https://github.com/bitml-lang>`_.


===================
Contents
===================

.. toctree::
    :maxdepth: 1
    :caption: BitML Tutorial

    installation

    nutshell

    compiler

    verification	      


.. toctree::
    :maxdepth: 1
    :caption: Smart contracts
      
    2p-lottery

    tc

    american-option

    auction

    court-seized-btc

    more-contracts


..        # with overline, for parts
..        * with overline, for chapters
..        =, for sections
..        -, for subsections
..        ^, for subsubsections
..        ", for paragraphs


.. warning ::
	|langname| is intended for research purposes only. 
	Do not use it to create mainnet transactions, or do it at your own risk.

===================
References
===================
	    
	    
   
.. [CCS18] M. Bartoletti, R. Zunino. **BitML: A Calculus for Bitcoin Smart Contracts**. In *ACM SIGSAC CCS*, 2018. Preprint: https://eprint.iacr.org/2018/122.pdf

.. [POST19] M. Bartoletti, R. Zunino. **Verifying liquidity of Bitcoin contracts**. In *Principles of Security and Trust (POST)*, 2019. Preprint: https://eprint.iacr.org/2018/1125.pdf

.. [ESEC] N. Atzei, M. Bartoletti, S. Lande, N. Yoshida, R. Zunino. **Developing secure Bitcoin contracts with BitML**. In Proceedings of the *2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)*. https://dl.acm.org/doi/pdf/10.1145/3338906.3341173

.. [RACKET] https://racket-lang.org/

.. [MAUDE]  http://maude.cs.illinois.edu/w/index.php/The_Maude_System http://maude.sip.ucm.es/strategies/
