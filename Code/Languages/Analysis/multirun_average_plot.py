from urllib.parse import quote_plus

import analysisutil
import matplotlib.pyplot as plt
import numpy as np

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')
analysisutil.add_argument('run_names', nargs='+')

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

fig = plt.figure()

for run_name in args.run_names:
    informativeness = file_util.load_dill('{0}/informativeness_{1}.dill'.format(run_name, args.informativeness_strategy))
    complexity = file_util.load_dill('{0}/complexity_{1}.dill'.format(run_name, args.complexity_strategy))
    plt.scatter(np.mean(informativeness), np.mean(complexity), label=run_name, s=160)

plt.legend()
plt.xlabel('informativeness')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_{2}_multirun_plot_average.png'.format(
    args.complexity_strategy,
    args.informativeness_strategy,
    '-'.join(args.run_names)
))