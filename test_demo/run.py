#导入包
import unittest
import test_math_suite
with open('test.txt','w+') as file:
    runner = unittest.TextTestRunner(file,'test',2)
    runner.run(test_math_suite.suite)