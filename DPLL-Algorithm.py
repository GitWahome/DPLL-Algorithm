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
            return eval("['{}','{}' ]".format('not',self.name))
def CNFGenerator(KB_CNF):
    outer = ["and"]
    for sets in KB_CNF:
        inner = ["or"]
        for lit in sets:
            inner.append(lit.__repr__())
        outer.append(inner)
    #sCNF = " and ".join(outer)
    return outer


def listifyWithConnectivesAt0(KB_CNF):
    KB_CNF=CNFGenerator(KB_CNF)
    if type(KB_CNF) is str:  # must be a single positive literal
        return ["and", ["or", KB_CNF]]
    elif KB_CNF[0] == "not":  # must be a single negative literal
        return ["and", ["or", KB_CNF]]
    elif KB_CNF[0] == "or":  # a single clause
        return ["and", KB_CNF]
    else:
        result = ["and"]
        for c in KB_CNF[1:]:
            if type(c) == str:
                result.append(["or", c])
            elif c[0] == "not":
                result.append(["or", c])
            else:
                result.append(c)
    return result


def allClausesTrue(KB_CNF, model):  # at least one member of model in each clause
    for clause in KB_CNF[1:]:  # skip the "and"
        if len([var for var in clause[1:] if var in model]) == 0:
            return False
    return True


def literalNegations(model):  # returns the compliment of each model literal
    result = []
    for literal in model:
        if type(literal) is str:
            result.append(["not", literal])
        else:
            result.append(literal[1])
    return result


def someClausesUnsatisfiable(KB_CNF, model):  # some clause cannot be satisfied
    negatedModel = literalNegations(model)
    for clause in KB_CNF[1:]:
        if len([var for var in clause[1:] if var not in negatedModel]) == 0:
            return True
    return False


def pureLiteral(KB_CNF, model):  # finds 1 pure literal not already in model
    negatedModel = literalNegations(model)
    potentialSolutions = []
    for clause in KB_CNF[1:]:
        if len([var for var in clause[1:] if var in model]) == 0:
            # clause not yet satisfied by model
            potentialSolutions = potentialSolutions + [var for var in clause[1:]]
    candidateCompliments = literalNegations(potentialSolutions)
    pureClause = [var for var in potentialSolutions if var not in candidateCompliments]
    for var in pureClause:
        if var not in model and var not in negatedModel:
            return var
    return False


def unitClause(KB_CNF, model):  # finds 1 literal not in model appearing by itself in a clause
    modelCompliments = literalNegations(model)
    for clause in KB_CNF[1:]:
        remaining = [var for var in clause[1:] if var not in modelCompliments]
        if len(remaining) == 1:
            if remaining[0] not in model:
                return remaining[0]
    return False


def pickSymbol(KB, model):  # finds a positive literal not in model or model literalNegations
    combined = model + literalNegations(model)
    for clause in KB[1:]:
        for literal in clause[1:]:
            if type(literal) is str and literal not in combined:
                return literal
    return False
def DPLL_MainOperator(cnf, model):
    if allClausesTrue(cnf, model):
        return model
    if someClausesUnsatisfiable(cnf, model):
        return False
    pure = pureLiteral(cnf, model)
    if pure:
        return DPLL_MainOperator(cnf, model + [pure])
    unit = unitClause(cnf, model)
    if unit:
        return DPLL_MainOperator(cnf, model + [unit])
    pick = pickSymbol(cnf, model)
    if pick:
        # try positive
        result = DPLL_MainOperator(cnf, model + [pick])
        if result:
            return result
        else:
            # try negative
            result = DPLL_MainOperator(cnf, model + [['not', pick]])
            if result:
                return result
            else:
                return False


def DPLL_Satisfiable(KB):
    satifiable = DPLL_MainOperator(listifyWithConnectivesAt0(KB), [])
    if type(satifiable) is bool:
        return (bool(satifiable), "NO VALID MODEL")
    truthV = {}
    for vals in satifiable:
        if type(vals) is str:
            truthV[vals]="true"
        elif type(vals) is list:
            truthV[vals[1]] = "false"
    if not satifiable:
        return (bool(satifiable),"NO VALID MODEL")
    else:
        setAll = []
        for i in KB:
            for j in i:
                setAll.append(j.name)
        setAll = set(setAll)
        model = dict(zip(setAll, ["free"] * len((setAll))))
        for vals in truthV:
            try:
                del(model[vals])
            except:
                pass
        finalSolnModel = {**truthV,**model}
        return (bool(satifiable), finalSolnModel)
"""
Test some KBs.
"""

A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
E = Literal('E')
F = Literal('F')
G = Literal('G')
H = Literal('G')
I = Literal('G')
J = Literal('G')
K = Literal('G')
L = Literal('G')
M = Literal('G')



KB1=[{A},{-A}]
KB = [{A, B},{A, -C},{-A, B, D}]
KB1=[{A},{-A}]
KB2 = [{A, B},{A, -C},{-A, B, D}]
KB3 = [{A, B},{-A, -B},{C, D, E}]
KB4 = [{A, B},{-C, -C},{-D, E, F}]
KB5 = [{A, A},{-A, -A},{B, B},{-B,-B},{C,C},{-C,-C}]
KB6 = [{A, A},{-B},{C},{-D,-E},{F},{G,H},{-I,-J,K,L,-M}]
KB7 = [{A, C},{F, -G},{-E, F, D}]
print(DPLL_Satisfiable(KB6))

"""
Fig 7.20 #Never Implemented this test. I was confused by this one. 
"""
stench = Literal("stench")
breeze = Literal("breeze")
glitter = Literal("glitter")
bump = Literal("bump")
scream = Literal("scream")
percepts=[stench,breeze, glitter,bump,scream]

def  HybridWumpusAgent(percepts):

    action = None
    return action



