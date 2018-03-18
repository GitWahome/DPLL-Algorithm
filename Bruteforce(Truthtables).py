"""
-I created a Literal class that will hold within it the Literal used in our clauses.
-The neg returns another instance of Literal that is not self because negative Literals have a False sign
and redeclaration would falsify the positive version which would mess things up.
-I have a repr method to print out the literal in question together with the sign.
"""
class Literal:
    def __init__(self, name, sign=True):
        self.name = name
        self.value =sign

    def __neg__(self):
        return Literal(self.name,False)

    """
    -While I am technically supposed to use -, I use not since it is a keyword in python and I will use it
    when evaluating my function. 
    -It really simplifies things especially during the recursive search for a 
    satisfactory model. 
    -I make use of brackets to enforce the order of evaluation in my CNF. 
    """
    def __repr__(self):
        if self.value:
            return self.name
        else:
            return str(" not "+self.name+"")
"""
I used this function to count the number of literals in the KB(Disregarding the negative sign) so
as to generate a sensible number of models in the generator. 
-This function returns all possible model which
will serve as our search domain and the set of All literals which I map to the true-false-free values in the CNF
for subsequent evaluation.
"""
def modelsGenerator(KB):
    setAll=[]
    for i in KB:
        for j in i:
            setAll.append(j.name)
    import itertools
    AllModels = list(itertools.product(["True", "False", "None"], repeat=len(set(setAll))))
    return (AllModels,set(setAll))
"""
-This little baby here generates a string version of the CNF from the KB. 
-The 's' prepending the CNF variable denotes this. 
-I leave in a number of curly brackets to allow for the input of the values.
"""
def CNFGenerator(KB):
    outer = []
    for sets in KB:
        inner = []
        for lit in sets:
            inner.append(lit.__repr__())
        innerBr = str("({})".format(" or ".join(inner)))
        outer.append(innerBr)
    sCNF = " and ".join(outer)
    return sCNF

def DPLL_SatisfiableBrute(KB):
    """
    In here are all possible true, false and none(which is equivalent to free for me) for the stated number
    of literals. I will test the solutions iteratively and if one of them returns true, I will terminate the
    search and return the model that satisfies our KB.
    """
    possibleSolutions, KBLiterals=modelsGenerator(KB)
    """
    Print the KB because the order is flipped. This allows you to adjust to the order of the truth values.
    """
    print("THIS IS OUR KB: {}".format(KB))
    sCNF = CNFGenerator(KB)
    print("OUR KB IN STRING AND CNF FORMAT IS: {}".format(sCNF))
    """
    -Here, I now search for a solution in the domain of possible solutions.
    -I do it by creating a dictionary mapping the Literals to various truth values be it true, false or None.
    -After doing this, I go through the generated sCNF replacing the symbol with the equivalent truth value.
    -Remember the use of not? This is where it comes in handy. I don't have to worry about the negatives since
    they were covered.
    -Please not, I did not do a bruteforce on this. I evaluated the individual CNFs parsin.
    """
    for potential in possibleSolutions:
        valuesDictionary = dict(zip(KBLiterals, potential))
        sCNFList = [chars for chars in sCNF]
        for vals in sCNFList:
            try:
                sCNFList[sCNFList.index(vals)]=valuesDictionary[vals]
            except:
                pass
        """
        And now we test if the value is actually true. If it is, we have satisfied the model
        """
        satisfiable = eval(''.join(sCNFList))
        """
        As soon as a valid solution model is found, the search is terminated and the solution returned.
        """
        if satisfiable:
            return (satisfiable, valuesDictionary)
    return (False, "NO VALID MODEL.")





A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
E = Literal('E')
F = Literal('F')
G = Literal('G')

#Test Cases
KB1=[{A},{-A}]
KB2 = [{A, B},{A, -C},{-A, B, D}]
KB3 = [{A, B},{-A, -B},{C, D, E}]
KB4 = [{A, B},{-C, -C},{-D, E, F}]
KB5 = [{A, A},{-A, -A},{B, B},{-B,-B},{C,C},{-C,-C}]
KB6 = [{A, C},{F, -G},{-E, F, D}]

#From Assignment
KB = [{A, B},{A, -C},{-A, B, D}]
TestKB=KB #Paste KB here or paste up with a number and assign to this.
(satisfiable, model) = DPLL_SatisfiableBrute(TestKB)
print("\nThe KB {} is satisfiable: {}."
      "\nAn example of a satisfactory model is: {}".format(TestKB, satisfiable,model))
