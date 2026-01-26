import os

from Member import Member

class MemberService:

    def __init__(self, file_name = "members.txt"):
        self.file_name = file_name
        self.members = []
        self.session = None
        self.load_members()

    def run(self):
        run = True
        while run:
            self.main_menu()
            sel = input(">>>")

            if sel == "1": self.member_add()
            elif sel == "2": self.member_login()
            elif sel == "3": self.member_logout()
            elif sel == "4": self.member_modify()
            elif sel == "5": self.member_delete()
            elif sel == "9" : run = False
            else:
                print("잘못 입력하셨습니다.")

    def load_members(self):
        if not os.path.exists(self.file_name):
            self.save_members()
            return
        self.members = []
        with open(self.file_name, "r", encoding="utf-8") as f:
            for line in f:
                self.members.append(Member.from_line(line)) # Member객체에 .from_line() 메서드 실행

    def main_menu(self):
        print("""
====== 회원관리 프로그램 (Member 객체 기반) ======
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
9. 종료
        """)

    def save_members(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            for member in self.members:
                f.write(member.to_line()) # Member객체의 메서드를 사용해 1줄씩 기록

    def member_add(self):
        print("\n[회원가입]")
        uid = input("아이디: ")

        if self.find_member(uid): # 자주쓰는 중복코드로 메서드 처리
            print("존재하는 아이디")
            return
        pw = input("비밀번호: ")
        name = input("이름 : ")
        role = "user"

        self.members.append(Member(uid, pw, name, role))
        self.save_members()
        self.load_members()
        print("회원가입 완료")

    def member_login(self):
        print("\n[로그인]")
        uid = input("아이디 : ")
        pw = input("비밀번호 : ")

        member = self.find_member(uid)

        if not member:
            print("존재하지 않는 아이디")
            return
        if not member.active:
            print("비활성화/블랙리스트계정")
            return
        if member.pw == pw:
            self.session = member
            print(f"{member.name}님 로그인 성공 ({member.role})")

            if member.role == "admin":
                self.member_admin()

        else:
            print("비밀번호 오류")

    def member_admin(self):
        subrun = True
        while subrun:
            print("\n[관리자 메뉴]")
            print("1. 회원 리스트 조회")
            print("2. 회원 비밀번호 변경")
            print("3. 블랙리스트 처리")
            print("4. 블랙리스트/비활성화해제")
            print("5. 권한 변경")
            print("9. 종료")

            sel = input("선택: ")
            if sel == "1":
                self.show_member_list()

            elif sel == "2":
                uid = input("대상 아이디: ")
                member = self.find_member(uid)
                if member:
                    member.pw = input("새 비밀번호: ")
                    self.save_members()
                    print("비밀번호 변경 완료")
                else:
                    print("회원 없음")

            elif sel == "3":
                uid = input("대상 아이디 : ")
                member = self.find_member(uid)
                if member:
                    member.active = False
                    self.save_members()
                    print("블랙리스트 처리 완료")
                else:
                    print("회원 없음")

            elif sel == "4":
                uid = input("대상 아이디 : ")
                member = self.find_member(uid)
                if member:
                    member.active = True
                    self.save_members()
                    print(f"{member.name}님의 블랙리스트/휴면계정이 해제되었습니다.")
                else:
                    print("회원 없음")

            elif sel == "5":
                uid =  input("대상 아이디: ")
                member = self.find_member(uid)
                if member:
                    print("admin/manager/user:")
                    role_select = input("권한 선택: ")
                    if role_select == "1":
                        member.role = "admin"
                        print("admin으로 변경")

                    elif role_select == "2":
                        member.role = "manager"
                        print("manager로 변경")
                    elif role_select == "3":
                        member.role = "user"
                        print("user로 변경")
                    else:
                        print("잘못된 선택입니다")
                        return

                    self.save_members()
                    print("권한 변경 완료")

                else:
                    print("회원 없음")

            elif sel == "9":
                subrun = False


    def member_logout(self):
        self.session = None
        print("로그아웃 완료")

    def member_modify(self):
        if not self.session:
            print("로그인필요")
            self.member_login()
            return

        print("\n[내정보 수정]")
        print("1. 이름 변경")
        print("2. 비밀번호 변경")
        sel = input("선택 : ")
        if sel == "1":
            self.session.name = input("새 이름: ")
        elif sel == "2":
            self.session.pw = input("새 비밀번호: ")

        self.save_members()
        print("수정완료")


    def member_delete(self):
        if not self.session:
            print("로그인필요")
            self.member_login()
            return
        print("1. 완전 탈퇴")
        print("2. 계정 비활성화")
        sel = input("선택: ")
        if sel == "1":
            if input("정말 탈퇴하시겠습니까?(y/n): ").lower() == "y":
                self.members.remove(self.session)
        elif sel == "2":
            if input("계정을 비활성화하시겠습니까?(y/n): ").lower() == "y":
                self.session.active = False

        self.session = None
        self.save_members()
        print("처리완료")


    def find_member(self, uid): # id를 이용해 members에서 찾는 공통메서드
        for member in self.members:
            if member.id == uid:
                print(member.name, "님을 찾았습니다")
                return member
        return None

    def show_member_list(self):
        print("\n[회원 목록]")
        print("-"*60)
        print(f"{'id':10} {'이름':10} {'권한':10} {'상태'}")
        print("-"*60)

        for member in self.members:
            status = "활성" if member.active else "비활성"
            print(f"{member.id:10} {member.name:10} {member.role:10} {status}")

        print("-"*60)



