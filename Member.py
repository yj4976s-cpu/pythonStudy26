# 회원관리용 코드를 만든다.
# c -> 회원추가
# r -> 관리자일경우 (전체회원보기), 일반회원(로그인)
# u -> 관리자일경우 (회원차단, 암호변경문의), 일반회원(내정보수정, 암호변경)
# d -> 회원탈퇴

# 메뉴구현
run = True # 프로그램 동작중을 관리하는 변수
login_user = None # 현재 로그인한 사용자 인덱스

menu = """
=====================================
 mbc 아카데미 회원 관리 프로그램
=====================================
 1. 회원가입
 2. 로그인
 3. 회원보기
 4. 내정보수정
 5. 프로그램 종료
 """

# 사용할 리스트 변수를 생성한다. # 회원 데이터
sns = [1, 2] # 사용자 관리번호
ids = ["kkw", "lhj"] # 로그인용 id
passwords = ["1234", "4321"] # 로그인용 pw
names = ["관리자", "임효정"] # 사용자명
emails = ["admin@mbc.com", "lhj@mbc.com"] # 이메일주소
admins = [True, False]  # 관리자 유무 관리자: True, 일반사용자 False

while run:
    print(menu)
    select = input("1 ~ 5 숫자를 입력하세요 : ")
    # =====================================
    # 1. 회원가입
    # =====================================
    if select == "1":
        print("회원가입 메뉴.")

        sn = input("사번: ")
        id = input("아이디: ")

        if id in ids:
            print("이미 존재하는 아이디입니다.")
            continue # 끝나지 않고 상위메뉴로 돌아감

        pw = input("비밀번호 : ")
        name = input("이름 : ")
        email = input("이메일 : ")

        print("\n입력 정보 확인")
        print(f"사번 : {sn}")
        print(f"이름 : {name}")
        print(f"아이디 : {id}")
        print(f"비밀번호 : {pw}")
        print(f"이메일 : {email}")

        if input("가입하시겠습니까? (y/n) : ") == "y":
            sns.append(sn)
            ids.append(id)
            passwords.append(pw)
            names.append(name)
            emails.append(email)
            admins.append(False)
            print("회원가입 완료")
        else:
            print("회원가입 취소")
    # ===============================
    # 2. 로그인
    # ===============================
    elif select == "2":
        print("로그인 메뉴.")

        id = input("아이디 : ")
        pw = input("비밀번호 : ")

        if id in ids:
            idx = ids.index(id)
            if passwords[idx] == pw:
                login_user = idx
                print(f"{names[idx]}님 로그인 성공")

                if admins[idx]:
                    print("> 관리자 계정입니다.")
                else:
                    print("> 일반 회원 계정입니다.")
            else:
                print("비밀번호가 틀렸습니다")
        else:
            print("존재하지 않는 아이디 입니다.")

    # =======================================
    # 3. 회원보기
    # =======================================
    elif select == "3":
        if login_user is None:
            print("로그인 후 이용 가능합니다.")
            continue

        print("회원 정보 보기 메뉴에 진입하였습니다.")

        # 관리자
        if admins[login_user]:
            print("\n[전체 회원 목록]")
            for i in range(len(ids)):
                print(f"{i+1}. {names[i]} | {ids[i]} | {passwords[i]} | {emails[i]} | 관리자: {admins[i]}")

        else:
            # 일반회원
            print("\n[내 정보]")
            print(f"이름 : {names[login_user]}")
            print(f"아이디 : {ids[login_user]}")
            print(f"비밀번호 : {passwords[login_user]}")
            print(f"이메일 : {emails[login_user]}")

    # ==================================
    # 내정보수정
    # ==================================
    elif select == "4":
        if login_user is None:
            print("로그인 후 이용 가능합니다.")
            continue


        print("내정보 수정 페이지 입니다.")
        print("\n내정보 수정")
        print("1. 이름 변경")
        print("2. 이메일 변경")
        print("3. 아이디 변경")
        print("4. 비밀번호 변경")

        choice = input("선택: ")

        if choice == "1":
            names[login_user] = input("새 이름 : ")
            print("이름 변경 완료 : " + names[login_user])

        elif choice == "2":
            emails[login_user] = input("새 이메일 : ")
            print("이메일 변경 완료 : " + emails[login_user])

        elif choice == "3":
            ids[login_user] = input("새 아이디 : ")
            print("아이디 변경 완료 : " + ids[login_user])

        elif choice == "4":
            passwords[login_user] = input("새 비밀번호 : ")
            print("비밀번호 변경 완료 : " + passwords[login_user])

        else:
            print("잘못된 선택")

    # ==========================================
    # 5. 종료
    # ==========================================

    elif select == "5":
         print("회원가입 프로그램이 종료됩니다.")
         run = False

    else:
        print("1~5사이 값을 입력하세요!!!")
