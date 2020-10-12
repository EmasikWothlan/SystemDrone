# config, about default behavior and writing default behavior
import os
import json
import random


class Config:
    def __init__(self, save_path=None, save_pattern=None, interval=None):
        self.save_path = save_path
        self.save_pattern = save_pattern
        self.interval_ = interval  # see interval() below.
        self.load_config()

    def write_config(self, config_filename=None):
        config_dict = {
            'save_path': self.save_path or '.',
            'save_pattern': self.save_pattern or '/- Artist - %A/',
            'interval_': self.interval_
        }
        config_filename = config_filename or os.path.join('..', 'drone_config.cfg')
        with open(config_filename, mode='w') as fd:
            json.dump(config_dict, fd)

    def load_config(self, config_filename=None):
        config_filename = config_filename or os.path.join('..', 'drone_config.cfg')
        if os.path.exists(config_filename):
            with open(config_filename) as fd:
                config_dict = json.load(fd)
        else:
            config_dict = dict()
        self.save_path = config_dict.get('save_path', False) or '.'
        self.save_pattern = config_dict.get('save_pattern', False) or '/- Artist - %A/'
        self.interval_ = config_dict.get('interval_', False) or 5

    # interval between two requests.
    def interval(self):
        if type(self.interval_) is tuple:
            return random.randint(self.interval_[0], self.interval_[-1])
        elif type(self.interval_) is int:
            return self.interval_
        else:
            return random.randint(4, 8)
