from flask import Flask, render_template, jsonify
from GenerateArguments import generateArgs
import Literals
import Rules
import Arguments

app = Flask(__name__)

employees = [
   {'id': 0,
	'Nom': 'Dupont',
	'Prénom': 'Jean',
	'Fonction': 'Développeur',
	'Ancienneté': '5'},
   {'id': 1,
	'Nom': 'Durand',
	'Prénom': 'Elodie',
	'Fonction': 'Directrice Commerciale',
	'Ancienneté': '4'},
   {'id': 2,
	'Nom': 'Lucas',
	'Prénom': 'Jérémie',
	'Fonction': 'DRH',
	'Ancienneté': '4'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcArg',  methods=['GET'])
def calcArg():
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
    arg = generateArgs(rules)
    return render_template('index.html', arguments=arg)
