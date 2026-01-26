# 프로그램에서 사용될 변수들
# 전역변수(global) -> py 파일 안에서 전체적으로 사용되는 변수
# 지역변수(local) -> while, if, for, def안에서 사용되는 변수

run = True
session = None # 로그인한 사용자의 리스트 인덱스 기억용

# 프로그램에서 사용될 리스트들
ids = ["admin","manager","user"]
pws =["1234", "5678", "6789"]
names = ["관리자","팀장","일반 사용자"]
roles = ["admin","manager","user"]
active = [True, True, True] # 회원사용중, 탈퇴, 중지, 블랙리스트..

def member_add():
    print("회원가입")
    new_id = input("아이디 : ")
    if new_id in ids: # 이미 있는 아이디인지 점검
        print("존재하는 아이디 입니다.")
        return
    else:
        new_pw = input("비밀번호 : ")
        new_name = input("이름 : ")
        member_add_menu() # 회원권한 메뉴를 불러 권한설정

        role_set = input("권한 선택 : ")
        if role_set == 1 :
            new_role = "admin"
        elif role_set == 2:
            new_role = "manager"
        else:
            new_role = "user"
        print(f"""
입력한 정보 확인
이름 : {new_name}
아이디 : {new_id}
비밀번호 : {new_pw}
권한 : {new_role}
""")

        save_select = input("저장을 누르려면 y: ")
        if save_select == "y" :
            ids.append(new_id)
            pws.append(new_pw)
            names.append(new_name)
            roles.append(new_role)
            active.append(True)
            print("저장완료")

        else:
            print("회원가입 취소")

def member_login():
    print("로그인")

    global session # 전역변수로 지정한 내용 활용

    if session is not None:
        print("이미 로그인 한 상태입니다.")
        print(f"로그인한 사용자는 {names[session]} 님 입니다.")
        return
    else:

        user_id = input("로그인 ID : ")
        user_pw = input("비밀번호 : ")

        if user_id in ids:  # 키보드로 받은 id를 ids 리스트에 있는지?
            # True 있으면
            idx = ids.index(user_id)
            if not active[idx]:  # 회원 활성화 상태인지?
                # False
                print("비활성화/차단된 계정입니다.")
                return
            else:
                if user_pw == pws[idx]:
                    session = idx
                    role = roles[idx] # role을 변수로 넣어 roles[idx]를 불러옴

                    print(f"{user_id}님 환영합니다.")
                    print(f"{roles[idx]}권한을 가지고 있습니다.")
                    if role == "admin": # 관리자로 로그인시 관리자메뉴를 따로 뜨게함
                        member_admin()
                else:
                    print("비밀번호가 틀렸습니다.")
        else:
            print("존재하지 않는 아이디")

def member_admin():
    print("관리자사용메뉴")
    print("1. 회원 비밀번호 변경")
    print("2. 회원 블랙리스트 처리")
    print("3. 회원 권한 변경")
    print("4. 종료")

    select = input("선택 : ")

    if select == "1" :
        uid = input("대상 아이디: ")
        if uid in ids:
            idx = ids.index(uid)
            pws[idx] = input("새로운 비밀번호: ")
            print("비밀번호 변경이 완료되었습니다.")

    elif select == "2" :
        uid = input("대상 아이디: ")
        if uid in ids:
            idx = ids.index(uid)
            active[idx] = False # 계정 비활성화와 비슷하게 써서 블랙리스트계정을 강제 비활성화
        print("블랙리스트를 처리하였습니다.")

    elif select == "3" :
        uid = input("대상 아이디: ")
        if uid in ids:
            idx = ids.index(uid)
            print("admin/manager/user")
            roles[idx] = input("새로운 권한 : ")
            print("회원의 권한이 변경되었습니다.")

def member_logout():
    global session
    if session is None:
        print("로그인이 되어있지 않습니다")
    else:
        print(f"{names[session]}님이 로그아웃 하셨습니다.")
        session = None # None을 써서 로그인이 안된상태로 돌아감

def member_modify():
    if session is None:
        print("로그인 후 이용하세요")
        return
    print("나의 정보 수정")
    print("1. 이름 변경")
    print("2. 아이디 변경")
    print("3. 비밀번호 변경")

    select = input("선택: ")
    if select == "1" :
        names[session] = input("새로운 이름: ")
        print("이름이 변경되었습니다.")
    elif select == "2" :
        ids[session] =  input("새로운 아이디: ")
        print("아이디가 변경되었습니다.")

    elif select == "3" :
        pws[session] = input("새로운 비밀번호: ")
        print("비밀번호가 변경되었습니다.")

def member_delete():
    global session
    if session is None:
        print("로그인 후 이용하세요")
        return
    print("회원탈퇴/비활성화")
    print("1. 계정 비활성화")
    print("2. 회원탈퇴")

    select = input("선택 : ")

    if select == "1" :
        active[session] = False # 비활성화를 위해 사용중이거나 활성중인 세션종료
        session = None
        print("비활성화가 완료되었습니다.")

    elif select == "2" :
        ids.pop(session)
        pws.pop(session)
        names.pop(session)
        active.pop(session)
        session = None
        print("탈퇴가 완료되었습니다")

def main_menu():
    print(f"""
======엠비씨 아카데미 회원관리프로그램입니다.=======
1. 회원가입
2. 로그인
3. 로그아웃
4. 회원정보수정
5. 회원탈퇴
6. 프로그램 종료
""")

def member_add_menu(): # 회원가입 권한 설정메뉴
    print(f"""
--------회원권한선택--------
1. 관리자
2. 팀장
3. 일반사용자
""")

# 프로그램 시작
while run :
    main_menu()
    select = input(">>>")
    if select == "1" :
        member_add()

    elif select == "2" :
        member_login()

    elif select == "3" :
        member_logout()

    elif select == "4" :
        member_modify()

    elif select == "5" :
        member_delete()

    elif select == "6" :
        run = False

    else:
        print("잘못된 입력입니다.")
