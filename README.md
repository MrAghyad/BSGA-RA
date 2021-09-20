# BSGA-RA
A Co-evolutionary Genetic Algorithms Approach To Detect Video Game Bugs

## Abstract
Video games systems are known for their complexity, concurrency and non-determinism, which makes them prone to challenging tacit bugs. Video games development is costly and the corresponding verification process is tiresome. Testing the nondeterministic and concurrent behaviors of video games systems is not only crucial but also challenging, especially when the game state space is huge. Accordingly, typical software testing approaches are neither suitable nor effective to find related bugs. Novel automated approaches to support video game testing are needed. This problem has caught researchers’ attention recently. Approaches found in the literature have tried to address two sub problems: modeling and uncovering bugs. Colored Petri nets is known to support modeling and verifying concurrent and nondeterministic systems. Search approaches have been used in the literature to check the availability of faulty states through exploring state spaces. However, these approaches tend to lack adaptability to test different video games systems due to the limitations of the defined fitness functions, in addition to difficulties in searching huge state spaces due to exhaustive and unguided search. The availability of approaches that guide and direct the searching process of such bugs is mandatory. Thus, in this study we address this problem as we present a potential solution for automated software testing using collaborative work of two genetic algorithms (i.e. co-evolutionary) agents, where our approach is applied to colored Petri nets representations of the software workflow. The results of our experiments have shown the potential of the proposed approach in effectively finding bugs automatically.

## About Repository
This repository is meant to provide details regarding the experiments, systems requirements, manually created rules, and outputs. 
The repository is divided into the following:
1. [Platformer Game (Experiments A & D)](https://github.com/MrAghyad/BSGA-RA/tree/main/ExperimentA%26D-Platformer)
2. [Rogue-like Game (Experiment B)](https://github.com/MrAghyad/BSGA-RA/tree/main/ExperimentB-Rogue-like)
3. [InfiniteRunner Game (Experiment C)](https://github.com/MrAghyad/BSGA-RA/tree/main/ExperimentC-InfiniteRunner)
4. [Software System (Experiment E)](https://github.com/MrAghyad/BSGA-RA/tree/main/ExperimentE-SoftwareSystem)
