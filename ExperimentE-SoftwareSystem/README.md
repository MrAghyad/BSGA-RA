# Software System
<div align="center">
	<br>
	<img src="https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentE-SoftwareSystem/softwareCPN.png?raw=true">
	<br>
	<em>
	Figure: Software System Petri Nets
	</em>
</div>
<br/>

A shutdown system for a [Korean nuclear power plant](https://ieeexplore.ieee.org/abstract/document/566752). This system checks the state of a nuclear reactor such as power and pressure, in addition, 
it creates a shutdown/trip signal if there is unsafe  situation, such as, very high or low levels of pressure. 
This system is considered non-deterministic due to the parallel executions and randomization it contains. 
This system's representation has been used in the literature as a case study for reachabiltiy analysis of colored Petri nets and finding hazard 
situations. The colored Petri nets model of the system consists of six places and four transitions, 
in addition, the system consists of two rules which were discussed by [Cho et. al](https://ieeexplore.ieee.org/abstract/document/566752). 

This system was selected to further test and push the applicability of the proposed approach. Also, to verify that the proposed approach can be applied to systems other than games.


Note: Petri nets model creation code that was implemented by the authors of this repositry and which was used in the experiments can be found in the following [link](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentE-SoftwareSystem/Software_CPN.py).


## Rules
The following set of requirements and rules were manually created by the authors to serve the purpose of the study, 
where rules were constructed using the proposed CPN-MCL rules scheme.

|Index| Requirement | Rule |
|:---:|:-----------:|:----:|
|0| When pdltrip == 1, pressure shall not exceed 4810 and power shall not exceed 2739 | not ( (@pressure >= 4810) and (@power >= 2739) and (@pdltrip == 1) )|
|1| When pdltrip == 1, pressure shall not be less than 1287 and power shall not exceed 2739  | not ((@pressure <= 1287)  and (@power >= 2739) and (@pdltrip == 1) )|


## Experiments
### Software system - Experiment E: BSGA and RA
in this experiment we study applying our approach (BSGA-RA) on a colored Petri nets representation of a 
shutdown nuclear system to check finding bugs and the ability of breaking rules. 
This experiment was repeated ten times. 


## Places Ranges Used
|   Place  | Value Ranges |
|:--------:|:------------:|
|   power  |   [0, 5000]  |
| pressure |   [0, 5000]  |
|  pdltrip |    [0, 1]    |

