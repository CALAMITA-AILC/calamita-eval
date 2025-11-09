import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calamita_recalc import CalamitaTask
import os
import yaml
import importlib
import json


def import_function(loader, node):
    function_name = loader.construct_scalar(node)
    yaml_path = os.path.dirname(loader.name)

    *module_name, function_name = function_name.split(".")
    if isinstance(module_name, list):
        module_name = ".".join(module_name)
    module_path = os.path.normpath(os.path.join(yaml_path, "{}.py".format(module_name)))

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function = getattr(module, function_name)
    return function


def load_yaml_config(yaml_path=None, yaml_config=None, yaml_dir=None, mode="full"):
    if mode == "simple":
        constructor_fn = ignore_constructor
    elif mode == "full":
        constructor_fn = import_function

    yaml.add_constructor("!function", constructor_fn)
    if yaml_config is None:
        with open(yaml_path, "rb") as file:
            yaml_config = yaml.full_load(file)

    if yaml_dir is None:
        yaml_dir = os.path.dirname(yaml_path)

    assert yaml_dir is not None

    if "include" in yaml_config:
        include_path = yaml_config["include"]
        del yaml_config["include"]

        if isinstance(include_path, str):
            include_path = [include_path]

        include_path.reverse()
        final_yaml_config = {}
        for path in include_path:
            if not os.path.isfile(path):
                path = os.path.join(yaml_dir, path)

            try:
                included_yaml_config = load_yaml_config(yaml_path=path, mode=mode)
                final_yaml_config.update(included_yaml_config)
            except Exception as ex:
                raise ex

        final_yaml_config.update(yaml_config)
        return final_yaml_config
    return yaml_config


def load_samples(path):
    data = []
    with open(path, "r") as f:
        for row in f:
            data.append(json.loads(row))
    return data, len(data)


def prepare_sample(sample):
    try:
        return [sample['target'], sample['resps'][0][0]]
    except Exception as e:
        print(e)
        return [sample['target'], '[]']


class DimmiTask(CalamitaTask):
    def evaluate(self, subtask, samples_path):
        yaml_path = f"tasks/dimmi/dimmi_{subtask}.yaml"
        
        config = load_yaml_config(yaml_path=yaml_path)
        samples, num_samples = load_samples(samples_path)
        
        metric_function = config['metric_list'][0]['metric']
        
        tot = 0
        for sample in samples:
            tot += metric_function(prepare_sample(sample))
        
        return {'mean': tot / num_samples}
