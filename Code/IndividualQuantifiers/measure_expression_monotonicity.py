from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Monotonicity import MonotonicityMeasurer

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

meanings = file_util.load_dill('meanings.dill')

universe = Generator.generate_simplified_models(args.model_size)

measurer_a_up = MonotonicityMeasurer(universe,args.model_size,'A')
measurer_b_up = MonotonicityMeasurer(universe,args.model_size,'B')
measurer_a_down = MonotonicityMeasurer(universe,args.model_size,'A',down=True)
measurer_b_down = MonotonicityMeasurer(universe,args.model_size,'B',down=True)

with ProcessPool(nodes=args.processes) as process_pool:
    monotonicities_a_up = process_pool.map(measurer_a_up, meanings)
    monotonicities_b_up = process_pool.map(measurer_b_up, meanings)
    monotonicities_a_down = process_pool.map(measurer_a_down, meanings)
    monotonicities_b_down = process_pool.map(measurer_b_down, meanings)
    monotonicities_a_max = process_pool.map(max,
                                          monotonicities_a_up, monotonicities_a_down)
    monotonicities_b_max = process_pool.map(max,
                                            monotonicities_b_up,monotonicities_b_down)
    monotonicities_max = process_pool.map(lambda x, y: (x+y)/2, monotonicities_a_max,
                                          monotonicities_b_max)

file_util.dump_dill(monotonicities_a_up,'monotonicities_a_up.dill')
file_util.dump_dill(monotonicities_a_down,'monotonicities_a_down.dill')
file_util.dump_dill(monotonicities_b_up,'monotonicities_b_up.dill')
file_util.dump_dill(monotonicities_b_down,'monotonicities_b_down.dill')
file_util.dump_dill(monotonicities_max,'monotonicities_max.dill')
