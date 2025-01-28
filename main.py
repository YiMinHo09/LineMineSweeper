import random
from turtle import TurtleGraphicsError

private_number = ["공지", "지뢰", "활로"] # 프런트 표기용 리스트 (고유 번호를 넣어 텍스트로 변환)
contain = [14, 9, 2] # 공지, 지뢰, 활로 갯수
ground = []
# 맵 생성
while len(ground) < sum(contain):
    i = random.randrange(0, 3)
    print("i:", i)
    if contain[i]:
        print("remain:", contain[i])
        ground.append({"room": i, "opened": 0}) # 방 종류, 방이 밝혀졌는지
        contain[i] -= 1
    print("len:", len(ground))
##
print(ground)

# 인게임에서 사용하는 데이터
winner = 0 # 탈출자 수
survivor = [] # 게임 중인 인원 목록
# 순서 결정
for i in range(9):
    survivor.append("bot%s" % (i+1)) # TODO : 멀티 들어가면 버튼 누르기로 정해야 함
survivor.insert(random.randrange(0, 10), "player")
##
print(survivor)
# 플레이어 행동
def entry(target, player): # target = 방 번호, player = 선수 이름
    if ground[target]["opened"]: # 닫힌 방만 들어갈 수 있음
        global winner
        if ground[target]["room"] == 1:
            survivor.remove(player)
        elif ground[target]["room"] == 2:
            survivor.remove(player)
            winner += 1
        ground[target]["opened"] = 1
##
# 게임 루프
while True:
    for i in survivor: # 순서 진행
        print("==="+i+"===")
        if i == "player": # 플레이어 차례
            input()
        if "bot" in i: # 게임 에이아이
            pass
