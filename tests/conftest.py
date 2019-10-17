from logging import config
import yaml

with open("log_spec.yaml", "r") as log_spec_file:
    config.dictConfig(yaml.load(log_spec_file, Loader=yaml.FullLoader))

import logging
def pytest_tavern_beta_before_every_test_run(test_dict, variables):
    # logging.info("Starting test %s", test_dict["test_name"])
    
    # variables["extra_var"] = "abc123"
    logging.info(test_dict.keys())
    logging.info(variables.keys())
