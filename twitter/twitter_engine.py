from configparser import ConfigParser

config = ConfigParser()

config.read('../config/main_config.ini')

print('SECTIONS ', config.sections())
print('TWITTER', config['twitter'].keys())
