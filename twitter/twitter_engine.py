

from configparser import ConfigParser

config = ConfigParser()


config.read('../config/main_config.ini')



print('==='*5)
print('SECTIONS ', config.sections())
print('STATUS ', config['accounts']['status'])
