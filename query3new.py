import requests
import urllib3
import json
import networkx as nx
import matplotlib.pyplot as plt

hold = "<http://localhost:2020/vocab/resource/holder_copy_holder_name>"
perfix = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/"

def generateSparql3new(sorce = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>",
                   level = 5):
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

def output3new(json_result,sorceCompany,level):
    list_bindings = json_result['data']['results']['bindings']
    # print(list_bindings)
    result_len = len(list_bindings)
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
    return set_all, list_out


def query3new():
    # input
    f = open('./company.txt',encoding='UTF-8')
    company_set =set( f.readlines()[0].split() )
    print("请输入持股公司A名称：（例：招商局轮船股份有限公司）")
    sorceCompany = input()
    while sorceCompany not in company_set:
        print("输入公司名有误，请重新输入持股公司A名称：（例：招商局轮船股份有限公司）")
        sorceCompany = input()
    sorce = perfix + sorceCompany + ">"
    print("请输入持股公司C名称：（例：招商银行股份有限公司）")
    destCompany = input()
    while destCompany not in company_set:
        print("输入公司名有误，请重新输入持股公司C名称：（例：招商局轮船股份有限公司）")
        destCompany = input()
    dest = perfix + destCompany + ">"
    # generate sparql
    sparql1 = generateSparql3new(sorce,5)
    sparql2 = generateSparql3new(dest,5)
    #prepare post url and data
    url = "https://gstore.cstcloud.cn/api"
    postData1  = {
        "action": "queryDB",
        "accesskeyid": "698fd8bec15d47e9ae0b8ed72bce3b1a",
        "access_secret": "2CB8B6E50E05A24D5C0124E44EFF607B",
        "dbName": "jinrong",
        "sparql": sparql1
    }
    postData2  = {
        "action": "queryDB",
        "accesskeyid": "698fd8bec15d47e9ae0b8ed72bce3b1a",
        "access_secret": "2CB8B6E50E05A24D5C0124E44EFF607B",
        "dbName": "jinrong",
        "sparql": sparql2
    }
    # post
    response1 = requests.post(url = url, data = postData1, verify=False)
    response2 = requests.post(url = url, data = postData2, verify=False)
    # output
    json_result1 = json.loads(response1.text)
    if 'msg' in json_result1 and json_result1['msg'] == 'ok' and 'success' in json_result1 and json_result1['success'] == 1:
        print("**********从数据库获取信息成功**********")
    else:
        print("**********从数据库获取信息失败**********")
        print(json_result1['msg'])
        return
    json_result2 = json.loads(response2.text)
    if 'msg' in json_result2 and json_result2['msg'] == 'ok' and 'success' in json_result2 and json_result2['success'] == 1:
        print("**********从数据库获取信息成功**********")
    else:
        print("**********从数据库获取信息失败**********")
        print(json_result2['msg'])
        return
    # print(json_result2)
    print("\n")
    shop_set, shop_list = output3new(json_result1,sorceCompany,5)
    dhop_set, dhop_list = output3new(json_result2,destCompany,5)
    if sorceCompany in dhop_set and destCompany in shop_set:
        print("************* "+sorceCompany+" 与 "+destCompany+" 之间有环")
    else:
        print("************* "+sorceCompany+" 与 "+destCompany+" 之间无环")
        return
    
    edge_list = []
    for path in shop_list:
        if destCompany in path:
            last = sorceCompany
            for now in path:
                edge_list.append((last,now))
                last = now
                if now == destCompany:
                    break
            break
    print("\n")
    for path in dhop_list:
        if sorceCompany in path:
            last = destCompany
            for now in path:
                edge_list.append((last,now))
                last = now
                if now == sorceCompany:
                    break
            break

    DG = nx.DiGraph()
    DG.add_edges_from(edge_list)
    nx.draw(DG, pos = nx.circular_layout(DG), with_labels=True, font_size=10)
    plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签 
    plt.rcParams['axes.unicode_minus']=False
    plt.show()
    
    
    

if __name__ =='__main__':
    urllib3.disable_warnings()
    query3new()

