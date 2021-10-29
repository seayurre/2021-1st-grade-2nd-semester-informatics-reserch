###############################################
#휴리스틱 함수 결정하는 변수 p
#무한대는 1e9로 표현
p = 1

import psutil
mem = psutil.Process() #저장공간 계산


import time

f = open("C:/Users/HOME/Desktop/PythonWorkspace/2021 2학기 과제연구/20210901 도로_가공.txt", 'r',encoding="utf-8")
lines = f.readlines()
#도로 데이터에서 시점명과 종점명이 누락되어 있는 것을 발견함-서울시와 다른 지역 사이 경계에 있는 도로이거나 마땅한 이름이 없는 것으로 추정됨
#이런 데이터들은 삭제하였음(수작업)
f.close()

#지명과 인덱스 대응시키기
지명_index = {}
index=1
for line in lines:
    시점명, 종점명, 시간=line.split(',')
    if 시점명 not in 지명_index.keys():
        지명_index[시점명] = index
        index+=1
    if 종점명 not in 지명_index.keys():
        지명_index[종점명] = index
        index+=1
    

#그래프 연결 관계 나타내기
a=list() #인접행렬
for x in range(2000):
    a.append([])
    for y in range(2000):
        a[x].append(0)

for line in lines:
    시점명, 종점명, 시간=line.split(',')
    # 시점명.strip()
    # 종점명.strip() #시점명과 종점명 띄어쓰기 삭제
    시점명_index = 지명_index[시점명]
    종점명_index = 지명_index[종점명]
    a[시점명_index][종점명_index] = float(시간)


#dictionary value로 key값 얻기
def value_to_key(val):
    for key, value in 지명_index.items():
         if val == value:
             return key


#휴리스틱 함수 불러오기
import HR1

#A* 알고리즘 구현
g = []
h = []
f = []
timeTOt = []
최단경로 = []
시간 = 0

#각 정점에서 목적점까지 가는데 걸리는 시간을 배열에 저장한 timeTOt 초기화
for  i in range(2000):
    timeTOt.append(0)

def Astar(s, u, t): #시작점 s, 현재 정점 u, 목적점 t
    global 시간
    global 최단경로
    if s == u:
        for i in range(1813):
            g.append(1e9)
            f.append(1e9)
            h.append(0)
        g[s] = 0
        최단경로.append(s)
    
    if u == t:
        print("도착")
        return     

    min = 1e9 #최소 f값을 가지는 다음 정점을 찾기 위한 변수
    다음정점후보 = 0
    check = 0 #현재 노드에 연결된 다른 노드가 있는지 확인하기 위한 변수
    for i in range(1813):
        if a[u][i] != 0 and i != u:
            #print("연결된 지점 : " + value_to_key(u) + " " + value_to_key(i))
            check = 1
            if i == t:
                최단경로.append(i)
                시간 = 시간 + a[u][i]
                timeTOt[s] = 시간
                return
            if g[i] > g[u] + a[u][i] : 
                g[i] = g[u] + a[u][i]
                h[i] = HR1.휴리스틱1(value_to_key(i), value_to_key(t),p) 
                f[i] = g[i] + h[i]
                if min > f[i] :
                    min = f[i]
                    다음정점후보 = i
                    시간 = 시간 + a[u][i]
            print("{}이 갈 수 있는 {} - f:{}, g:{}, h:{}".format(value_to_key(u), value_to_key(i), f[i], g[i], h[i]))
    
    if check == 1:
        최단경로.append(다음정점후보)
        Astar(s, 다음정점후보, t)
    elif check == 0:
        print("갈 수 있는 방법이 없습니다")
        return 


#최단경로를 구할 두 지점 입력받기       
시점명, 종점명 = input().split()
시점명_index = 지명_index[시점명]
종점명_index = 지명_index[종점명]


start = time.time()
#Astar 함수를 실행해 최단경로 구하기
Astar(시점명_index, 시점명_index, 종점명_index)
finish = time.time()

availableHR = 1
for i in range(1813):
    if timeTOt[i] < h[i]:
        availableHR = 0

if availableHR == 0:
    print("p = {}일 때는 불가능한 휴리스틱 함수입니다".format(p))

#최단경로와 최단경로로 갈 때 걸리는 시간 출력하기
print("---------최단경로-----------")
for i in 최단경로:
    print("{} - f:{}, g:{}, h:{}".format(value_to_key(i), f[i], g[i], h[i]))
print()
print("걸리는 시간 :", 시간)
print("p = {}인 휴리스틱 함수를 사용할 때 Astar 함수 시간 : {}".format(p, finish - start)) 

print(mem.memory_info()) #저장공간 출력 - rss 값 byte 확인
