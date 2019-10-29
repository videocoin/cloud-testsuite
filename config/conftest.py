from logging import config
import yaml

with open("./config/log_spec.yaml", "r") as log_spec_file:
    config.dictConfig(yaml.load(log_spec_file, Loader=yaml.FullLoader))

