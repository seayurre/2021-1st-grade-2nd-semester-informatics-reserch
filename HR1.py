def 휴리스틱1(u_지명, t_지명, p): #정점 u, 목적점 t, Minkowski Distance의 p 변수

    # p = 1 : 맨해튼 거리
    # p = 2 : 유클리드 거리
    # p = 무한대(1e9) : 체비쇼프 거리 
    # https://goofcode.github.io/similarity-measure

    f = open("C:/Users/HOME/Desktop/PythonWorkspace/2021 2학기 과제연구/진짜노드좌표.txt", 'r', encoding="utf-8")
    data = f.readlines()
    f.close()

    global u_위도
    global u_경도
    global t_위도
    global t_경도 

    #인덱스 값인 u, t를 대응되는 지명으로 바꿔줌 

    #노드좌표.txt의 값을 바탕으로 u와 t의 좌표값을 받음
    u_위도 = 0
    u_경도 = 0
    t_위도 = 0
    t_경도 = 0

    i = 0
    for line in data:
        i += 1
        place, y, x = line.split(',')
        x = float(x)
        y = float(y)
        if place == u_지명:
            u_위도 = x
            u_경도 = y
        if place == t_지명:
            t_위도 = x
            t_경도 = y
    

    #거리 계산해서 리턴하기
    위도차 = abs(u_위도 - t_위도) * 110 #km
    경도차 = abs(u_경도 - t_경도) * 88.74 #km
    평균속도 = 23/ 3600 #2021/09/01 서울시 평균 속도 23 - km/s
    if p == 1e9 : #p가 무한대인 경우
        return max(위도차, 경도차) / 평균속도
    else:
        d = (abs(위도차**p +  경도차**p)**1/p) / 평균속도
        return d
    