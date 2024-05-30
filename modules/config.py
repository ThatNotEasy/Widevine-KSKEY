import configparser

def load_configurations():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
