from flask import Flask, render_template, jsonify, request
from Rules import Rules
from Arguments import Arguments
from GenerateArguments import generateArgs, emptyArgumentsBase
from GenerateAttacks import generateUndercuts, generateRebuts
from parseAspartix import readKB
from Defeats import defeat, genHisto
from BurdenBasedSemantics import computeBurden, compareArgRankings
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

    Rules.ruleCount = 0
    file = request.files['file']
    if file:
        file.save(os.path.join('uploads', 'KB.txt'))

    readKB(parsedRules)
    parsedRules = sorted(parsedRules, key=lambda rule: int(rule.literalReference.name[1:]))

    return render_template('index.html', parsedRules=parsedRules)

@app.route('/calcArg',  methods=['GET'])
def calcArg():
    global arguments, arg, parsedRules, undercuts, rebuts

    emptyArgumentsBase()
    Arguments.nameCount = 0
    
    arguments = []
    arg = []
    undercuts = {}
    rebuts = {}

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

    burdenValues = computeBurden(arguments, defeatWeakLink, int(iteration))
    ranking = compareArgRankings(burdenValues)

    return render_template('index.html', parsedRules=parsedRules, arguments=arg, undercuts=undercuts, rebuts=rebuts, defeatWeakLink=defeatWeakLink, ranking=ranking)

if __name__ == '__main__':
    app.run(debug=True)