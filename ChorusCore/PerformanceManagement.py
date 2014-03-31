'''
Created on Mar 23, 2014

@author: Anduril
@target: provide Perofrmance result
'''
import Utils
import ChorusGlobals
from ChorusConstants import CommonConstants

class Performance_Object:
    def __init__(self, name, status, detail, time_taken):
        self.name = name
        self.status = status
        self.detail = detail
        self.time_taken = round(time_taken*1000)
        
class Performance_Result:
    data = []
    number = 0
    def add(self, name, status, detail, time_taken):
        self.data.append(Performance_Object(name, status, detail, time_taken))
        self.number += 1
    
    