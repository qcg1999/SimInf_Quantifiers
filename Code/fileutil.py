import os
from copy import copy

import dill


class FileUtil(object):

    def __init__(self, folderName):
        os.makedirs(folderName, exist_ok=True)
        self.folderName = folderName

    def dump_dill(self, data, filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'wb') as file:
            dill.dump(data, file)

    def load_dill(self,filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'rb') as file:
            return dill.load(file)

    def save_stringlist(self, data, filename):
        with open('{0}/{1}'.format(self.folderName, filename), 'w') as file:
            for item in data:
                file.write('{0}\n'.format(item))

    def full_path(self, filename):
        return '{0}/{1}'.format(self.folderName, filename)

    def save_figure(self, fig, filename):
        os.makedirs(self.full_path('figures'), exist_ok=True)
        fig.savefig(self.full_path('figures/{0}'.format(filename)), bbox_inches='tight')

    def get_base_file_util(self):
        file_util_base = copy(self)
        file_util_base.folderName = os.path.dirname(self.folderName)
        return file_util_base

def base_dir(dest_dir, setup_name, max_quant_length, model_size):
    return "{0}/{1}_length={2}_size={3}".format(dest_dir, setup_name, max_quant_length,model_size)


def run_dir(dest_dir, setup_name, max_quant_length, model_size, run_name):
    return "{0}/{1}".format(base_dir(dest_dir, setup_name, max_quant_length, model_size), run_name)
