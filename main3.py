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
global g,h,f
g=[]
h=[]
f=[]

s, f = input().split()
start = 지명_index[s]
finish = 지명_index[f]


pq = PriorityQueue()
########start의 f값 ######여기서 f값만 바꿀 수 있는 방법을 찾으면 됨 ! - 파이썬에서 str은 바뀌지 않는다는데... 지금까지 계속 바꾸지 않았나
    
for i in range(1813):
    g.append(1e9)
    f.append(1e9)
    h.append(0)
    g[start] = 0
    path.append(start)

f[start] =h[start]
pq.put((f[start],start)) #start의 f값, start

found = False
while not pq.empty():
    if found:
        print("도착!")
        break
    current = pq.get()[1] #어차피 index 알고 있으니까 q.get()[0]값은 안 가져와도 됨
    path.append(current)


    for v in graph[current]:
        i=v[0]#인덱스
        ga=v[1]#가중치
        if g[i] > g[current] + graph[current][i]:
            g[i]=g[current]+graph[current][i]
            f[i] = g[i] + h[i]
            pq.put((f[i], i))
        if i == finish:
            f[i] = f[current] + graph[current][i]
            found = True


for i in path:
    print(value_to_key(i))

print("시간 : {}".format(f[finish])) 
    


