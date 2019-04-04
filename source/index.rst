********************
BitML Toolchain
********************

|langname| is a domain specific language for specifying smart contracts 
that can be executed on Bitcoin [18CCS]_.
The language is computationally sound, i.e. a vulnerability at the computational level 
can be detected at the symbolic level, allowing us to verify |langname| smart contracts.

The toolchain consists of:

* A compiler, to translate contracts into *standard* Bitcoin transaction
* A verifier, to verify security properties of contract.

The toolchain supports the verification of the various forms of *liquidity* [19POST]_,
which guarantees that funds never remain frozen in a contract, 
as well as other user-defined properties . 

The toolchain is built in Racket [RACKET]_ and Maude [MAUDE]_,
and it is integrated in the DrRacket IDE.



The project is open source, and you are welcome to contribute to our
`repositories <https://github.com/bitml-lang>`_.

|langname| is developed by the `Blockchain@Unica group <http://blockchain.unica.it/>`_
of the `University of Cagliari <https://www.unica.it/unica/en/homepage.page>`_.

**Contents:**


.. toctree::
    :maxdepth: 1
    :caption: Getting Started

    nutshell



.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: Installation and Configuration

    installation


.. toctree::
    :maxdepth: 1
    :caption: Smart contracts
      
    timed-commitment


..        # with overline, for parts
..        * with overline, for chapters
..        =, for sections
..        -, for subsections
..        ^, for subsubsections
..        ", for paragraphs


.. warning ::
	|langname| is intended for research purposes only. 
	Do not use it to create mainnet transactions, or do it at your own risk.


.. rubric:: References

.. [18CCS] M. Bartoletti, R. Zunino. BitML: A Calculus for Bitcoin Smart Contracts. In proceedings of the 2018 ACM SIGSAC CCS 18. Preprint: https://eprint.iacr.org/2018/122.pdf

.. [19POST] M. Bartoletti, R. Zunino. Verifying liquidity of Bitcoin contracts. In Principles of Security and Trust (POST), 2019. Preprint: https://eprint.iacr.org/2018/1125.pdf

.. [RACKET] https://racket-lang.org/

.. [MAUDE]  http://maude.cs.illinois.edu/w/index.php/The_Maude_System http://maude.sip.ucm.es/strategies/