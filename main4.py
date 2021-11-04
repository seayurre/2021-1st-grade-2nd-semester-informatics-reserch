from queue import PriorityQueue
import psutil
mem = psutil.Process() #저장공간 계산
import time
import HR1

ff = open("C:/Users/yulyu/Desktop/과제연구 집탐 코드/20210901 도로_가공.txt", 'r',encoding="cp949")
lines = ff.readlines()
#도로 데이터에서 시점명과 종점명이 누락되어 있는 것을 발견함-서울시와 다른 지역 사이 경계에 있는 도로이거나 마땅한 이름이 없는 것으로 추정됨
#이런 데이터들은 삭제하였음(수작업)
ff.close()

#dictionary value로 key값 얻기
def value_to_key(val):
    for key, value in 지명_index.items():
         if val == value:
             return key



###############################################
#휴리스틱 함수 결정하는 변수 p
#무한대는 1e9로 표현
p = 1

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


path = []
timee = 0

s, f = input().split()
start = 지명_index[s]
finish = 지명_index[f]


Node=list()#index, f값, g값, h값을 묶어서 정리
Node.append([])
for x in range(1, 1814):
    Node.append([])
    Node[x].append(x)#index
    Node[x].append(1e9)#f값
    Node[x].append(1e9)#g값
    Node[x].append(HR1.휴리스틱1(value_to_key(x),종점명,p))#h값
    Node[x].append(0)#chk-0이면 아직 안 간 거고 1이면 간 점이다

#0-index 1-f 2-g 3-h 4-chk
Node[start][1]=Node[start][3]
Node[start][2]=0

while True:
    #while not q.empty()와 같은 기능을 하는 부분
    끝났나=True
    for x in Node:
        if x[4]==0:#Q가 아직 안 비었네!
            끝났나=False
    if 끝났나:
        print("못 찾고 끝난 것 같다")
        break

    #f값이 가장 작은 점 불러오고, 그 점은 chk를 1로 바꿔주기
    fmin=1e11
    findex=start
    for x in Node:
        if x[4]==0 and fmin>x[1]:
            fmin=x[1]
            findex=x[0]
    Node[findex][4]=1

    if findex==finish:
        print("찾았다!!")
        break

    for v in graph[findex]:
        vindex=v[0]
        vw=v[1]

        if Node[vindex][4]==0 and Node[vindex][2]>Node[findex][2]+vw:
            Node[vindex][2]=Node[findex][2]+vw
            Node[vindex][1]=Node[vindex][2]+Node[vindex][3]

print(Node[finish][2])



        




for i in path:
    print(value_to_key(i))

print("시간 : {}".format(f[finish])) 
    


