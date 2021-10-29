def 휴리스틱2(u_지명, t_지명, p):
    f = open("C:/Users/HOME/Desktop/PythonWorkspace/2021 2학기 과제연구/진짜노드좌표.txt", 'r', encoding="utf-8")
    lines = f.readlines()
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
