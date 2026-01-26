# while문 : run, Subrun
# if문 : 메뉴 선택이나, 판단용
# for문 : 리스트에 있는 전체내용 출력용
# for in : 리스트에 있는 내용 인덱스 찾는 용

run = True
session = None
users = {"admin": {"passwords": "1234","role": "ADMIN"}, "seller": {"role": "SELLER"},"user1": {"role" : "user", "grade" : "NORMAL"}, "user2" :{"role": "USER", "grade": "VIP"}}
# 딕셔너리를 이용해 일반사용자는 Normal,vip로 등급을 나눔
products = {"콜라": {"price": 1500, "stock":10}, "사이다": {"price": 1400, "stock":10}, "커피" : {"price": 2000, "stock": 10}}
discount = {"ADMIN" : 0.20, "SELLER" : 0.10, "USER" : {"NORMAL": 0.00,"VIP": 0.15}}


mainMenu = """
=============================
자판기 메인메뉴(일반)
1. 로그인
2. 회원가입
3. 상품목록
4. 상품찾기
5. 프로그램 종료

==============================

"""


mainMenu_seller = """
==============================
자판기 메인 메뉴(판매자)

1. 나의 상품관리
2. 상품목록
3. 로그아웃
4. 종료
===============================

"""

mainMenu_admin = """
--------------------------------
자판기 메인 메뉴(관리자)

1. 판매자/상품 관리
2. 상품목록
3. 사용자 등급변경(VIP/NORMAL)
4. 할인율 변경
5. 로그아웃
6. 종료
"""

while run:
    print(mainMenu)
    select = input(">>>")
         # 양쪽공백없이 쓰기위해 strip함수사용
    if select == "1":
        uid = input("ID: ")
        upw = input("PW: ")
        login_success = False

        if uid["id"] == uid and users[uid]["password"] == upw:
            session = {"id": uid, "role": users[uid]["role"]}
            if users[uid]["role"] == "USER":
                session["grade"] = users[uid].get("grade","NORMAL") # 키로 등급값을 가져오기위해 get함수를 이용
                print(f"로그인 성공 ID = {session['id']} / ROLE={session['role']}")

                if session["role"] == "USER":
                    print("등급:", session["grade"])
        else:
                print("아이디 혹은 비밀번호 오류")

    elif select == "2": # 판매자와 사용자 회원가입
        uid = input("새 ID: ")
        if uid in users:
            print("존재하는 ID")
        else:
            upw = input("새 PW: ")

            print("1) 판매자(SELLER)")
            print("2) 일반사용자(USER)")
            select = input("가입 유형 선택").strip()
            if select == "1":
                users[uid] = {"password": upw, "role": "SELLER"}
                print("판매자 화원가입 완료")
            elif select == "2":
                users[uid] = {"password": upw, "role": "USER", "grade": "NORMAL"}
                print("일반사용자 회원가입 완료")
            else:
                print("잘못된 선택")

    elif select == "3":
        print("상품목록입니다")
        rate = 0
        if session is None:
            role = session["role"]
            if role == "USER":
                grade = session.get("grade","NORMAL")
                rate = discount["User"][grade]
        else:
            rate = discount[role]



    elif select == "5":
        print("자판기 종료")
        run = False
    else:
        print("선택이 잘못되었습니다")





