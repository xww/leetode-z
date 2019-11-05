# -*- coding=utf-8 -*-
# author=zyq
import time, os
import problem_detail
import copy


class Template_mixin(object):
    """html报告"""
    HTML_TMPL = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Leetcode分类统计</title>
            <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
            <h1 style="font-family: Microsoft YaHei">Leetcode分类统计</h1>
            
            <style type="text/css" media="screen">
        body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
        </style>
        </head>
        
        <body>
          <h2>
            <a href="#divpinlv">按频率分类</a>
            <a href="#divgongsi">按公司分类</a>
          </h2>
          
            <div id='divpinlv'>
              <table id='result_table' class="table table-condensed table-bordered table-hover">
                <colgroup>
                    <col align='left' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
                    <th>题号</th>
                    <th>题目</th>
                    <th>URL</th>
                    <th>难度</th>
                    <th>出现次数</th>
                </tr>
                %(table_bypinlv)s
            </table>
            </div>
            
        <div id='divgongsi'>            
            <!--
            <h2><a href="#bytedance">bytedance</a></h2>
            <h2><a href="#bytedance2">bytedance2</a></h2>
            -->
            %(index_str)s
            
            %(all_coms)s            
            
            
            
        </div>

        </body>
        </html>"""

    TABLE_TMPL = """
        <tr class='failClass warning'>
            <td>%(id)s</td>
            <td>%(title)s</td>
            <td><a href="%(url_href)s">%(url)s</a></td>
            <td>%(level)s</td>
            <td>%(counts)s</td>
        </tr>"""
    ONE_COM_TPL = """
    <div id='div%(divid)s'>
            <h2>%(com_name)s</h2>
            <table id='result_table2' class="table table-condensed table-bordered table-hover">
                <colgroup>
                    <col align='left' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row2' class="text-center success" style="font-weight: bold;font-size: 14px;">
                    <th>题号</th>
                    <th>题目</th>
                    <th>URL</th>
                    <th>难度</th>
                    <th>出现次数</th>
                </tr>
                %(one_com_table)s
            </table>
            </div> 
    """


if __name__ == '__main__':
    table_pinlv = ''

    html = Template_mixin()

    leetccodestatics = problem_detail.LeetCodeStatics()
    leetccodestatics.file2probles_detail()
    problems = leetccodestatics.problems_detail
    sorted_problems = sorted(problems, cmp=problem_detail.problem_cmp)
    for p in sorted_problems:
        # print p.total_counts, p.url

        table_td = html.TABLE_TMPL % dict(id=p.id, title=p.title, url_href=p.url,
                                          url=p.url, level=p.level, counts=p.total_counts, )

        table_pinlv += table_td

    # 按公司
    """
    <h2><a href="#bytedance">bytedance</a></h2>
            <h2><a href="#bytedance2">bytedance2</a></h2>
    """
    leetccodestatics.gen_coms_detail()
    coms_detail = leetccodestatics.coms_detail.values()
    coms_detail = sorted(coms_detail, cmp=problem_detail.com_cmp)
    title_href = ''
    all_coms_str = ''

    for i in range(len(coms_detail)):
        print coms_detail[i].com_name, coms_detail[i].total_counts
        one_com_table = ''
        # name_len = len(coms_detail[i].com_name + ':' + str(coms_detail[i].total_counts))
        # need_nbsp_count = 30 - name_len
        # one_title = '<a href="#div' + str(i + 1) + '">' + coms_detail[i].com_name + ':' + str(
        #     coms_detail[i].total_counts) + '&nbsp;' * need_nbsp_count + '</a>'
        one_title = '<h2><a href="#div' + str(i + 1) + '">' + coms_detail[i].com_name + ':' + str(
            coms_detail[i].total_counts) + '</a></h2>'
        title_href += one_title
        temp_problems = copy.deepcopy(coms_detail[i].problems)
        temp_problems = sorted(temp_problems, cmp=problem_detail.owner_com_counts_cmp)
        for p in temp_problems:
            table_td = html.TABLE_TMPL % dict(id=p.id, title=p.title, url_href=p.url,
                                              url=p.url, level=p.level, counts=p.owner_com_counts, )
            one_com_table += table_td
        one_com_str = html.ONE_COM_TPL % dict(divid=str(i + 1), com_name=coms_detail[i].com_name,
                                              one_com_table=one_com_table)
        all_coms_str += one_com_str

    output = html.HTML_TMPL % dict(table_bypinlv=table_pinlv,
                                   index_str=title_href,
                                   all_coms=all_coms_str)

    # filename = '{date}_TestReport.html'.format(date=time.strftime(
    # '%Y%m%d%H%M%S'))
    filename = 'aa.html'

    # dir = os.path.join(
    #     os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report')
    # filename = os.path.join(dir, filename)

    with open(filename, 'wb') as f:
        f.write(output)
