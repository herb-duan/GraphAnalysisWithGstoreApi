import requests
import urllib3
import json

hold = "<http://localhost:2020/vocab/resource/holder_copy_holder_name>"
perfix = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/"

def generateSparql3(sorce = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>",
                   dest = "<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>"):
    sparql = "\
            ask { \
                " + sorce + hold + "?A1hop. \
                   ?A1hop" + hold +" ?A2hop. \
                   ?A2hop" + hold +" ?A3hop. \
                   ?A3hop" + hold +" ?A4hop. \
                    ?A4hop" + hold +" ?A5hop. \
                    FILTER (?A1hop =" + dest + " || ?A2hop =" + dest + "||?A3hop =" + dest +"\
                     ||?A4hop =" + dest + "||?A5hop =" + dest + ")  \
                    " + dest + hold + "?B1hop. \
                   ?B1hop" + hold +" ?B2hop. \
                   ?B2hop" + hold +" ?B3hop. \
                   ?B3hop" + hold +" ?B4hop. \
                    ?B4hop" + hold +" ?B5hop. \
                    FILTER (?B1hop =" + sorce + " || ?B2hop =" + sorce + "||?B3hop =" + sorce +"\
                     ||?B4hop =" + sorce + "||?B5hop =" + sorce + ")  \
            }\
            "
    print("****** 生成的 sparql 语句为：")
    print(sparql)
    return sparql

def output3(json_result,sorceCompany,destCompany):
    list_bindings = json_result['data']['results']['bindings']
    print(list_bindings[0]['askResult']['value'])
    if list_bindings[0]['askResult']['value'] == True:
        print("************* "+sorceCompany+" 与 "+destCompany+" 之间有环")
    else:
        print("************* "+sorceCompany+" 与 "+destCompany+" 之间无环")
        return


def query3():
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
    sparql = generateSparql3(sorce,dest)
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
    print(json_result)
    print("\n")
    output3(json_result,sorceCompany,destCompany)
    

if __name__ =='__main__':
    urllib3.disable_warnings()
    query3()


"""
ask {                 
    <file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司><http://localhost:2020/vocab/resource/holder_copy_holder_name>?A1hop.
    ?A1hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?A2hop.
    ?A2hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?A3hop.
    ?A3hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?A4hop.
    ?A4hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?A5hop.
    FILTER (?A1hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司> || 
    ?A2hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>||
    ?A3hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>||
    ?A4hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>||
    ?A5hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司>)
    <file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商银行股份有限公司><http://localhost:2020/vocab/resource/holder_copy_holder_name>?B1hop.
    ?B1hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?B2hop.
    ?B2hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?B3hop.
    ?B3hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?B4hop.
    ?B4hop<http://localhost:2020/vocab/resource/holder_copy_holder_name> ?B5hop.
    FILTER (?B1hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司> ||
    ?B2hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>||
    ?B3hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>||
    ?B4hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>||
    ?B5hop =<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/招商局轮船股份有限公司>)
    }
"""