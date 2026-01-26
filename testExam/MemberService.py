import os

from Member import Member # 회원 객체 추가연결

class MemberService:
    def __init__(self,file_name="members.txt"):
    # 클래스 생성시 초기값 관리
        self.file_name = file_name
        self.members = [] # 회원리스트를 Member()객체에 담는다.

        self.session = None # 로그인 상태를 담당
        self.load_members() # 아래쪽 메서드 호출

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
            elif sel == "9": run = False
            else:
                print("잘못된 입력입니다.")


    def load_members(self): # 파일에서 메모리로 불러옴
        if not os.path.exists(self.file_name):
            self.save_members()
            return
        self.members = [] # 혹시 남아있을지 모르는 메모리 값을 초기화
        with open(self.file_name,"r", encoding="utf-8") as f:
            for line in f:
                self.members.append(Member.from_line(line)) # Member객체에 .from_line()메서드 실행

    def save_members(self):
        with open(self.file_name,"w", encoding="utf-8") as f:
            for member in self.members:
                f.write(member.to_line())

    def find_member(self,uid): # id를 이용해 members에서 찾는 공통 메서드
        for member in self.members:
            if member.id == uid:
                print(member.name,"님을 찾았습니다")
                return member # 같은게 있으면 member객체를 리턴
        return None

    def member_add(self):
        print("\n[회원가입]")
        uid = input("아이디: ")
        if self.find_member(uid): # 중복코드로 메서드 처리
            print("존재하는 아이디")
            return

        pw = input("비밀번호: ")
        name = input("이름: ")
        email = input("이메일: ")
        role = "user"

        self.members.append(Member(uid,pw,name,email,role))
        self.save_members()
        self.load_members()
        print("회원가입 완료")

    def member_login(self):
        print("\n[로그인]")
        uid = input("아이디: ")
        pw =  input("비밀번호: ")
        member = self.find_member(uid)
        if not member:
            print("존재하지 않는 아이디")
            return
        if not member.active:
            print("비활성화 계정")
            return
        if member.pw == pw:
            self.session = member
            print(f"{member.name}님 로그인 성공 ({member.role})")

            if member.role == "admin":
                self.member_admin() # 관리자용 메서드로 들어간다

        else:
            print("비밀번호 오류")

    def member_logout(self):
        self.session = None
        print("로그아웃 완료")

    def member_modify(self):
        if not self.session:
            print("로그인 필요")
            return

        print("\n[내정보 수정]")
        print("1. 이름 변경")
        print("2. 비밀번호 변경")
        print("3. 이메일 변경")
        sel = input("선택: ")

        if sel == "1":
            self.session.name = input("새 이름: ")
        elif sel == "2":
            self.session.pw =  input("새 비밀번호: ")
        elif sel == "3":
            self.session.email = input("새 이메일: ")

        self.save_members()
        print("정보 수정 완료")

    def member_delete(self):
        if not self.session:
            print("로그인 필요")
            return
        print("1. 완전탈퇴")
        print("2. 비활성화")
        sel = input("선택: ")
        if sel == "1":
            self.members.remove(self.session)
        elif sel == "2":
            self.session.active = False

        self.session = None
        self.save_members()
        print("처리 완료")


    def main_menu(self):
        print("""
============ 회원관리 프로그램 ===========
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보 수정
5. 회원탈퇴
9. 종료""")

    def member_admin(self): # role = "admin에 진입가능한 메서드
        subrun = True
        while subrun:
            print("\n[관리자 메뉴]")
            print("1. 회원리스트 조회")
            print("2. 비밀번호 변경")
            print("3. 블랙리스트 등록")
            print("4. 블랙리스트 해제")
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
                uid = input("대상 아이디: ")
                member = self.find_member(uid)
                if member:
                    member.active = False
                    self.save_members()
                    print(f"{member.name}님 블랙리스트 등록 완료")
                else:
                    print("회원 없음")

            elif sel == "4":
                uid = input("대상 아이디: ")
                member = self.find_member(uid)
                if member:
                    member.active = True
                    self.save_members()
                    print(f"{member.name}님 블랙리스트 해제")
                else:
                    print("회원 없음")

            elif sel == "5":
                uid = input("대상 아이디: ")
                member = self.find_member(uid)
                if member:
                    member.role = input("admin/manager/user: ")
                    self.save_members()
                    print("권한이 변경되었습니다.")
                else:
                    print("회원없음")

            elif sel == "9":
                subrun = False

    def show_member_list(self):
        # 관리자가 볼수 있는 회원 리스트
        print("\n[회원 목록]")
        print("-"*60)
        print(f"{'ID':10} {'이름':10} {'이메일':15} {'권한':10} {'상태'}")
        print("-"*60)
        for member in self.members:
            # members리스트에 있는 객체를 하나씩 가져와 member에 넣는다.
            status = "활성" if member.active else "비활성" # True면 status변수에 "활성"을 넣고 아니면 "비활성"
            print(f"{member.id:10} {member.name:10} {member.email:20} {member.role:10} {status}")
            print("-"*60)








