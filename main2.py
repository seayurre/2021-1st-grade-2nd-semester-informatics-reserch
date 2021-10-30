###############################################
#휴리스틱 함수 결정하는 변수 p
#무한대는 1e9로 표현
p = 3

import psutil
mem = psutil.Process() #저장공간 계산
import time

f = open("C:/Users/yulyu/Desktop/과제연구 집탐 코드/20210901 도로_가공.txt", 'r',encoding="utf-8")
lines = f.readlines()
#도로 데이터에서 시점명과 종점명이 누락되어 있는 것을 발견함-서울시와 다른 지역 사이 경계에 있는 도로이거나 마땅한 이름이 없는 것으로 추정됨
#이런 데이터들은 삭제하였음(수작업)
f.close()

#지명과 인덱스 대응시키기
지명_index = {}#value로 int값이 들어감
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
graph = {}

for line in lines:
    시점명, 종점명, 시간=line.split(',')
    # 시점명.strip()
    # 종점명.strip() #시점명과 종점명 띄어쓰기 삭제
    시점명_index = 지명_index[시점명]
    종점명_index = 지명_index[종점명]
    시간 = float(시간)
    temp = [] #그래프에 추가해줄 이어질 노드와 노드까지의 가중치
    temp.append(종점명_index)
    temp.append(시간)
    if 시점명_index not in graph.keys():
        graph[시점명_index] = []
        graph[시점명_index].append(temp)
    else:
        graph[시점명_index].append(temp)

'''
graph[key]={[[3, 3.0546513], [49,4.5415231]]}
key가 지점의 index
value가 그 지점과 연결된 다른 지점들이고 [index , 가중치]로 저장됨
'''


#dictionary value로 key값 얻기
def value_to_key(val):
    for key, value in 지명_index.items():
         if val == value:
             return key


#휴리스틱 함수 불러오기
import HR1

#우선순위 큐를 사용하기 위한 모듈
from queue import PriorityQueue #queue 모듈의 PriorityQueue 클래스를 가져올 것임

timeTOt = []
최단경로 = []
시간 = 0

#각 정점에서 목적점까지 가는데 걸리는 시간을 배열에 저장한 timeTOt 초기화
#이 휴리스틱이 사용가능한지 체크하기 위함
for  i in range(2000):
    timeTOt.append(0)

#우선순위 큐 설정
pq=PriorityQueue()

#최단경로를 구할 두 지점 입력받기       
시점명, 종점명 = input().split()
시점명_index = 지명_index[시점명]
종점명_index = 지명_index[종점명]

#A* 알고리즘 구현
g = []
h = []
f = []

for x in range(2000):
    g.append(1e9)
    f.append(1e9)
    h.append(0)
for x in range(1, 1633):
    h[x]=HR1.휴리스틱1(value_to_key(x),종점명,p) #1~1632

start = time.time()#시간 측정 시작

chk=[]#이 점을 방문했는가?
for x in range(2000):
    chk.append(False)

'''다른 점들까지의 g는 모두 무한으로 설정해놓고 시작점만 0으로 설정해두기'''
g[시점명_index]=0
f[시점명_index]=h[시점명_index]

chk[시점명_index]=True

pq.put([(-1)*f[시점명_index],시점명_index]) #책과 다르게 한 점 한 점 넣는 방식으로

prev=[]
for x in range(2000):
    prev.append(0) 

print("큐 들어간다")
qcnt=0

#그냥 가중치가 아니라 h(x)+g(x)를 사용해야 하는 것에 유의!
while not pq.empty():
    u=pq.get()
    uvalue=-u[0]#가장 작은 f값
    uindex=u[1]#그 지점의 index
    
    if uindex==종점명_index: #종점에 도달하면!
        print("도착!")
        break

    chk[uindex]=True

    if uindex in graph:
        for node in graph[uindex]: #graph[uindex].items()->uindex와 연결된 모든 점의 [index, 가중치]값들
            thisindex=node[0]#인덱스
            thisvalue=node[1]#가중치

            if chk[thisindex] == False and g[uindex]+thisvalue<g[thisindex]:
                g[thisindex]=g[uindex]+thisvalue
                prev[thisindex]=uindex
                f[thisindex]=g[thisindex]+h[thisindex]
                pq.put([(-1)*f[thisindex],thisindex])
    else:
        print("graph에 %d번 점이 없다! 큰일이네!"%uindex)

print("%d %s"%(종점명_index,value_to_key(종점명_index)))
이전=종점명_index
while True:
    if 이전==시점명_index:
        break
    print("%d %s"%(prev[이전],value_to_key(prev[이전])))
    이전=prev[이전]
print("%d. 따라란~"%g[종점명_index])




'''def Astar(s, u, t): #시작점 s, 현재 정점 u, 목적점 t-----책에서는 편의상 함수로 표현했지만 나는 그냥 함수 쓰는게 불편해서 함수 안 쓰고 함
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
    for 정점과시간 in graph[u]:
        i, 가중치 = 정점과시간.split()
        if i == t:
            최단경로.append(i)
            시간 = 시간 + 가중치
            timeTOt[s] = 시간
            return
        if g[i] > g[u] + 가중치 : 
            g[i] = g[u] + 가중치
            h[i] = HR1.휴리스틱1(value_to_key(i), value_to_key(t),p) 
            f[i] = g[i] + h[i]
            if min > f[i] :
                min = f[i]
                다음정점후보 = i
                시간 = 시간 + 가중치
        print("{}이 갈 수 있는 {} - f:{}, g:{}, h:{}".format(value_to_key(u), value_to_key(i), f[i], g[i], h[i]))
    
    if check == 1:
        최단경로.append(다음정점후보)
        Astar(s, 다음정점후보, t)
    elif check == 0:
        print("갈 수 있는 방법이 없습니다")
        return '''

'''
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
'''
