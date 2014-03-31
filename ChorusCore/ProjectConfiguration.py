'''
Created on Jan 19, 2014

@author: Anduril
@target: provide a basic class for user to parse config file
'''
import os, sys, optparse
import Utils
import ChorusGlobals
from LogServer import LogServer,Level, LogType, Formatter
from ChorusConstants import CommonConstants

class ProjectConfiguration:
    '''Load options, own all project step functions'''
    def init_options(self):
        self.parser = optparse.OptionParser()
        self.parser.add_option("-c","--config",dest="configfile",
                               default="default.cfg",
                               help="config file name, e.g: test.cfg")
        self.parser.add_option("-p","--path",dest="configpath",
                               default="",
                               help="config file path, default: Config/, e.g. test")
        self.parser.add_option("-o","--output",dest="outputpath",
                               default="",
                               help="output file path, default: Output/, e.g: Output")
        self.parser.add_option("--color",dest="color",
                               default=False, action="store_true",
                               help="provide a colorful console with different log level")
        self.parser.add_option("-e","--env",dest="env",
                               default=None, 
                               help="choose environment to run the test in config file")
    
    def setup(self, argv=[]):
        if not hasattr(self,"parser"):
            self.init_options()
        self.options, argv = self.parser.parse_args(list(argv))
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
            config_filepath = os.path.sep.join("Config","config_file_path")
        config_paths = config_filepath.split(os.path.sep)
        self.config_filepath = Utils.get_filestr(config_paths, config_filename)
        self.cfg=Utils.read_config(self.config_filepath)
        try:
            self.get_config()
            self.get_parameters()
        except Exception,e:
            self.logger.critical("Cannot get suite information from config file %s with error: %s:%s" % (config_filename,str(Exception),str(e)))
            raise Exception("Cannot get suite information from config file %s with error: %s:%s" % (config_filename,str(Exception),str(e)))
    
    def write_config(self):
        with open(self.config_filepath, 'wb') as config_file:
            self.cfg.write(config_file)
    
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