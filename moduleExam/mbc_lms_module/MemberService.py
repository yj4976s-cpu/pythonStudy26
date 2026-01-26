# 회원에 관한 Crud를 구현
# 부메뉴와 함께 run()메서드를 진행

import os

class MemberService:

    def __init__(self, file_name="members.txt"):# 객체생성시 만드는 기본값 (생성자)

        self.file_name = file_name
        self.members = []
        self.login_user = None # session대신 login_user사용
        self.load_members()

    def load_members(self):
        self.members = []

        if not os.path.exists(self.file_name):
            self.save_members()
            return

        with open(self.file_name, "r", encoding="utf-8") as f:
            for line in f:  # f변수에 있는 파일객체를 줄단위로 반복한다.
                data = line.strip().split("|")

                data[6] = True if data[6] == "True" else False
                self.members.append(data)

    def save_members(self): # members 2차원 리스트 값을 파일로 덮어쓴다.

        with open(self.file_name, "w", encoding="utf-8") as f:
            for member in self.members: # 메모리에 있는 members 2차원 리스트를 1줄씩 가져온다.
                f.write(f"{member[0]}|{member[1]}|{member[2]}|{member[3]}|{member[4]}|{member[5]}|{member[6]}\n")

    def member_add(self): # self는 클래스의 객체주소
        print("\n[회원가입]")
        uid = input("아이디: ")

        for member in self.members: # 2차원 배열인 members에 1차원 리스트를 가져와 (
            if member[0] == uid:
                print("존재하는 아이디 입니다.")
                return
        sns = []
        for member in self.members:
            if member[1].isdigit(): # 학번이 숫자인지 검사를위해 isdigit을 씀(관리자/교수는 None)
                sns.append(int(member[1]))

        # 학번 결정: 기존 학번이 있으면(최댓값+1), 아니면 20260001부터 시작
        if sns:
            new_sn = str(max(sns)+1)
        else:
            new_sn = "20260001"

        pw = input("비밀번호: ")
        name = input("이름: ")
        email = input("이메일: ")

        print("1. admin 2. professor 3. student")
        role_select = input("권한 선택: ")

        role = "student"
         # 교수/관리자는 학번이 없음
        if role_select == "1":
            role = "admin"
            new_sn = "None"
        elif role_select == "2":
            role = "professor"
            new_sn = "None"

        # 여기까지 변수에 입력 완료
        self.members.append([uid, new_sn, pw, name, email, role, True])
        # 메모리에 있는 2차원리스트 members 뒤에 추가
        self.save_members() # 파일로 저장
        self.load_members()
        print(f"회원가입 완료 새로운 학번: {new_sn}")

    def member_login(self):
        print("로그인메뉴")
        uid = input("아이디: ")
        pw = input("비밀번호: ")
        for i, member in enumerate(self.members):
            if member[0] == uid: # 활성화여부 체크(True인지 확인)
                if not member[6]:
                    print("비활성화/정지된 계정입니다.")
                    return
                if member[2] == pw:
                    self.login_user = member
                    print(f"{member[3]}님 로그인 성공 role: {member[5]}")

                    if member[5] == "admin":  # 관리자 이면
                        self.member_admin()
                        return
                    return

                else:
                    print("비밀번호가 틀렸습니다.")
                    return

        print("존재하지 않는 아이디입니다.")

    def show_member_list(self):
        print("\n[회원목록]")
        print("-" * 80)
        print(f"{'id':10} {'학번':10} {'pw':10} {'이름':10} {'이메일':10} {'권한':10} {'상태':10}") # 아이디 비밀번호 이름 권한 상태 각각 10칸씩 띄워서 보이게함
        print("-" * 80)

        for member in self.members:
            status = "활성화" if member[6] else "비활성화" # member[6] = "활성화"로 하면 메모장에 True가 활성화라는 문자상태로 바뀔수 있어 메모장에서는 바뀌지않고
                                                    # status라는 변수로 바꿔 파이썬 창에서만 활성화로 보이게함
            print(f"{member[0]:10} {member[1]:10} {member[2]:10} {member[3]:10} {member[4]:20}{member[5]:10} {status:20}")

        print("-" * 80)


    def member_admin(self):
        while True:
            print("\n[관리자 메뉴]") # 로그인시 admin = role이면 진입
            print("1. 회원 비밀번호 변경")
            print("2. 회원 블랙리스트 추가")
            print("3. 회원 블랙리스트/휴면게정해제")
            print("4. 회원목록")
            print("0. 종료")

            select = input("선택: ")
            if select == "0":
                print("관리자 메뉴를 종료합니다.")
                break

            if select == "4":
                self.show_member_list()
                continue

            uid = input("대상 아이디: ")

            found = False
            for i, member in enumerate(self.members):
                if member[0] == uid: # 아직 아이디를 찾기 전
                    found = True
                    if select == "1":
                        new_pw = input("새 비밀번호: ")
                        member[2] = new_pw
                        print(f"{member[3]}남의 비밀번호가 변경되었습니다.")
                    elif select == "2":
                        if input(f"{member[3]}님을 블랙리스트에 추가하시겠습니까? (y/n): ").lower() == "y":
                            member[6] = False
                            print(f"{member[2]}님을 블랙리스트로 추가하였습니다.")
                    elif select == "3":
                        if input(f"{member[3]}님의 블랙리스트/휴면계정을 해제하시겠습니까?(y/n): ").lower() == "y":
                            member[6] = True

                            print(f"{member[3]}님의 블랙리스트/휴면계정이 해제되었습니다.")
                        else:
                            print("블랙리스트/휴면계정 해제 취소")

                    self.save_members()  # 파일로 저장
                    self.load_members()
                    print("작업 완료")
                    break
            else:
                print("존재하지 않는 회원입니다.")

    def member_logout(self):
        if self.login_user:
            print(f"{self.login_user[3]}님 로그아웃되었습니다.")
            self.login_user = None

        else:
            print("로그인 후 이용하세요")

    def member_modify(self):
        while True:
            if self.login_user is None:
                print("로그인 후 이용하세요")
                return

            print("\n[내 정보 수정]")
            print("1. 이름 변경")
            print("2. 비밀번호 변경")
            print("3. 이메일 변경")
            print("0. 취소")

            select = input("선택: ")
            if select == "1":
                self.login_user[3] = input("새 이름: ")
            elif select == "2":
                self.login_user[2] = input("새 비밀번호: ")

            elif select == "3":
                self.login_user[4] = input("새 이메일: ")
            elif select == "0":
                break

            self.save_members()
            self.load_members()
            print("내 정보 수정완료")
            break

    def member_delete(self):
        if self.login_user is None:
            print("로그인 후 이용하세요")
            return
        print("\n[회원 탈퇴 및 비활성화]")
        print("1. 계정 비활성화")
        print("2. 회원탈퇴")
        print("0. 취소")

        select = input("선택: ")
        if select == "1":
            if input("계정을 비활성화 하시겠습니까?(y/n): ").lower() == "y":
                self.login_user[6] = False
                print("계정이 비활성화되었습니다.")
                self.login_user = None
            else:
                print("비활성화 취소")
                return

        elif select == "2":
            if input("계정을 탈퇴 하시겠습니까?(y/n): ").lower() == "y":
                for i, member in enumerate(self.members):
                    if member == self.login_user:
                        self.members.pop(i) # self주소와 member정보가 일치하면 삭제
                        break
                self.login_user = None
            else:
                print("계정 탈퇴 취소")

        elif select == "0":
            return

        self.save_members()
        self.load_members()



    def run(self):
        # 부메뉴 구현 메서드
        subrun = True
        while subrun:
            print("""
-----------------------------
1. 로그인
2. 회원가입
3. 회원수정
4. 회원탈퇴
5. 로그아웃


9. 회원서비스 종료
""")

            subSelect = input(">>>")
            if subSelect == "1":
                print("로그인 메서드 호출")
                self.member_login()

            elif subSelect == "2":
                print("회원가입 메서드 호출")
                self.member_add()

            elif subSelect == "3":
                print("회원수정 메서드 호출")
                self.member_modify()

            elif subSelect == "4":
                print("회원탈퇴 메서드 호출")
                self.member_delete()

            elif subSelect == "5":
                print("로그아웃 메서드 호출")
                self.member_logout()

            elif subSelect == "9":
                print("회원서비스 종료")
                subrun = False

            else:
                print("잘못된 메뉴를 선택하였습니다.")


