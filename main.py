import tkinter
import random

# 플레이어 행동
def entry(target, player): # target = 방 번호 (인덱스), player = 선수 이름
    print("entry:", target, player)
    if ground[target]["available"]: # 닫힌 방만 들어갈 수 있음
        output = "" # 프론트 맨 해야 할 말 기록
        global current_player
        output += "%s번 방은 %s입니다." % (target + 1, private_number[ground[target]["room"]]) + "\n"
        print("%s번 방은 %s입니다." % (target + 1, private_number[ground[target]["room"]]))
        if ground[target]["room"] == 1: # 탈락처리
            output += "%s, 탈락입니다." % player + "\n"
            print("%s, 탈락입니다." % player)
            participants[current_player].config(fg="#cF0F0F")
            participants.pop(current_player)
            survivor.remove(player)
        elif ground[target]["room"] == 2: # 통과처리
            global winner
            output = "%s, 통과입니다." % player + "\n"
            print("%s, 통과입니다." % player)
            participants[current_player].config(fg="#CFFFCF")
            participants.pop(current_player)
            winner.append(player)
            survivor.remove(player)
        else: # 보류 처리
            current_player += 1

        # 힌트 공개 (방 열림 처리)
        hint_num = ground[target-1]["room"] + ground[(target+1) % (len(ground))]["room"]
        ground[target]["available"] = 0
        ground[target]["known"] = 1
        output += "%s번방의 힌트 값은 " % (target + 1) + str(hint_num) + " 입니다."
        print("%s번방의 힌트 값은" % (target + 1), hint_num, "입니다.")
        ground[target]["ui"].config(text="%s번 %s[%s]" % (target + 1, private_number[ground[target]["room"]], hint_num),
                                    state="disabled") # 첫번째 방과 마지막 방을 이어주는 예외처리
        return output
##
# 차례를 넘기고 프론트와 백엔드를 연결해주는 역할
def game_loop(target):
    global current_player
    print("parameter:", target)
    participants[current_player].config(bg="#f46c8c")
    subject = survivor[current_player]
    if target != "bot":
        notice.config(text=entry(target, subject)) # 메인 알고리즘 호출 후 리턴값으로 해설함
        print("round check:", current_player, "/", len(survivor))
    else:
        best_choice = {"num": [], "probability": -4} # num 안에 있는 것들이 가장 좋은 방, 확률은 이 방의 잠재 가치
        spade_choice = [] # 삽질 리스트 : 힌트 없이 새로 방을 들어가야 할 때 경우의 수
        print("=알고리즘 시작=")
        for q, a in enumerate(ground):
            probability = -1
            if a["available"]: # 들어갈 수 있는 방의 종류가 뭔지 추론함
                print("!", q, "번째 방")
                for k in [-1, 1]: # 윗 방 아랫방 호출
                    if not ground[(q + k) % (len(ground))]["available"]: # 단서가 있는가
                        print("힌트가 있음", k)
                        if ground[(q + k*2) % (len(ground))]["known"]: # 방의 종류가 확정됨
                            print("정석 추론 가능")
                            a["known"] = 1
                            if a["room"] == 0: # 공지 취급
                                probability = 1
                            elif a["room"] == 1: # 지뢰 취급
                                probability = -1
                            elif a["room"] == 2: # 활로 취급
                                probability = 2
                            # 등록
                            if probability > best_choice["probability"]:
                                best_choice["num"] = [ground.index(a)]
                                best_choice["probability"] = probability
                                print("확률 갱신됨", best_choice)
                            elif probability == best_choice["probability"]:
                                best_choice["num"].append(ground.index(a))
                                print("추가 완료", best_choice)
                            break
                        # ground[target-1]["room"] + ground[(target+1) % (len(ground))]["room"]
                        elif (ground[(q + k - 1)]["room"] + ground[(q + k + 1) % (len(ground))]["room"] == 0
                              or ground[(q + k - 1)]["room"] + ground[(q + k + 1) % (len(ground))]["room"] == 4):
                            print("지뢰 가능성 없음")  # 공지 혹은 활로로 확정됨
                            a["known"] = 1
                            probability = ground[(q + k) % (len(ground))]["room"] + 1
                            # 등록
                            if probability > best_choice["probability"]:
                                best_choice["num"] = [ground.index(a)]
                                best_choice["probability"] = probability
                                print("확률 갱신됨", best_choice)
                                break
                            elif probability == best_choice["probability"]:
                                best_choice["num"].append(ground.index(a))
                                print("추가 완료", best_choice)
                                break
                        else: # 생존 확률만 계산됨
                            print("경우의 수 계산 필요")
                            if ground[q + k]["room"] == 1: # 공지인 경우(0) + 지뢰인 경우(-1)
                                probability = -1
                            if ground[q + k]["room"] == 2: # 활로인 경우(+2) + 공지인 경우(0) + 지뢰인 경우(-1) + 지뢰인 경우(-1)
                                probability = 0
                            if ground[q + k]["room"] == 3: # 활로인 경우(+2) + 지뢰인 경우(-1)
                                if ground[q + -k]["known"] and ground[q + -k]["room"] == 1:
                                    # 3,1 기믹 예외 처리
                                    print("31 기믹 사용")
                                    probability = -1
                                    a["known"] = 1
                                    ground[q + 2]["known"] = 1
                                    ground[q - 2]["known"] = 1
                                else:
                                    probability = 1
                            # 등록
                            if probability > best_choice["probability"]:
                                best_choice["num"] = [ground.index(a)]
                                best_choice["probability"] = probability
                                print("확률 갱신됨", best_choice)
                            elif probability == best_choice["probability"]:
                                best_choice["num"].append(ground.index(a))
                                print("추가 완료", best_choice)
                else: # 무작위로 고를 목록에 추가
                    spade_choice.append(q)
                    print("변두리 방", spade_choice)
        # 최선의 경우가 손해일 때는 무작위로 이동, 반반일 때는 무작위로 이동하거나 계산대로 이동함
        print("= 선택의 시간", subject)
        if best_choice["probability"] < 0 or (best_choice["probability"] == 0 and random.randrange(0, 2)):
            print("삽질을 해야겠어", spade_choice)
            notice.config(text=entry(random.choice(spade_choice), subject))
        else: # 반절 넘으면 계산한 대로 이동
            print("저기로 가야겠어", best_choice)
            notice.config(text=entry(random.choice(best_choice["num"]), subject))
    # 차례 세는 구분자 초기화
    if current_player == len(survivor):
        print("round end")
        current_player = 0
    # 게임 끝내기
    if len(survivor) + len(winner) == 2 or len(winner) == 2:
        print("===game end===")
        sub_title.config(text="게임이 종료되었습니다.\n통과하신 2명의 플레이어 분들을 진심으로 축하합니다.")
        for q in ground:
            # % (방 번호, 해당 방 종류 표기, 힌트숫자)
            q["ui"].config(text="%s번 %s[%s]" % (ground.index(q) + 1, private_number[ground[ground.index(q)]["room"]],
                        ground[ground.index(q) - 1]["room"] + ground[(ground.index(q) + 1) % (len(ground))]["room"]),
                           state="disabled")
        operate_the_bot.config(state="disabled")
    # 버튼 접근 설정
    else:
        sub_title.config(text="%s, 방으로 이동하세요" % survivor[current_player])
        participants[current_player].config(bg="#FFCFCF")
        if survivor[current_player] != "player":
            operate_the_bot.config(state="normal")
            for q in ground:
                q["ui"].config(state="disabled")
        else:
            operate_the_bot.config(state="disabled")
            for q in ground:
                if q["available"]:
                    q["ui"].config(state="normal")
    print("==loop next==")

# 프론트 설정
window = tkinter.Tk()
if window.winfo_screenwidth() < 1400:
    width = 1400
else:
    width = window.winfo_screenwidth() // 3 * 2
height = width // 10 * 7
window.geometry("%sx%s+%s+%s" % (width, height, (window.winfo_screenwidth() - width) // 2,
                                 (window.winfo_screenheight() - height) // 4))
window.configure(bg="#F46C8C")
window.title("위 아래 지뢰찾기")
window.iconbitmap("icon.ico")

# 기본 요소 배치
ui_ground = tkinter.Frame(window, width=width / 2, height=height, bg="#f46c8c")
leaderboard = tkinter.Frame(window, width=width / 2, height=height, bg="#f46c8c")
ui_ground.pack(side="left")
leaderboard.pack(side="right")
front_man = tkinter.Frame(window, width=width, height=height // 10, bg="#0e0e0e")
front_man.pack()

# 방 관련 데이터
private_number = ["공지", "지뢰", "활로"] # 프런트 표기용 리스트 (고유 번호를 넣어 텍스트로 변환)
contain = [13, 10, 2] # 공지, 지뢰, 활로 갯수
ground = [] # 게임판

# 맵 생성
for i in range(sum(contain)):
    # 방 종류 무작위 선택 (제비뽑기 해서 순서대로 배치하는 방식)
    print("list:", contain)
    choice = random.randrange(1, sum(contain) + 1)
    print("choice:", choice)
    if choice <= contain[0]:
        room_num = 0
    elif choice <= contain[0] + contain[1]:
        room_num = 1
    else:
        room_num = 2
    print("type:", room_num)
    ##
    if contain[room_num]:
        print("remain:", contain[room_num])
        ground.append({"room": room_num, "available": 1,
                       "ui": tkinter.Button(ui_ground, text="%s번" % (len(ground) + 1), width=width // 24,
                                            command=lambda t=len(ground): game_loop(t),
                                            bg="#36393f", fg="#b4b5b7"),
                       "known": 0})
        # room : 방 종류, available : 방을 선택할 수 있는가, ui : 이 방을 화면에 표기하는 객체, known : 방 정보가 공개되었는가
        # known은 봇이 사용하는 정보입니다. (멀티 들어가면 없어집니다)
        print("ground:", ground)
        contain[room_num] -= 1
        ground[-1]["ui"].pack()
    else: # 개발 중간 단계에서 사용한 예외처리. 이번 연산을 무효화 시키고 정상적인 아웃풋으로 수렴하게 하는 역할
        print("!예외 발생!") # 하지만 예외가 발생하면 어딘가는 확률이 편향되어 있다는 의미이므로 지금은 실행되면 안됨
    print("len:", len(ground), "\n")
##
print(ground)

# 인게임에서 사용하는 데이터
winner = [] # 탈출자 목록
survivor = [] # 게임 중인 인원 목록
participants = [] # 화면에 띄울 객체들 목록 (survivor과 인덱스를 공유합니다.)
##

# 순서 결정 (다음 코드들은 봇전 전용입니다)
for i in range(9):
    survivor.append("bot%s" % (i+1)) # 멀티 들어가면 버튼 누르기로 정해야 합니다
    participants.append(tkinter.Label(leaderboard, text=survivor[-1], font=("Basic", height // 30), bg="#f46c8c"))
my_turn = random.randrange(0, 10)
survivor.insert(my_turn, "player")
participants.insert(my_turn, tkinter.Label(leaderboard, text="player", font=("Basic", height // 30), bg="#f46c8c"))
for i in participants:
    i.pack()
operate_the_bot = tkinter.Button(leaderboard, text="봇 이동 시키기", command=lambda: game_loop("bot"))
if survivor[0] == "player":
    operate_the_bot.config(state="disabled")
else:
    operate_the_bot.config(state="normal")
    for e in ground:
        e["ui"].config(state="disabled")
operate_the_bot.pack()
##
print(survivor)

notice = tkinter.Label(front_man, text="", font=("Basic", height // 20))
notice.pack()
sub_title = tkinter.Label(front_man, text="",font=("Basic", height // 40, "bold"))
sub_title.pack()
current_player = 0

participants[0].config(bg="#FF2F2F")
notice.config(text="게임을 시작하겠습니다.", bg="#0e0e0e", fg="light gray")
sub_title.config(text="1번은 이동해 주십시오.", bg="#0e0e0e", fg="light gray")

print("===game start===")
window.mainloop()
