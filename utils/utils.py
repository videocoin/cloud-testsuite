import yaml

def load_yaml(file):
    with open('./consts/common.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    return data_loaded
