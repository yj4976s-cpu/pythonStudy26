import os
# MemberManager
#  ├─ file_name 변수
#  ├─ members
#  ├─ session
#  ├─ load_members() 메서드
#  ├─ save_members()
#  ├─ member_add()
#  ├─ member_login()
#  ├─ member_admin()
#  ├─ member_logout()
#  ├─ member_modify()
#  ├─ member_delete()
#  ├─ main_menu()
#  └─ run()

class MemberManager: # 객체를 담당하는 클래스 사용법은 변수 = MemberManager() 생성

        # 클래스에서 self는 객체의 주소를 가지고 있음.
        # def__init__(self) 클래스 구현시 필수
    def __init__(self,file_name = "members.txt"): # 객체생성시 만드는 기본값 (생성자)
        self.file_name = file_name # 객체에 파일이름을 넣는다.
        self.members = []          # 객체에 members 리스트를 만든다.
        self.session = None        # 객체에 세션변수를 만들고 기본값으로 None 처리(정수)
        self.load_members()        # 아래에 선언된 load_members() 메서드를 호출한다.

    # =====================
    # 파일로드
    # =====================
    def load_members(self): # 앞으로 만들 메서드는() 괄호 안에 self가 필수
        self.members = [] # 빈배열로 생성 (혹시나, 이전에 리스트가 남아있을 수 있음)

        if not os.path.exists(self.file_name):
            self.save_members() # 동일 디렉토리에 파일명이 없으면
            return                             # save_members()메서드를 호출 (open()으로 파일생성)
                                            # load_members()메서드를 빠져나와라

        with open(self.file_name, "r", encoding="utf-8") as f:
            #     members.txt    읽기 전용  한글처리필수  -> f라는 변수에 넣어라
            for line in f:  # f변수에 있는 파일객체를 줄단위로 반복함
                data = line.strip().split("|")
                # 1줄 읽은 값을 엔터제거 | 를 기준으로 잘라 -> 1차원 리스트로 생성
                # ["kkw","1234","김기원","admin","True"]
                data[4] = True if data[4] == "True" else False
                # 리스트 5번째 값이 문자열 True이면 불타입 True로 변경 아니면 False
                self.members.append(data)
                # 2차원 배열인 members 맨뒤에 추가 for문 종료까지

    # ====================
    # 파일 저장
    # ====================
    def save_members(self): # members 2차원 리스트 값을 파일로 덮어쓴다.
        # 왜? 파일처리는 수정을 하지 않는다. r(읽기전용), w(덮어쓰기), a(마지막에 추가)
        with open(self.file_name, "w", encoding="utf-8") as f:
            #     members.txt     덮어쓰기      한글처리 -> f변수에 넣어라.
            for member in self.members: # 메모리에 있는 members 2차원 리스트를 1줄씩 가져와
                # member 변수에 넣어라.
                # member = ["kkw", "1234", "김기원", "admin", "True"]
                f.write(f"{member[0]}|{member[1]}|{member[2]}|{member[3]}|{member[4]}\n")
                #               kkw|1234|김기원|admin|True엔터   -> write 저장
                #                                              -> for가 종료될때까지

    # ====================
    # 회원가입
    # ====================
    def member_add(self): # self는 클래스의 객체주소
        print("\n[회원가입]")
        uid = input("아이디: ") # 키보드에 입력한 값을 uid변수에 넣음

        for member in self.members: # 2차원 배열인 members에 1차원 리스트를 가져와 (1줄)
            if member[0] == uid:
                print("존재하는 아이디 입니다.")
                return # member_add() 메서드를 빠져나온다.

        # 중복 id가 없으면 아래쪽 코드 실행 -> else : 로 처리해도 되나-> 들여쓰기 필수
        pw = input("비밀번호: ")
        name = input("이름: ")

        print("1. admin 2. manager 3. user")
        role_select = input("권한 선택: ")

        role = "user"
        if role_select == "1":
            role = "admin"
        elif role_select == "2":
            role = "manager"


        # 여기까지 변수에 입력 완료
        self.members.append([uid,pw,name,role,True])
        # 메모리에 있는 2차원리스트 members 뒤에 추가!! .append()
        self.save_members() # 파일로 저장
        self.load_members()
        print("회원가입 완료")


    # =================
    # 로그인
    # =================

    def member_login(self):
        print("\n[로그인]")
        uid = input("아이디: ")
        pw = input("비밀번호: ")

        # enumerate() -> 2차원 배열을 인덱스와 리스트를 추출한다.
        for i, member in enumerate(self.members):
        #  idx, member
            if member[0] == uid: # for문 중에 같은 아이디가 있으면
                if not member[4]: # active가 false인지 확인
                    print("비활성화/블랙리스트에 추가된 계정입니다.")
                    return # member_login()메서드를 빠져나온다.

                # ["kkw", "1234", "김기원", "admin", "True"]
                #    0       1       2        3        4
                # active가 True이면
                if member[1] == pw: # member[]
                    self.session = i # session 변수에 인덱스를 넣는다. (회원주소)
                    print(f"{member[2]}님 로그인 성공 ({member[3]})")

                    if member[3] == "admin": # 관리자 이면
                        self.member_admin() # 메서드를 호출한다.(관리자메뉴)
                    return

                else: # if member[1] == pw 결과가 False이면
                    print("비밀번호가 틀렸습니다.")
                    return # member_login()메서드를 빠져나온다.

        print("존재하지 않는 아이디입니다.") # for문에 return이 안걸리면 여기까지 온다.

    def show_member_list(self):
        print("\n[회원목록]")
        print("-" * 60)
        print(f"{'id':10} {'pw':10} {'이름':10} {'권한':10} {'상태':10}") # 아이디 비밀번호 이름 권한 상태 각각 10칸씩 띄워서 보이게함
        print("-" * 60)

        for member in self.members:
            status = "활성화" if member[4] else "비활성화" # member[4] = "활성화"로 하면 메모장에 True가 활성화라는 문자상태로 바뀔수 있어 메모장에서는 바뀌지않고
                                                    # status라는 변수로 바꿔 파이썬 창에서만 활성화로 보이게함
            print(f"{member[0]:10} {member[1]:10} {member[2]:10} {member[3]:10} {status:10}")

        print("-" * 60)

    # ===================================
    # 관리자 기능
    # ===================================
    def member_admin(self):
        while True:
            print("\n[관리자 메뉴]") # 로그인시 admin = role이면 진입
            print("1. 회원 비밀번호 변경")
            print("2. 회원 블랙리스트 추가")
            print("3. 회원 블랙리스트/휴면게정해제")
            print("4. 회원 권한 변경")
            print("5. 회원목록")
            print("0. 종료")

            select = input("선택: ") # 관리자 메뉴 선택용
            if select == "0": # 대상 id 찾는 입력
                print("관리자 메뉴를 종료합니다.")
                break

            if select == "5":
                self.show_member_list()
                continue

            uid = input("대상 아이디: ")

            for member in self.members: # members의 2차원 배열을 반복
                if member[0] == uid:    # 대상 id를 찾으면
                    if select == "1":   # 비밀번호 변경
                        member[1] = input("새 비밀번호: ")
                        print("회원비밀번호 변경완료")
                    elif select == "2": # 블랙리스트 처리
                        if input(f"{member[2]}님을 블랙리스트로 추가하시겠습니까?(y/n): ").lower() == "y": # y를 대문자로 입력할경우를 대비해 lower()함수 입력
                            member[4] = False
                            print(f"{member[2]}님을 블랙리스트로 추가하였습니다.")
                        else:
                            print("블랙리스트 취소")

                    elif select == "3":
                        if input(f"{member[2]}님의 블랙리스트/휴면계정을 해제하시겠습니까?(y/n): ").lower() == "y":
                            member[4] = True
                            print(f"{member[2]}님의 블랙리스트/휴면계정이 해제되었습니다.")
                        else:
                            print("블랙리스트/휴면계정 해제 취소")

                    elif select == "4": # 권한 변경 입력
                        member[3] = input("admin / manager / user: ")
                        print("회원권한을 변경하였습니다.")

                    self.save_members() # 파일로 저장
                    self.load_members()
                    print("작업 완료")
                    break
            else:
                print("존재하지 않는 회원입니다.")

    # ====================================
    # 로그아웃
    # ====================================

    def member_logout(self):
        if self.session is None:
            print("로그인 후 이용하세요")
            return
        if input("로그아웃하시겠습니까?(y/n): ").lower() == "y":
            print("로그아웃 완료")
            self.session = None # 세션값에 있는 인덱스를 None 처리함
        else:
            print("로그아웃 취소")
            return

    # ====================================
    # 내정보 수정
    # ====================================
    def member_modify(self):
        while True:
            if self.session is None: # 현재 세션에 값이 None이면?
                print("로그인 후 이용하세요")
                return
            print("\n[내 정보 수정]")
            print("1. 이름 변경")
            print("2. 아이디 변경")
            print("3. 비밀번호 변경")

            select = input("선택: ")

            if select == "1": # 이름변경
                self.members[self.session][2] = input("새 이름: ")
                # 2차원배열     로그인인덱스  이름필드
            elif select == "2":
                self.members[self.session][0] = input("새 아이디: ")

            elif select == "3":
                self.members[self.session][1] = input("새 비밀번호: ")
                #   2차원 배열      로그인인덱스   암호필드

            self.save_members()
            self.load_members()
            print("내 정보 수정완료")
            break

    # ====================================
    # 회원탈퇴
    # ====================================

    def member_delete(self):
        if self.session is None:
            print("로그인 후에 이용하세요")
            return

        print("\n[회원 탈퇴]")
        print("1. 계정 비활성화")
        print("2. 회원 탈퇴")

        select = input("선택: ")
        if select == "1":
            if input("계정을 비활성화 하시겠습니까?(y/n): ").lower() == "y":
                self.members[self.session][4] = False
            else:
                print("비활성화 취소")

        if select == "2":
            if input("계정을 삭제 하시겠습니까?(y/n): ").lower() == "y":
                self.members.pop(self.session)
            else:
                print("계정 삭제 취소")

        self.session = None
        self.save_members() # 파일로 저장
        self.load_members() # 다시 파일에 있는 내용 불러오기
        print("계정처리완료")

    # ====================================
    # 메뉴
    # ====================================
    def main_menu(self):
        print("""
========== 회원관리 프로그램(class기반) =========
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
6. 종료
""")

    # ===================================
    # 실행
    # ===================================
    def run(self):
        while True:
            self.main_menu()
            select = (input(">>>"))

            if select == "1": self.member_add()
            elif select == "2": self.member_login()
            elif select == "3": self.member_logout()
            elif select == "4": self.member_modify()
            elif select == "5": self.member_delete()
            elif select == "6": break

# ===================================
# 프로그램 시작
# ===================================

app = MemberManager() # 가장 중요한 포인트(지금까지 만든 클래스를 객체로 만들고)
app.run() # 객체있는 .run()메서드를 실행한다.




