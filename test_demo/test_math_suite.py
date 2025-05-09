import unittest
#from test_math_method import TestMathMethod
import test_math_method

#引入测试套件
suite = unittest.TestSuite()

#引入批量执行测试用例
loader = unittest.TestLoader()

#增加一条测试用例，(测试类名(测试方法名))
#suite.addTest(TestMathMethod('test_two_negative'))

#suite.addTests(loader.loadTestsFromTestCase(TestMathMethod))

suite.addTests(loader.loadTestsFromModule(test_math_method))