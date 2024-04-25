from flask import Flask, render_template, jsonify, request
import Literals
import Rules
import Arguments
from GenerateArguments import generateArgs, resetArgumentsBase
from GenerateAttacks import generateUndercuts, generateRebuts
from Defeats import defeat
from collections import defaultdict

app = Flask(__name__)

arguments = []
arg = []
rules = {}
undercuts = {}
rebuts = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genReg', methods=['POST'])
def genReg():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            parsedRules = set()
            readKB(parsedRules, uploaded_file)
        print(parsedRules)
    return render_template('index.html', parsedRules=parsedRules)

@app.route('/calcArg',  methods=['GET'])
def calcArg():
    global arguments, arg, rules, undercuts, rebuts

    resetArgumentsBase()
    Arguments.Arguments.nameCount = 0
    
    arguments = []
    arg = []
    rules = {}
    undercuts = {}
    rebuts = {}

    a = Literals.Literals("a", True)
    aF = Literals.Literals("a", False)
    b = Literals.Literals("b", True)
    bF = Literals.Literals("b", False)
    c = Literals.Literals("c", True)
    cF = Literals.Literals("c", False)
    d = Literals.Literals("d", True)
    dF = Literals.Literals("d", False)
    eF = Literals.Literals("e", False)

    r1 = Literals.Literals("r1", False)
    r2 = Literals.Literals("r2", False)
    r3 = Literals.Literals("r3", False)
    r4 = Literals.Literals("r4", False)
    r5 = Literals.Literals("r5", False)
    r6 = Literals.Literals("r6", False)
    r7 = Literals.Literals("r7", False)
    r8 = Literals.Literals("r8", False)
    r9 = Literals.Literals("r9", False)

    rule1 = Rules.Rules({}, aF, False, r1)
    rule2 = Rules.Rules({bF, dF}, cF, False, r2)
    rule3 = Rules.Rules({c}, dF, False, r3)
    
    rule4 = Rules.Rules({aF}, d, True, r4)
    rule5 = Rules.Rules({}, bF, True, r5, 1)
    rule6 = Rules.Rules({}, c, True, r6, 1)
    rule7 = Rules.Rules({}, dF, True, r7, 0)
    rule8 = Rules.Rules({cF}, eF, True, r8)
    rule9 = Rules.Rules({c}, r4.negate(), True, r9)
    print(len(rules))
    rules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}

    print(len(arguments))
    print("mtn apres")
    arguments = generateArgs(rules)
    print(len(arguments))

    arg = sorted(arguments, key=lambda arg: int(arg.name[1:]))
    return render_template('index.html', arguments=arg)

@app.route('/calcAttaq',  methods=['GET'])
def calcAttaq():
   global arguments, arg, rules, undercuts, rebuts
   undercuts = generateUndercuts(arguments, rules)
   rebuts = generateRebuts(arguments)
   return render_template('index.html', arguments=arg, undercuts=undercuts, rebuts=rebuts)

@app.route('/calcDefeats', methods=['POST'])
def calcDefeats():
    global arguments, arg, rules, undercuts, rebuts
    method = request.form['method']
    principal = request.form['principal']
    
    defeatWeakLink = defaultdict(set)

    for rebut in rebuts:
        for (arg1, arg2) in rebuts[rebut]:
            defeatTuple = defeat(arg1, arg2, method, principal)
            if defeatTuple is not None:
                defeatWeakLink[arg1.topRule.conclusion].add(defeatTuple)
    return render_template('index.html', arguments=arg, undercuts=undercuts, rebuts=rebuts, defeatWeakLink=defeatWeakLink)

def readKB(parsedRules, uploaded_file):
    tmpPreLit1 = Literals.Literals("tmp2", False)
    tmpPreLit2 = Literals.Literals("tmp1", False)
    tmpCclLit = Literals.Literals("ccl1", False)
    for f in uploaded_file.readlines():
        [text, premises, conclusion, fleche] = element(f.decode('utf-8'))
        print(text, premises, fleche, conclusion)
        if fleche == "=>":
            if len(premises) > 1:
                if '!' in premises[0]:
                    print(premises[0][0][1], "test")
                    tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                else:
                    print(premises[0][0])
                    tmpPreLit1 = Literals.Literals(premises[0], True)
                if '!' in premises[1]:
                    print(premises[1][0])
                    tmpPreLit2 = Literals.Literals(premises[0][1:], True)
                else:
                    print(premises[1][0])
                    tmpPreLit2 = Literals.Literals(premises[0], False)
                if '!' in conclusion[0]:
                    print(conclusion[0][0])
                    tmpCclLit = Literals.Literals(conclusion[0], True)
                else:
                    print(conclusion[0][0])
                    tmpCclLit = Literals.Literals(conclusion[0], False)
                if len(conclusion) > 1:
                    parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, True, text[0], conclusion[1]))
                if len(conclusion) == 1:
                    parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, True, text[0]))
            if len(premises) == 1 and premises[0] != '':
                if '!' in premises[0]:
                    tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                else:
                    tmpPreLit1 = Literals.Literals(premises[0], False)
                if '!' in conclusion[0]:
                    tmpCclLit = Literals.Literals(conclusion[0], True)
                else:
                    tmpCclLit = Literals.Literals(conclusion[0], False)
                if len(conclusion) > 1:
                    # print(tmpPreLit1)
                    parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, True, text[0], conclusion[1]))
                if len(conclusion) == 1 and conclusion[0] != '':
                    parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, True, text[0]))
        if fleche == '->':
            if len(premises) > 1:
                if '!' in premises[0]:
                    tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                else :
                    tmpPreLit1 = Literals.Literals(premises[0], False)
                if '!' in premises[1]:
                    tmpPreLit1 = Literals.Literals(premises[1][1:], True)
                else :
                    tmpPreLit1 = Literals.Literals(premises[1], False)
                if '!' in conclusion[0]:
                    tmpCclLit = Literals.Literals(conclusion[0], True)
                else:
                    tmpCclLit = Literals.Literals(conclusion[0], False)
                if len(conclusion) > 1:
                    parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, False, text[0], conclusion[1]))
                if len(conclusion) == 1:
                    parsedRules.add(Rules.Rules({tmpPreLit1, tmpPreLit2}, tmpCclLit, False, text[0]))
            if len(premises) == 1 and premises[0] != '':
                if '!' in premises[0]:
                    tmpPreLit1 = Literals.Literals(premises[0][1:], True)
                else:
                    tmpPreLit1 = Literals.Literals(premises[0], False)
                if '!' in conclusion[0]:
                    tmpCclLit = Literals.Literals(conclusion[0], True)
                else:
                    tmpCclLit = Literals.Literals(conclusion[0], False)
                if len(conclusion) > 1:
                    parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, False, text[0], conclusion[1]))
                if len(conclusion) == 1 and conclusion[0] != '':
                    print(tmpPreLit1)
                    parsedRules.add(Rules.Rules(tmpPreLit1, tmpCclLit, False, text[0]))
        return parsedRules
    else :
        print("pas de fichier KB.txt")

def element(f):
    regle = f.strip()
    text = []
    sous = []
    premises = []
    conclusion = []
    fleche = ''
    elements = regle.split(' ', 1)
    if len(elements) > 1:
        text.append(elements[0])
        if '=>' in elements[1]:
            sous = elements[1].split('=>',1)
            fleche = '=>'
        else:
            sous = elements[1].split('->',1)
            fleche = '->'
        if len(sous) > 1:
            premises = [sous[0].split(',')]
            conclusion = sous[1].split(' ')
        
    return text, premises, conclusion, fleche