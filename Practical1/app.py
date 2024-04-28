from flask import Flask, render_template, jsonify, request
import Literals
import Rules
import Arguments
from GenerateArguments import generateArgs, resetArgumentsBase
from GenerateAttacks import generateUndercuts, generateRebuts
from parseAspartix import readKB
from Defeats import defeat, genHisto
from BurdenBasedSemantics import calculate_bur_values1
from collections import defaultdict
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

arguments = []
arg = []
parsedRules = set()
undercuts = {}
rebuts = {}
defeatWeakLink = defaultdict(set)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genReg', methods=['POST'])
def genReg():
    global parsedRules
    parsedRules = set()

    Rules.Rules.ruleCount = 0
    file = request.files['file']
    if file:
        file.save(os.path.join('uploads', 'KB.txt'))

    # a = Literals.Literals("a", True)
    # aF = Literals.Literals("a", False)
    # b = Literals.Literals("b", True)
    # bF = Literals.Literals("b", False)
    # c = Literals.Literals("c", True)
    # cF = Literals.Literals("c", False)
    # d = Literals.Literals("d", True)
    # dF = Literals.Literals("d", False)
    # eF = Literals.Literals("e", False)

    # r1 = Literals.Literals("r1", False)
    # r2 = Literals.Literals("r2", False)
    # r3 = Literals.Literals("r3", False)
    # r4 = Literals.Literals("r4", False)
    # r5 = Literals.Literals("r5", False)
    # r6 = Literals.Literals("r6", False)
    # r7 = Literals.Literals("r7", False)
    # r8 = Literals.Literals("r8", False)
    # r9 = Literals.Literals("r9", False)

    # rule1 = Rules.Rules({}, aF, False, r1)
    # rule2 = Rules.Rules({bF, dF}, cF, False, r2)
    # rule3 = Rules.Rules({c}, dF, False, r3)
    
    # rule4 = Rules.Rules({aF}, d, True, r4)
    # rule5 = Rules.Rules({}, bF, True, r5, 1)
    # rule6 = Rules.Rules({}, c, True, r6, 1)
    # rule7 = Rules.Rules({}, dF, True, r7, 0)
    # rule8 = Rules.Rules({cF}, eF, True, r8)
    # rule9 = Rules.Rules({c}, r4.negate(), True, r9)
            
    # parsedRules = {rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9}
    
    readKB(parsedRules)

    return render_template('index.html', parsedRules=parsedRules)

@app.route('/calcArg',  methods=['GET'])
def calcArg():
    global arguments, arg, parsedRules, undercuts, rebuts

    resetArgumentsBase()
    Arguments.Arguments.nameCount = 0
    
    arguments = []
    arg = []
    undercuts = {}
    rebuts = {}

    # print(len(arguments))
    # print("mtn apres")
    arguments = generateArgs(parsedRules)

    arg = sorted(arguments, key=lambda arg: int(arg.name[1:]))

    return render_template('index.html', parsedRules=parsedRules, arguments=arg)

@app.route('/calcAttaq',  methods=['GET'])
def calcAttaq():
   global arguments, arg, parsedRules, undercuts, rebuts
   undercuts = generateUndercuts(arguments, parsedRules)
   rebuts = generateRebuts(arguments)
   return render_template('index.html', parsedRules=parsedRules, arguments=arg, undercuts=undercuts, rebuts=rebuts)

@app.route('/calcDefeats', methods=['POST'])
def calcDefeats():
    global arguments, arg, parsedRules, undercuts, rebuts, defeatWeakLink
    method = request.form['method']
    principal = request.form['principal']
    
    defeatWeakLink = defaultdict(set)

    for rebut in rebuts:
        for (arg1, arg2) in rebuts[rebut]:
            defeatTuple = defeat(arg1, arg2, method, principal)
            if defeatTuple is not None:
                defeatWeakLink[arg1.topRule.conclusion].add(defeatTuple)

    histo = genHisto(defeatWeakLink, arg)

    plt.bar(histo.keys(), histo.values())
    plt.xlabel('Nombre de défaites')
    plt.ylabel('Nombre d\'arguments')
    plt.title('Histogramme des défaites par argument')
    with app.app_context():
        plt.savefig('static/histo.png')
        plt.close()

    return render_template('index.html', parsedRules=parsedRules, arguments=arg, undercuts=undercuts, rebuts=rebuts, defeatWeakLink=defeatWeakLink)


@app.route('/calcRanking', methods=['POST'])
def calcRanking():
    global arguments, arg, parsedRules, undercuts, rebuts, defeatWeakLink
    
    iteration = request.form['rankIteration']

    ranking = calculate_bur_values1(arguments, defeatWeakLink, int(iteration))

    return render_template('index.html', parsedRules=parsedRules, arguments=arg, undercuts=undercuts, rebuts=rebuts, defeatWeakLink=defeatWeakLink, ranking=ranking)

if __name__ == '__main__':
    app.run(debug=True)