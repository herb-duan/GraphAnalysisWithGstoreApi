import requests
import urllib3
import json
import networkx as nx
import matplotlib.pyplot as plt

hold = "<http://localhost:2020/vocab/resource/holder_copy_holder_name>"
perfix = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/"

def generateSparql1(sorce = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>",
                   dest = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>"):
    sparql = "\
            select ?1hop ?x ?2hop\
            where { \
                { \
                " + sorce + hold + "?1hop. \
                FILTER (?1hop = " + dest + ")  \
                } \
                UNION \
                { \
                " + sorce + hold + " ?x. \
                ?x "+ hold +" ?2hop. \
                FILTER (?2hop = "+ dest +") \
                } \
            }\
            "
    print("****** 生成的 sparql 语句为：")
    print(sparql)
    return sparql

def output1(json_result,sorceCompany,destCompany):
    list_bindings = json_result['data']['results']['bindings']
    result_len = len(list_bindings)
    edge_list = []
    if result_len == 0:# 没有路径
        print("没有 " + sorceCompany+ " 到 " +destCompany+ " 1跳或2跳路径")
        return
    # 如果存在一跳路径，则输出
    # list_bindings.sort()
    index = 0
    print("**********一跳路径**********")
    if '1hop' in list_bindings[index]:
        index = index + 1
        print(sorceCompany+ " 到 " +destCompany+ " 的一跳路径：\n"+ sorceCompany+ " --> " +destCompany)
        edge_list.append( (sorceCompany,destCompany) )
    else:
        print("没有 " + sorceCompany+ " 到 " +destCompany+ " 的一跳路径")
    
    # 输出2跳路径
    print("**********两跳路径**********")
    if index < result_len and 'x' in list_bindings[index] and '2hop' in list_bindings[index]:
        print(sorceCompany+ " 到 " +destCompany+ " 的二跳路径：")
    else :
        print("没有 " + sorceCompany+ " 到 " +destCompany+ " 的二跳路径")
        DG = nx.DiGraph()
        DG.add_edges_from(edge_list)
        nx.draw(DG, pos = nx.circular_layout(DG), with_labels=True, font_size=10)
        plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签 
        plt.rcParams['axes.unicode_minus']=False
        plt.show()
        return
    
    for i in range(result_len) :
        if index < result_len:
            print(sorceCompany+ " --> " +list_bindings[index]['x']['value'][len(perfix)-1:] + "-->" + list_bindings[index]['2hop']['value'][len(perfix)-1:])
            edge_list.append( (sorceCompany, list_bindings[index]['x']['value'][len(perfix)-1:]) )
            edge_list.append( (list_bindings[index]['x']['value'][len(perfix)-1:],list_bindings[index]['2hop']['value'][len(perfix)-1:]) )
            index = index + 1
    # print(edge_list)
    DG = nx.DiGraph()
    DG.add_edges_from(edge_list)
    nx.draw(DG, pos = nx.circular_layout(DG), with_labels=True, font_size=10)
    plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签 
    plt.rcParams['axes.unicode_minus']=False
    plt.show()


def query1():
    # input
    f = open('./company.txt',encoding='UTF-8')
    company_set =set( f.readlines()[0].split() )
    #print(company_set)
    print("请输入持股公司名称：（例：招商局轮船股份有限公司）")
    sorceCompany = input()
    while sorceCompany not in company_set:
        print("输入公司名有误，请重新输入持股公司名称：（例：招商局轮船股份有限公司）")
        sorceCompany = input()
    sorce = perfix + sorceCompany + ">"
    print("请输入被持股公司名称：（例：招商银行股份有限公司）")
    destCompany = input()
    while destCompany not in company_set:
        print("输入公司名有误，请重新输入被持股公司名称：（例：招商局轮船股份有限公司）")
        destCompany = input()
    dest = perfix + destCompany + ">"
    # generate sparql
    sparql = generateSparql1(sorce,dest)
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
    # print(json_result)
    print("\n")
    output1(json_result,sorceCompany,destCompany)
    

if __name__ =='__main__':
    urllib3.disable_warnings()
    query1()

