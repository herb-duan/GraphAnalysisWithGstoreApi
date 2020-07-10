import requests
import urllib3
import json
import networkx as nx
import matplotlib.pyplot as plt

hold = "<http://localhost:2020/vocab/resource/holder_copy_holder_name>"
perfix = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/"

def generateSparql2(sorce = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>",
                   level = 3):
    select_name = " "
    where_sectence = " "
    for i in range(level):
        select_name +=  "?"+str(i+1)+"hop " 
        if i == 0:
            where_sectence += sorce
        else:
            where_sectence += "?"+str(i)+"hop"
        where_sectence += hold
        where_sectence += "?"+str(i+1)+"hop. "


    sparql = "\
            select "+ select_name +"\
            where { "+ where_sectence +"}\
            "
    print("****** 生成的 sparql 语句为：")
    print(sparql)
    return sparql

def output2(json_result,sorceCompany,level):
    list_bindings = json_result['data']['results']['bindings']
    # print(list_bindings)
    result_len = len(list_bindings)
    edge_list = []
    if result_len == 0:# 没有路径
        print("没有 " + sorceCompany+ " 开始的路径")
        return
    
    list_out = []
    list_all = []
    for i in range(result_len):# 对每条结果遍历
        tmp_out =[]
        for j in range(level): # 对结果中的每一跳遍历
            tmp_out.append(list_bindings[i][str(j+1)+"hop"]['value'][len(perfix)-1:])
            list_all.append( list_bindings[i][str(j+1)+"hop"]['value'][len(perfix)-1:])
        list_out.append(tmp_out)
    set_all = set(list_all)
    list_out.sort()
    print("****** " + sorceCompany+ " 的"+ str(level) +"层内持股公司有 "+str(len(set_all) )+" 个:")
    print(set_all)
    print("****** " + sorceCompany+ " 的"+ str(level) +"层持股公司的路径有 "+str(result_len)+" 个:")
    for i in range(result_len):
        out = sorceCompany
        last = sorceCompany
        for j in range(level):
            out += " --> " + list_out[i][j]
            now = list_out[i][j]
            edge_list.append((last,now))
            last = now
        print(out)
    DG = nx.DiGraph()
    DG.add_edges_from(edge_list)
    nx.draw(DG, pos = nx.circular_layout(DG), with_labels=True, font_size=5)
    plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签 
    plt.rcParams['axes.unicode_minus']=False
    plt.show()


def query2():
    # input
    f = open('./company.txt',encoding='UTF-8')
    company_set =set( f.readlines()[0].split() )
    print("请输入持股公司名称：（例：招商局轮船股份有限公司）")
    sorceCompany = input()
    while sorceCompany not in company_set:
        print("输入公司名有误，请重新输入持股公司名称：（例：招商局轮船股份有限公司）")
        sorceCompany = input()
    sorce = perfix + sorceCompany + ">"
    print("请输入查询层数(>0)：（例：3）")
    level =int( input())
    # generate sparql
    sparql = generateSparql2(sorce, level)
    #prepare post url and data
    url = "https://gstore.cstcloud.cn/api"
    postData  = {
        "action": "queryDB",
        "accesskeyid": "698fd8bec15d47e9ae0b8ed72bce3b1a",
        "access_secret": "2CB8B6E50E05A24D5C0124E44EFF607B",
        "dbName": "jinrong",
        "sparql": sparql
    }
    # post
    response = requests.post(url = url, data = postData, verify=False)
    # output
    json_result = json.loads(response.text)
    if 'msg' in json_result and json_result['msg'] == 'ok' and 'success' in json_result and json_result['success'] == 1:
        print("**********从数据库获取信息成功**********")
    else:
        print("**********从数据库获取信息失败**********")
        print(json_result['msg'])
        return
    #print(json_result)
    print("\n")
    output2(json_result,sorceCompany,level)
    

if __name__ =='__main__':
    urllib3.disable_warnings()
    query2()

