import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
# 使用Chrome浏览器驱动程序
service = Service(executable_path=r"D:\学术交流论坛\.venv\Scripts\msedgedriver.exe")
driver=webdriver.Edge(service=service)

#智能等待
#driver.implicitly_wait(5)

# 打开网页
#driver.get("http://www.baidu.com")
driver.get("http://www.csdn.net")
# 获取网页标题并输出
#print("Page title is:", driver.title)

driver.find_element(By.LINK_TEXT,'Python').click()

#通过ID查找元素并输入用户名和密码
#driver.find_element(By.ID,"username").send_keys("1234567879")
#driver.find_element(By.ID,"password").send_keys("123456")

#调整窗口大小
#driver.maximize_window()
#driver.minimize_window()
#driver.set_window_size(300, 500)`

#点击登录按钮
#driver.find_element(By.NAME,"login").click()

time.sleep(5)

#前进或后退一页
driver.back()

driver.quit()

