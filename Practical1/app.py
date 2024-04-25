from flask import Flask, render_template, jsonify, request
import Literals
import Rules
import Arguments
from GenerateArguments import generateArgs
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

@app.route('/calcArg',  methods=['GET'])
def calcArg():
    global arguments, arg, rules, undercuts, rebuts
    arguments = []
    arg = []
    rules = {}
    undercuts = {}
    rebuts = {}

    print(len(arguments))
    print(len(arg))
    print(len(rules))
    print(len(undercuts))
    print(len(rebuts))

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
