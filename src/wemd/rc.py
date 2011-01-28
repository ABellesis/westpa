# WEMD run control routines

import os
from wemd.util.config_dict import ConfigDict
from wemd.util.miscfn import logging_level_by_name

# Runtime config file management
ENV_RUNTIME_CONFIG  = 'WEMDRC'
RC_DEFAULT_FILENAME = 'wemd.cfg'

RC_SIM_STATE_KEY = 'data.state'
RC_SIM_CONFIG_KEY = 'data.sim_config'

def read_config(filename = None):
    if filename is None:
        filename = RC_DEFAULT_FILENAME
    
    cdict = ConfigDict()
    cdict.read_config_file(filename)
    
    return cdict

def load_sim_manager(runtime_config):
    from wemd.sim_manager import WESimManager
    return WESimManager(runtime_config)
        
# Logging management
LOGGING_DEFAULT_FORMAT = 'WEMD[%(proc_rank)4s] %(levelname)-8s -- %(message)s'
    
LOGGING_DEFAULT_SETTINGS = {'': {'level': 'WARNING',
                                 'format': LOGGING_DEFAULT_FORMAT},
                            'wemd': {'level': 'WARNING'},
                            'sqlalchemy.engine': {'level': 'ERROR'}
                            }
    
def configure_logging(runtime_config):
    import logging
    logkeys = set(k for k in runtime_config if k.startswith('logging.'))
    logger_settings = LOGGING_DEFAULT_SETTINGS.copy()
    for key in logkeys:
        item = key[8:]
        value = runtime_config[key]
        try:
            (logger_name, param) = item.rsplit('.', 1)
        except ValueError:
            continue
        else:
            if param not in ('level', 'format', 'handler'):
                continue
        if logger_name == 'root': 
            logger_name = ''
        try:
            logger_settings[logger_name][param] = value
        except KeyError:
            logger_settings[logger_name] = {param: value}
        
    for (logger_name, settings) in logger_settings.iteritems():
        level = logging_level_by_name(settings.get('level', 'NOTSET'))
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        try:
            format = settings['format']
        except KeyError:
            pass
        else:
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(format))
                logger.addHandler(handler)
            else:
                for handler in logger.handlers:
                    handler.setFormatter(logging.Formatter(format))
        

# Exit codes
EX_SUCCESS           = 0
EX_ERROR             = 1
EX_USAGE_ERROR       = 2
EX_ENVIRONMENT_ERROR = 3
EX_RTC_ERROR         = 4
EX_DB_ERROR          = 5
EX_STATE_ERROR       = 6
EX_CALC_ERROR        = 7
EX_COMM_ERROR        = 8
EX_DATA_ERROR        = 9
EX_EXCEPTION_ERROR   = 10

_ex_names = dict((code, name) for (name, code) in locals().iteritems()
                 if name.startswith('EX_'))

def get_exit_code_name(code):
    return _ex_names.get(code, 'error %d' % code)

__all__ = [name for name in dict(locals()) 
           if not name.startswith('_') 
           and name not in ('os',)]