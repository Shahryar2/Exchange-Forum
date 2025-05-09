#导入包
import unittest
from test import MathMethod

#测试用例书写
class TestMathMethod(unittest.TestCase):
    def test_two_positive0(self):
        result=MathMethod(1,2).add()  #test two positive add
        self.assertEqual(result,3)

    def test_two_negative0(self):
        result=MathMethod(-1,-2).add()
        self.assertEqual(result,-3)

    def test_positive_negative0(self):
        result=MathMethod(1,-2).add()
        self.assertEqual(result,-1)

    def test_positive_zero0(self):
        result=MathMethod(1,0).add()
        self.assertEqual(result,1)

    def test_negative_zero0(self):
        result=MathMethod(-1,0).add()
        self.assertEqual(result,-1)

    def test_two_float0(self):
        MathMethod(0.1,0.2).add()

    def test_two_positive1(self):
        result=MathMethod(1,2).sub()
        self.assertEqual(result,-1)

    def test_two_negative1(self):
        result=MathMethod(-1,2).sub()
        self.assertEqual(result,-3)

    def test_positive_negative1(self):
        result=MathMethod(1,-2).sub()
        self.assertEqual(result,3)

    def test_positive_zero1(self):
        result=MathMethod(1,0).sub()
        self.assertEqual(result,1)

    def test_negative_zero1(self):
        result=MathMethod(-1,0).sub()
        self.assertEqual(result,-1)

    def test_two_float1(self):
        result=MathMethod(0.1,0.2).sub()
        self.assertEqual(result,-0.1)

#用来执行所有用例
if __name__ == '__main__':
    unittest.main()
