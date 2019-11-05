# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Collection(object):
    def __init__(self):
        self.bower = webdriver.Chrome()
        self.problems_detail = []

    def collect(self):
        self.bower.get('https://leetcode-cn.com/accounts/login/')

        time.sleep(2)
        self.bower.find_element_by_name('login').send_keys('xiongwenwu1997@126.com')
        time.sleep(1)
        self.bower.find_element_by_name('password').send_keys('xxxx')
        time.sleep(1)
        self.bower.find_element(By.XPATH, '//button[1]').click()
        time.sleep(1)

        self.bower.get('https://leetcode-cn.com/problemset/algorithms/')
        time.sleep(2)

        show_num_select = self.bower.find_elements_by_xpath("//tbody[2]")[0]
        show_num_select.find_element_by_xpath("//option[@value='9007199254740991']").click()
        # select.find_element_by_xpath("//option[@value='20']").click()

        time.sleep(1)

        # bower.get('https://leetcode-cn.com/problems/two-sum/')
        # time.sleep(2)

        # # 难度
        # print bower.find_elements_by_xpath(".//span[@class='css-14oznsj-Difficulty e5i1odf5']")[1].get_attribute(
        #     'data-degree')
        # # 分类tag
        # tags = bower.find_elements_by_class_name('topic-tag__1z4-')
        # tagname = tags[0].get_attribute("innerText")
        # print tagname
        #
        # compnay = bower.find_elements_by_class_name('company-tag-wrapper__1DTg')
        # compnies = compnay[0].find_elements_by_class_name('company-tag__2trG')
        # print len(compnies)
        # # google = compnies[0].get_attribute('href')
        # aws = compnies[0]
        # a = aws.find_element_by_tag_name('div')
        # print a.get_attribute("innerHTML")
        problems_body = self.bower.find_elements_by_xpath("//tbody[1]")[0]
        problems = problems_body.find_elements_by_xpath('//tr')
        print len(problems)
        for problem in problems[0:500]:
            self.get_problem_detail(problem)
        for problem_detail in self.problems_detail:
            self.get_problem_coms(problem_detail)
        # for problem_detail in self.problems_detail:
        #    print ','.join(problem_detail)

        # 测试时间选择 半年内 一年内 一到两年
        # bower.get('https://leetcode-cn.com/problems/flower-planting-with-no-adjacent/')
        # time.sleep(1)
        # times = bower.find_elements_by_class_name('time-period-button-group__2vI1')[0]
        # disables = times.find_elements_by_tag_name('button')
        # disable0 = disables[0].get_attribute('disabled')
        # disable1 = disables[1].get_attribute('disabled')
        # disable2 = disables[2].get_attribute('disabled')  #
        # print disable0 == 'true', disable1 == True, disable2 is None
        # # True False True

    def get_problem_detail(self, problem):
        try:
            tds = problem.find_elements_by_tag_name('td')
            if len(tds) != 7:
                return
            id = tds[1].get_attribute("innerText")
            # en_name = tds[2].get_attribute('value')
            cn_name = tds[2].find_element_by_xpath('.//div[1]//a').get_attribute("innerText")
            problem_url = tds[2].find_element_by_xpath('.//div[1]//a').get_attribute('href')
            degree = tds[5].find_element_by_xpath('.//span').get_attribute("innerText")
            self.problems_detail.append([id, cn_name, problem_url, degree])
            print id, cn_name, problem_url, degree
        except Exception as e:
            print e.message

    def get_problem_coms(self, problem_detail):
        try:
            self.bower.get(problem_detail[2])
            time.sleep(2)

            coms_static = {}
            time_periods = self.bower.find_elements_by_class_name('time-period-button-group__2vI1')[
                0].find_elements_by_tag_name('button')
            # 先展开公司 否则无法直接点击加载更多
            self.bower.find_element_by_class_name('header__1If0').click()
            time.sleep(1)

            for time_period in time_periods:
                if time_period.get_attribute('disabled') == 'true':
                    continue
                try:
                    time_period.click()
                    time.sleep(1)
                except Exception as e:
                    # 半年内这个标签是默认选中的，貌似click会报错
                    print e.message

                try:
                    # 加载更多,可能没有这个选项，所以会有异常
                    load_more = self.bower.find_element_by_class_name('load-more__2Cip')

                    load_more.find_element_by_tag_name('div').click()
                    time.sleep(1)
                except Exception:
                    pass

                coms = self.bower.find_elements_by_class_name('company-tag-wrapper__1DTg')[0]. \
                    find_elements_by_class_name('company-tag__2trG')

                for com in coms:
                    com_name_and_counts = com.find_element_by_tag_name('div').get_attribute("innerText").split('\n')
                    count = 0
                    try:
                        count = int(com_name_and_counts[2])
                    except Exception:
                        count = 1
                    if coms_static.get(com_name_and_counts[0]):
                        coms_static[com_name_and_counts[0]] = coms_static[com_name_and_counts[0]] + count
                    else:
                        coms_static[com_name_and_counts[0]] = count

            for com in coms_static:
                com_count_str = com + ':' + str(coms_static[com])
                problem_detail.append(com_count_str)
            print ','.join(problem_detail)

        except Exception as e:
            print e.message


if __name__ == '__main__':
    Collection().collect()
