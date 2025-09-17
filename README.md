# Master's Thesis

## Description
This repository contains code developed as part of the master's thesis of Grzegorz Nowakowski, supervised by Prof. Piotr Skowron. The project includes implementations for computing outcomes of voting rules and verifying these outcomes with respect to Core and Pareto optimality. The second part of the code, i.e., the linear programs for Core and Pareto optimality, can be found [here](https://github.com/COMSOC-Community/pabutools/pull/52).

## Directory structure
Below is an overview of the repository contents:
- [code](code/) - helper functions and voting rules not included in pabutools, used by the [notebook](main.ipynb)
- [pabulib](pabulib/) - approval election instances from [pabulib](https://pabulib.org/)
- [outcomes](outcomes/) - computed outcomes of pabulib elections for each voting rule 
- [outputs](outputs/) — runtime results for each voting rule and heuristic, along with graphical representations of these results 
- [latex](latex/) - LaTeX source files of the master's thesis and the compiled thesis itself  
