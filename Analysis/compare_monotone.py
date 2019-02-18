import pickle
import numpy as np
import Generator
import Parser
from GeneralizedQuantifierModel import SimplifiedQuantifierModel

monotone_set = 'B'
direction = 'down'


def flip_model(model):
    return SimplifiedQuantifierModel(model.B,model.A,model.B-model.AandB,model.AandB)


flip_model_if_needed = flip_model if monotone_set is 'B' else lambda model: model

quantifiers = list(Parser.load_from_file('../results/GeneratedQuantifiers.json').values())
quantifier_indices = []
for (i, quantifier) in enumerate(quantifiers):
    if not quantifier.has_presupposition:
        quantifier_indices.append(i)

with open('../results/generated_meanings.pickle','rb') as file:
    raw_meanings = pickle.load(file)

universe_size = 40
universe = Generator.generate_simplified_models(universe_size)

meanings = [[[[None]*(universe_size-AandB+1) for AandB in range(B+1)] for B in range(universe_size+1)]
            for i in quantifier_indices]

for (i,index) in enumerate(quantifier_indices):
    for (j, model) in enumerate(universe):
        model = flip_model_if_needed(model)
        meanings[i][model.B][model.AandB][model.AminusB] \
        = raw_meanings[index][j] if direction is 'up' else not raw_meanings[index][j]


is_monotone = [[[[None]*(universe_size-AandB+1) for AandB in range(B+1)] for B in range(universe_size+1)]
               for i in quantifier_indices]


def check_monotone_inner(meaning, index, B, AandB, AminusB, truth_found):
    if truth_found:
        if not meaning[B][AandB][AminusB]:
            return False
        if AandB + AminusB is universe_size:
            return True
        if AandB is B:
            return check_monotone(meaning, index, B, AandB, AminusB + 1, True)
        return check_monotone(meaning, index, B, AandB+1, AminusB, True) and check_monotone(meaning, index, B, AandB, AminusB+1, True)

    else:
        if AandB + AminusB is universe_size:
            return True

        if meaning[B][AandB][AminusB]:
            return check_monotone(meaning, index, B, AandB, AminusB, True)

        if AandB is B:
            return check_monotone(meaning, index, B, AandB, AminusB + 1)

        return check_monotone(meaning, index, B, AandB + 1, AminusB) and check_monotone(meaning, index, B, AandB, AminusB + 1)


def check_monotone(meaning, index, B, AandB=0, AminusB=0, truth_found=False):
    if is_monotone[index][B][AandB][AminusB] is None:
        is_monotone[index][B][AandB][AminusB] = check_monotone_inner(meaning,index,B,AandB,AminusB,truth_found)

    return is_monotone[index][B][AandB][AminusB]




monotone_quantifiers = []
non_monotone_quantifiers = []

monotone_cost = []
non_monotone_cost = []

monotone_complexity = []
non_monotone_complexity = []

cost = np.loadtxt('../results/generated_quantifiers_cost.txt')
complexity = np.loadtxt("../results/generated_quantifiers_complexity.txt")

for (i,quantifier_index) in enumerate(quantifier_indices):
    monotone = True
    for B in range(universe_size):
        if not check_monotone(meanings[i], i, B):
            monotone = False
            break

    if monotone:
        monotone_quantifiers.append(quantifiers[quantifier_index])
        monotone_cost.append(cost[i])
        monotone_complexity.append(complexity[i])
    else:
        non_monotone_quantifiers.append(quantifiers[quantifier_index])
        non_monotone_cost.append(cost[i])
        non_monotone_complexity.append(complexity[i])


cost = np.loadtxt('../results/generated_quantifiers_cost.txt')
complexity = np.loadtxt("../results/generated_quantifiers_complexity.txt")

print([str(q.expression) for q in monotone_quantifiers])

print("Monotone     cost: {0}, complexity: {1}".format(np.average(monotone_cost),np.average(monotone_complexity)))
print("Non monotone cost: {0}, compleixty: {1}".format(np.average(non_monotone_cost),np.average(non_monotone_complexity)))
