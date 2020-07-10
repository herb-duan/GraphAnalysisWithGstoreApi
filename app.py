import requests
import urllib3
import json
from query1 import query1
from query2 import query2
from query3 import query3
from query3new import query3new

if __name__ =='__main__':
    urllib3.disable_warnings()
    print("任务1：查询两个公司之间的关联路径（2-hop）并可视化")
    print("任务2：多层股权的穿透式查询并可视化")
    print("任务3：环形持股判断（返回有无环）")
    print("任务4（3plus）：环形持股查询并把环形路径可视化")
    print("请选择任务，输入【1、2、3、4】中的一个数")
    taskNum = input()
    if taskNum == "1":
        query1()
    if taskNum == "2":
        query2()
    if taskNum == "3":
        query3()
    if taskNum == "4":
        query3new()