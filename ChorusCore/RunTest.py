#!/Users/mxu/Documents/py_env/bin/python
'''
Created on Dec 28, 2013

@author: Anduril
'''
import sys,os
import optparse
from ProjectConfiguration import ProjectConfiguration
from ProjectExecution import RunTest
from LogServer import Level
class MyProject(ProjectConfiguration):
    '''default initialization, can be reloaded'''
#     def __init__(self,options):
#         ProjectConfiguration.__init__(self, options)
    
    def __init__(self,options):
        self.options=options
        self.set_output_folder()
        self.set_logserver(level=Level.debug)
        self.logserver.add_filehandler(level=Level.error,
                                       filepath=self.outputdir,filename="error.log")
        self.logserver.add_filehandler(level=Level.info,
                                       filepath=self.outputdir,filename="info.log")
        self.set_configfile()
        
    def start_test(self): 
        RunTest()

def main(argv=sys.argv):
    current_dir_abs = os.getcwd()
    sys.path.append(current_dir_abs)
    
    parser = optparse.OptionParser()
    parser.add_option("-c","--config",dest="configfile",
                      default="default.cfg",
                      help="config file name, e.g: test.cfg")
    parser.add_option("-p","--path",dest="configpath",
                      default="",
                      help="config file path, default: Config/, e.g. test")
    parser.add_option("-o","--output",dest="outputpath",
                      default="",
                      help="output file path, default: Output/, e.g: Output")
    parser.add_option("--color",dest="color",
                      default=False, action="store_true",
                      help="provide a colorful console with different log level")
    parser.add_option("-e","--env",dest="env",
                      default=None, 
                      help="choose environment to run the test in config file")
    options, argv = parser.parse_args(list(argv))
    init=MyProject(options)
    init.start_test()
    