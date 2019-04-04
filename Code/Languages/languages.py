import argparse
import ExperimentSetups
import fileutil
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
parser.add_argument('--run', default=0, type=int)

args = parser.parse_args()

setup = ExperimentSetups.parse(args.setup)

file_util = FileUtil(fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.run))

unevaluated_expressions = file_util.load_dill('expressions.dill')
meanings = file_util.load_dill('meanings.dill')
complexities = file_util.load_dill('expression_complexities.dill')

expressions = [EvaluatedExpression(expression, meaning, complexity)
               for (expression, meaning, complexity) in zip(unevaluated_expressions, meanings, complexities)]

if args.sample is None:
    languages = generate_all(expressions, args.max_words)
else:
    languages = generate_sampled(expressions, args.max_words, args.sample)

file_util.dump_dill(languages, 'languages.dill')
with open('{0}/languages.txt'.format(file_util.folderName), 'w') as f:
    for language in languages:
        f.write("{0}\n".format([str(e.expression) for e in language]))
