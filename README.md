# Commitment_Schemes
***
## Intro
This is a Python library which provides some VC schemes like:
- Catalano & Fiore VC based on RSA assumption => https://eprint.iacr.org/2011/495.pdf
- Catalano & Fiore VC based on CDH assumption => https://eprint.iacr.org/2011/495.pdf
- Pointproofs base on CDH assumption          => https://eprint.iacr.org/2020/419.pdf
- KVaC: Key-Value Commitments for Blockchains and Beyond => https://eprint.iacr.org/2020/1161.pdf

---
## Goal
The goal of this library is to provide an open source repository for those who want to develop and test old and new VC schemes. I'm not aiming to develop fast and clean code which provides short time during execution,
but to program schemes to verify their performance.

---
## Dependencies
Here there is a list of dependencies needed:
+ [Charm 0.5.0](https://github.com/JHUISI/charm)
+ [PyCryptoDome](https://www.pycryptodome.org/)
+ [Python 3.9 or less for building Charm](https://github.com/deadsnakes)

---
## TODO List
- [x] Catalano & Fiore VC scheme based on RSA
- [x] Catalano & Fiore VC scheme based on CDH
- [x] Pointproofs base on CDH
- [x]  KVaC: Key-Value Commitments for Blockchains and Beyond based on RSA

---
## What's inside?
Inside every folder, relatively for any branch, there is a couple of benchmarks done on my pc (Ryzen 5 3600x 6 cores / 12 thread no oc). These test aim to show the time required for:
+ Key generation
+ Generation messages (100,1000,10.000 messages) of size from 0 to 1000
+ Commitment calculation
+ Opening calculation
+ Verifiy calculation
+ Update commitment

Also some schemes, like CF RSA,CF CDH and KVaC provides method for:
+ Update proof
+ Aggregation of proof

The master branch also contains a bash script that includes all the schemes implemented previously as environment tests.
## NOTE:
Every csv file contains data expressed in millisecond [ms]

