# This files runs following the cron patterns bellow
# CRON_TO_RUN_EVERY_1TH_MONTH = '0 0 1 1 *'
# CRON_TO_RUN_EVERY_4TH_MONTH = '0 0 1 4 *'
# CRON_TO_RUN_EVERY_7TH_MONTH = '0 0 1 7 *'
import time
import os
import pathlib
from utils import get_chromedriver_path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.path.join(pathlib.Path(__file__).parent.resolve(), 'data', 'downloaded')}
options.add_experimental_option("prefs",prefs)
# options.headless = True

driver = webdriver.Chrome(options=options, executable_path=get_chromedriver_path())
driver.get('http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm?codigo=8133')
time.sleep(2)
driver.find_element_by_id('onetrust-accept-btn-handler').click()
driver.implicitly_wait(10)
main = driver.find_elements_by_tag_name('app-companies-home')
print(main)
# button = driver.find_element_by_id('keyword')
# ActionChains(driver).move_to_element(button).send_keys('TESTE')

# company_input.send_keys("some text")
# search_company_input.clic()


driver.quit()
