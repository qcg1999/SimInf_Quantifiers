import argparse
import itertools
from collections import namedtuple
from pathos.pools import ProcessPool

import dill

import ExperimentSetups
import Generator
from Languages.ComplexityMeasurer import WordCountComplexityMeasurer
from Languages.InformativenessMeasurer import InformativenessMeasurer
from Languages.LanguageGenerator import EvaluatedExpression, generate_all, generate_sampled
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('max_words', type=int)
parser.add_argument('--sample', type=int, default=None)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()

setup = ExperimentSetups.parse(args.setup)

file_util = FileUtil(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size)

expressions_by_meaning = file_util.load_dill('generated_expressions.dill')

expressions = [EvaluatedExpression(expression, meaning) for (meaning, expression) in expressions_by_meaning.items()]

if args.sample is None:
    languages = generate_all(expressions, args.max_words)
else:
    languages = generate_sampled(expressions, args.max_words, args.sample)

universe_size = len(Generator.generate_simplified_models(args.model_size))

# Possibly use this if memory becomes a problem.
# EvaluatedLanguage = namedtuple('EvaluatedLanguage', 'language complexity informativeness')
#
#
# def evaluate(language):
#     informativeness = measure_informativeness(language, universe_size)
#     complexity = measure_complexity_by_word_count(language, args.max_words)
#     return EvaluatedLanguage(language, complexity, informativeness)


pool = ProcessPool(nodes=args.processes)

informativeness = pool.map(InformativenessMeasurer(universe_size), languages)
complexity = pool.map(WordCountComplexityMeasurer(args.max_words), languages)

file_util.dump_dill(languages, 'languages.dill')
file_util.dump_dill(informativeness, 'informativeness.dill')
file_util.dump_dill(complexity, 'complexity.dill')

with open('{0}/languages.txt'.format(file_util.folderName), 'w') as f:
    for language in languages:
        f.write("{0}\n".format([str(e.expression) for e in language]))


