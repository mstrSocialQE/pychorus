#!/Users/mxu/Documents/py_env/bin/python
'''
Created on Dec 28, 2013

@author: Anduril
'''
import sys
#import os
#import optparse
#from ProjectConfiguration import ProjectConfiguration
#from ProjectExecution import RunTest
#from LogServer import Level
#class MyProject(ProjectConfiguration):
#    '''default initialization, can be reloaded'''
##     def __init__(self,options):
##         ProjectConfiguration.__init__(self, options)
#    
#    def __init__(self,options):
#        self.options=options
#        self.set_output_folder()
#        self.set_logserver(level=Level.debug)
#        self.logserver.add_filehandler(level=Level.error,
#                                       filepath=self.outputdir,filename="error.log")
#        self.logserver.add_filehandler(level=Level.info,
#                                       filepath=self.outputdir,filename="info.log")
#        self.set_configfile()
#        
#    def start_test(self): 
#        RunTest()

from ChorusCore import RunTest
RunTest.main(sys.argv)