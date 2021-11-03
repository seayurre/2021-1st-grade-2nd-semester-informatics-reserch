from queue import PriorityQueue
import psutil
mem = psutil.Process() #저장공간 계산
import time
import HR1

f = open("C:/Users/HOME/Desktop/PythonWorkspace/2021 2학기 과제연구/20210901 도로_가공.txt", 'r',encoding="cp949")
lines = f.readlines()
#도로 데이터에서 시점명과 종점명이 누락되어 있는 것을 발견함-서울시와 다른 지역 사이 경계에 있는 도로이거나 마땅한 이름이 없는 것으로 추정됨
#이런 데이터들은 삭제하였음(수작업)
f.close()

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

f =[]

#그래프 연결 관계 나타내기
graph=list() #인접행렬
for x in range(2000):
    f.append(0) #f 초기화
    graph.append([])
    for y in range(2000):
        graph[x].append(0)

for line in lines:
    시점명, 종점명, 시간=line.split(',')
    # 시점명.strip()
    # 종점명.strip() #시점명과 종점명 띄어쓰기 삭제
    시점명_index = 지명_index[시점명]
    종점명_index = 지명_index[종점명]
    graph[시점명_index][종점명_index] = float(시간) 

path = []
timee = 0


def Astar(start, finish): #start:시점명, finish:종점명
    q = PriorityQueue()
    q.put((1,start)) #start의 f값, start
    global graph, path, f, g, h, timee
    f[start] = 1 #start의 f값 ######여기서 f값만 바꿀 수 있는 방법을 찾으면 됨 ! - 파이썬에서 str은 바뀌지 않는다는데... 지금까지 계속 바꾸지 않았나

    # if current == start:
    #     for i in range(1813):
    #         g.append(1e9)
    #         f.append(1e9)
    #         h.append(0)
    #     g[start] = 0
    #     path.append(start)

    found = False
    while not q.empty():
        if found:
            break
        current = q.get()[1]
        path.append(current)
        for i in range(1813):
            if graph[current][i] != 0:
                h =  HR1.휴리스틱1(value_to_key(current), value_to_key(i),p) 
                if f[i] > f[current] + graph[current][i] + h:
                    f[i] = f[current] + graph[current][i] + h
                    q.put((f[i], i))
                if i == finish:
                    f[i] = f[current] + graph[current][i]
                    found = True

s, f = input().split()
start = 지명_index[s]
finish = 지명_index[f]
Astar(start, finish)

for i in path:
    print(value_to_key(i))

print("시간 : {}".format(f[finish]))
    


