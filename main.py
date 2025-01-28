import random

private_number = ["공지", "지뢰", "활로"] # 프런트 표기용 리스트 (고유 번호를 넣어 텍스트로 변환)
contain = [14, 9, 2] # 공지, 지뢰, 활로 갯수
ground = []
# 맵 생성
for i in range(sum(contain)):
    # 방 종류 무작위 선택 (제비뽑기 해서 순서대로 배치하는 방식)
    print("list:", contain)
    room = random.randrange(1, sum(contain)+1)
    print("choice:", room)
    if room <= contain[0]:
        room_num = 0
    elif room <= contain[0] + contain[1]:
        room_num = 1
    else:
        room_num = 2
    print("type:", room_num)
    ##
    #
    if contain[room_num]:
        print("remain:", contain[room_num])
        ground.append({"room": room_num, "available": 1}) # 방 종류, 방이 밝혀졌는지
        contain[room_num] -= 1
    else: # 테스트 코드인데 혹시 몰라서 남김
        print("!예외 발생!")
    print("len:", len(ground), "\n")
##
print(ground)

# 인게임에서 사용하는 데이터
winner = [] # 탈출자 목록
survivor = [] # 게임 중인 인원 목록
# 순서 결정
for i in range(9):
    survivor.append("bot%s" % (i+1)) # TODO : 멀티 들어가면 버튼 누르기로 정해야 함
survivor.insert(random.randrange(0, 10), "player")
##
print(survivor)
# 플레이어 행동
def entry(target, player): # target = 방 번호, player = 선수 이름
    if ground[target]["available"]: # 닫힌 방만 들어갈 수 있음
        print("%s번 방은 %s입니다." % (target, private_number[ground[target]["room"]]))
        global winner
        if ground[target]["room"] == 1: # 탈락처리
            print("%s, 탈락입니다." % player)
            survivor.remove(player) ##
        elif ground[target]["room"] == 2: # 통과처리
            print("%s, 통과입니다." % player)
            winner.append(player)
            survivor.remove(player) ##
        # 힌트 공개
        ground[target]["available"] = 0
        print(target, ground[target-1], ground[target+1])
        print("%s번방의 힌트 번호는 " % target, end="")
        if target == len(ground)-1:
            print(ground[target-1]["room"] + ground[0]["room"], "입니다.")
        else:
            print(ground[target-1]["room"] + ground[target+1]["room"], "입니다.") ##
##
# 게임 루프
while len(survivor) + len(winner) > 2: # TODO : 이 조건이 entry 안에 들어가야 함
    back_up = list(survivor)
    for i in back_up: # 순서 진행
        print("==="+i+"===")
        if i == "player": # 플레이어 차례
            entry(int(input("들어갈 방 번호")), i)
        if "bot" in i: # 게임 에이아이
            pass
    input("break point")
print("게임이 종료되었습니다.")
##