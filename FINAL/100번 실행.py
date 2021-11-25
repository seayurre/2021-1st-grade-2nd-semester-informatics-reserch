from queue import PriorityQueue
import psutil
mem = psutil.Process() #저장공간 계산
import time
import HR1

ff = open("C:/Users/yulyu/Desktop/과제연구 집탐 코드/20210901 도로_가공.txt", 'r',encoding="cp949")
쓸파일=open("C:/Users/yulyu/Desktop/결과다.txt","a",encoding="utf-8")
lines = ff.readlines()
#도로 데이터에서 시점명과 종점명이 누락되어 있는 것을 발견함-서울시와 다른 지역 사이 경계에 있는 도로이거나 마땅한 이름이 없는 것으로 추정됨
#이런 데이터들은 삭제하였음(수작업)
ff.close()



#dictionary value로 key값 얻기
def value_to_key(val):
    for key, value in 지명_index.items():
         if val == value:
             return key

s, f = input().split()

###############################################
#휴리스틱 함수 결정하는 변수 p
#무한대는 1e9로 표현

plist = [0.25, 0.5, 1, 2, 1e9]
p_time = []
for i in range(5):
    p_time.append([])

p횟수=[]
for x in range(5):#0이 p=0.25의 등수 정보
    p횟수.append([])
    for y in range(5):
        p횟수[x].append(0)
        
for _ in range(100):
    print("{}번째 실행".format(_+1))
    p순위=[]
    wdata=""
    for k in range(5):
        p = plist[k]
        Node=list()#index, f값, g값, h값을 묶어서 정리
        for x in range(2000):
            Node.append([])
            Node[x].append(0)#index-나중에 맞춰 줄 예정
            Node[x].append(1e9)#f값
            Node[x].append(1e9)#g값
            Node[x].append(1e9)#h값-나중에 맞춰 줄 예정
            Node[x].append(0)#chk-0이면 아직 안 간 거고 1이면 간 점이다

        #지명과 인덱스 대응시키기
        지명_index = {}#value로 int값이 들어감
        index=1
        for line in lines:
            시점명, 종점명, 시간=line.split(',')
            if 시점명 not in 지명_index.keys():
                지명_index[시점명] = index
                Node[index][0]=index
                Node[index][3]=HR1.휴리스틱1(시점명,s,p)
                index+=1
            if 종점명 not in 지명_index.keys():
                지명_index[종점명] = index
                Node[index][0]=index
                Node[index][3]=HR1.휴리스틱1(종점명,s,p)
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

        # 출력=open("C:/Users/yulyu/Desktop/과제연구 집탐 코드/그래프.txt","w",encoding="utf-8")
        # for x in range(1,1999):
        #     if x not in graph:
        #         출력.write("%d번 점은 없다\n"%x)
        #         continue
        #     else:
        #         yeewrite = "{},{},{}\n".format(x, value_to_key(x), graph[x]) #출력이 안돼!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #         출력.write(yeewrite)

        path = []
        timee = 0


        start = 지명_index[s]
        finish = 지명_index[f]
        # print("시작점의 번호는 %d, 끝점의 번호는 %d입니다용"%(start,finish))

        timestart=time.time()

        #0-index 1-f 2-g 3-h 4-chk
        Node[start][1]=Node[start][3]
        Node[start][2]=0

        prev=[]
        for x in range(10000):
            prev.append(0)

        while True:
            #while not q.empty()와 같은 기능을 하는 부분
            끝났나=True
            for x in Node:
                if len(x)!=5: #0번 점이거나 뭔가 문제가 있는 점
                    continue
                if x[4]==0:#Q가 아직 안 비었네!
                    끝났나=False
            if 끝났나:
                print("못 찾고 끝난 것 같다")
                break

            #f값이 가장 작은 점 불러오고, 그 점은 chk를 1로 바꿔주기
            fmin=1e11
            findex=start
            for x in Node:
                if len(x)!=5:
                    continue
                if x[4]==0 and fmin>x[1]:
                    fmin=x[1]
                    findex=x[0]
            Node[findex][4]=1

            #print("%d번 점을 탐색했어요~"%findex)

            if findex==finish:
                # print("찾았다!!")
                break

            #연결된 점들 쭉 탐색
            if findex in graph:
                for v in graph[findex]:
                    vindex=v[0]#연결된 점의 인덱스
                    vw=v[1]#가중치
                    #print("그것과 연결된 %d번 점을 탐색했어요~"%vindex)

                    if Node[vindex][4]==0 and Node[vindex][2]>Node[findex][2]+vw: 
                        Node[vindex][2]=Node[findex][2]+vw
                        prev[vindex]=findex
                        Node[vindex][1]=Node[vindex][2]+Node[vindex][3]

        timefinish=time.time()
        '''
        if p == 1 and _ == 0:
            이전=finish
            print(이전)
            printlist=[]
            while True:
                printlist.append(이전)
                if 이전==start:
                    break
                #printlist.append(prev[이전])
                이전=prev[이전]
            printlist = printlist[::-1]
            for i in printlist:
                print("{} {}".format(i, value_to_key(i)))
            print("소요 시간 : %f"%Node[finish][2])
        '''
        wdata+=str(timefinish-timestart)
        wdata+=','
        print("p=%f : 실행 시간 %f"%(p,timefinish-timestart))
        
        p_time[k].append(timefinish - timestart)
        p순위.append((timefinish - timestart,p))
        # import os
        # os.system("pause")
    wdata+='\n'
    쓸파일.write(wdata)
    p순위.sort()
    for x in range(5):
        if p순위[x][1]==0.25:
            p횟수[0][x]+=1
        elif p순위[x][1]==0.5:
            p횟수[1][x]+=1
        elif p순위[x][1]==1:
            p횟수[2][x]+=1
        elif p순위[x][1]==2:
            p횟수[3][x]+=1
        elif p순위[x][1]==1e9:
            p횟수[4][x]+=1    

'''
for i in range(5):
    psum = 0
    for j in range(len(p_time[i])):
        psum += p_time[i][j]
    print("p = {} : 평균 시간 {}".format(plist[i], psum/len(p_time[i])))
    print("응애")
'''

print(p횟수)