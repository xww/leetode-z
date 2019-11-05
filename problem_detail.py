# -*- coding:utf-8 -*-
import copy
class ProblemDetail(object):
    def __init__(self):
        self.id = 0
        self.title = None
        self.url = None
        self.level = None
        self.coms = {}
        self.total_counts = 0

        self.owner_com_name = None
        self.owner_com_counts = 0

    def __str__(self):
        return str(self.id) + ',' + self.title + ',' + self.owner_com_name + ',' + str(self.owner_com_counts)


def problem_cmp(x, y):
    if x.total_counts > y.total_counts:
        return -1
    if x.total_counts < y.total_counts:
        return 1
    return 0


def owner_com_counts_cmp(x, y):
    if x.owner_com_counts > y.owner_com_counts:
        return -1
    if x.owner_com_counts < y.owner_com_counts:
        return 1
    return 0


class ComDetail(object):
    def __init__(self):
        self.com_name = None
        self.problems = []
        self.total_counts = 0


def com_cmp(x, y):
    if x.total_counts > y.total_counts:
        return -1
    if x.total_counts < y.total_counts:
        return 1
    return 0


class LeetCodeStatics(object):
    def __init__(self):
        self.probles_detail = []
        self.coms_detail = {}
        self.name_map = {'字节跳动': '今日头条'}

    def file2probles_detail(self):
        f = open('aa.txt', 'r')
        for line in f.readlines():

            temp = line[:-1].split(',')
            if int(temp[0]) == 50:
                temp[1] += temp[2]
                temp.remove(temp[2])

            problem_detail = ProblemDetail()
            problem_detail.id = temp[0]
            problem_detail.title = temp[1]
            problem_detail.url = temp[2]
            problem_detail.level = temp[3]

            for i in range(4, len(temp)):
                com_name = temp[i].split(':')[0]
                real_name = com_name
                if com_name in self.name_map:
                    real_name = self.name_map[com_name]
                com_counts = temp[i].split(':')[1]
                problem_detail.total_counts += int(com_counts)
                if com_name in problem_detail.coms:
                    problem_detail.coms[real_name] = problem_detail.coms[real_name] + int(com_counts)
                else:
                    problem_detail.coms[real_name] = int(com_counts)
            self.probles_detail.append(problem_detail)

    def gen_coms_detail(self):
        for problem_detail in self.probles_detail:
            for com_name in problem_detail.coms.keys():
                temp_problem = copy.deepcopy(problem_detail)
                temp_problem.owner_com_name = com_name
                temp_problem.owner_com_counts = temp_problem.coms[com_name]
                if com_name in self.coms_detail:
                    self.coms_detail[com_name].problems.append(temp_problem)
                    self.coms_detail[com_name].total_counts += temp_problem.coms[com_name]
                else:
                    com_detail = ComDetail()
                    com_detail.com_name = com_name
                    com_detail.problems.append(temp_problem)
                    com_detail.total_counts = temp_problem.coms[com_name]
                    self.coms_detail[com_name] = com_detail


if __name__ == '__main__':
    leetccodestatics = LeetCodeStatics()
    leetccodestatics.file2probles_detail()

    # coms_name = set()
    # for problem_detail in leetccodestatics.probles_detail:
    #     for com_name in problem_detail.coms.keys():
    #         coms_name.add(com_name)
    # for name in list(coms_name):
    #     print name

    # problems = leetccodestatics.probles_detail
    # sorted_problems = sorted(problems, cmp=problem_cmp)
    # for p in sorted_problems:
    #     print p.total_counts, p.url

    leetccodestatics.gen_coms_detail()
    coms_detail = leetccodestatics.coms_detail.values()
    coms_detail = sorted(coms_detail, cmp=com_cmp)
    for com in coms_detail:
        com.problems = sorted(com.problems, cmp=owner_com_counts_cmp)
        print com.com_name, com.total_counts
        for p in com.problems:
            print p
