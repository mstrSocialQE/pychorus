'''
Created on Jan 19, 2014

@author: Anduril
@target: provide a basic class for user to parse config file
'''
import Utils
import ChorusGlobals
from LogServer import LogServer,Level, LogType, Formatter
from ChorusConstants import CommonConstants

class ProjectConfiguration:
    '''Load options, own all project step functions'''
    
    def __init__(self, options):
        '''Provide initial full steps, input options contains basic parameters'''
        self.options=options
        self.set_output_folder()
        self.set_logserver()
        self.set_configfile()
    
    def set_output_folder(self):
        '''Set output folder
           Input: options.outputpath
           Output: self.outputdir, ChorusGlobals.outputdir'''
        self.outputdir = Utils.create_folder(self.options.outputpath, "Output", True)
        ChorusGlobals.set_outputdir(self.outputdir)
        print "Set output directory to %s" % self.outputdir
        
    def set_configfile(self):
        configfile = ConfigFile(self.options.configfile,self.options.configpath)
        configfile.get_env(self.options.env)
        self.parameters = configfile.parameters
        self.config = configfile.config
        ChorusGlobals.set_parameters(self.parameters)
        ChorusGlobals.set_configinfo(self.config)

    def set_logserver(self, name = LogType.ChorusCore, level=Level.debug,
                formatter=Formatter.Console):
        self.logserver=LogServer(name, level, formatter, colorconsole = self.options.color)
        ChorusGlobals.set_logserver(self.logserver)
        ChorusGlobals.set_logger(self.logserver.get_logger())
        
#     def close_logserver(self):
#         self.logserver.close_logger()

class ConfigFile:
    '''Read Config file'''
    parameters={}
    def __init__(self, config_filename, config_filepath=None):
        self.CONFIG_KEY = CommonConstants.CONFIG_KEY
        self.logger = ChorusGlobals.get_logger()
        if config_filepath=="":
            config_filepath = "Config"
        else:
            config_filepath = "/".join("Config","config_file_path")
        self.cfg=Utils.read_config(config_filename, config_filepath)
        try:
            self.get_config()
            self.get_parameters()
        except Exception,e:
            self.logger.critical("Cannot get suite information from config file %s with error: %s" % (config_filename,str(e)))
            raise Exception("Cannot get suite information from config file %s with error: %s" % (config_filename,str(e)))
        
    def get_config(self):
        section = self.CONFIG_KEY
        tmpdict = {}
        for option in self.cfg.options(section):
            tmpdict[option] = self.cfg.get(section, option)
        self.config = tmpdict
    
    def get_env(self, env = None):
        if env:
            new_env = env
        elif self.config.has_key(CommonConstants.ENV_KEY) and self.config[CommonConstants.ENV_KEY]!=self.CONFIG_KEY:
            new_env = self.config[CommonConstants.ENV_KEY]
        else:
            new_env = None
            self.logger.info("Load Default section as environment")
        if new_env:
            if self.parameters.has_key(new_env):
                for key in self.parameters[new_env]:
                    self.config[key]=self.parameters[new_env][key]
                self.logger.info("Load %s section as environment" % new_env)
            else:
                self.logger.warning("Cannot load %s section, will use Default instead" % new_env)     
    
    def get_parameters(self):
        for section in self.cfg.sections():
            if section!=self.CONFIG_KEY:
                tmpdict = {}
                for option in self.cfg.options(section):
                    tmpdict[option] = self.cfg.get(section, option)
                self.parameters[section] = tmpdict