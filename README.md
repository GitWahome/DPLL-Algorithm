The Input method is as listed in the KB i.e [{A},{C,D}]. A, C, D Are instances of literal. 
An overload on __neg__ has been performed to allow for false valued and negative literalsI included both the DPLL and a BRUTEFORCE approach optimized for String Evals of the Conjuctive Normal Form generator in string form(The use of key python words is necessary to allow eval to work). The output is as follows ["Satisfiability",["Satisfying model example"]] where "true"=True,"false"=False,"free"=Either Value works.
 
UnitClause and Pure Heuristics and implemented in DPLL.  It also takes inputs in
the same manner but modifies them to a new form to function correctly. It is a modified version of AIMA
and Gordon's implementations, Links in the acknowledgement.
