'''
Created on Nov 18, 2013

@author: Anduril
'''
from ChorusCore.MyTestCase import MyTestCase
from ChorusCore import TestScope, Utils

class TestSuite1_Pass(MyTestCase):
    '''TestSuite name must equal to the filename'''
    @classmethod
    def setUpClass(cls):
        '''Add prepare scripts before all cases'''
        cls.picture1 = open(Utils.get_filestr(["TestData"], "test_photo.png"),"r")
        cls.picdata1 = cls.picture1.read()
        cls.picture2 = open(Utils.get_filestr(["TestData"], "test_photo1.png"),"r")
        cls.picdata2 = cls.picture2.read()
        super(TestSuite1_Pass,cls).setUpClass()
        
    def setUp(self):  
        '''scripts before each cases'''
        MyTestCase.setUp(self)   
        
    def tearDown(self):
        '''scripts after each cases'''
        MyTestCase.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        '''Add en scripts after all cases'''
        super(TestSuite1_Pass,cls).tearDownClass()
        
    @TestScope.setscope(TestScope.Scope.Sanity,TestScope.Scope.Regression)
    def testC01_pass(self):
        '''Each test case must start with a "test" label'''
        self.assertImageData("A01_Compare_Photo_With_Baseline", self.picdata1, image_logic=100, imagetype="png")
        self.assertData("A01_Compare_Data_With_Baseline", {"data":"I like chorus"})
        self.assertBool("A01_Compare_Bool", True)
        self.assertTrue(True, "Break_Message_for_unitteset_assertTrue")
        self.assertEqual("A01_data","A01_data","Break_Message_for_unittest_assertEqual")
        
    @TestScope.setscope(TestScope.Scope.Regression)
    def testC02_fail(self):
        self.assertImageData("A01_Compare_Photo_With_Baseline", self.picdata2, image_logic=100, imagetype="png")
        self.assertData("A01_Compare_Data_With_Baseline", {"data":"I don't like chorus"})
        self.assertBool("A01_Compare_Bool", False)
        #self.assertTrue(False, "Break_Message_for_unitteset_assertTrue")
        self.assertEqual("A01_data","A02_data","Break_Message_for_unittest_assertEqual")
        
    def testC03_crash(self):
        self.assertBool("A01_Compare_Bool", True)
        abc
    
    @TestScope.setscope(TestScope.Scope.Regression)
    def testC04_crash(self):
        self.assertBool("A01_Compare_Bool", True)
        abc