# 대부분 프로그래밍에서 1번이 되는(start) 파일을 main으로 만듬
# 목표 : MBC아카데미 LMS 프로그램을 만들어 보자.
# 회원관리 : 시스템담당자, 교수, 행정, 학생, 손님, 학부모
# 성적관리 : 교수가 성적등록, 수정,
#           행정담당자가 학기마다 백업(이전->삭제)
#           학생은 개인성적일람, 성적출력
#           손님은 학교소개페이지 열람
#           학부모는 자녀학사관리
#  게시판 : 회원제, 비회원제, 문의사항, Q/A

# 필요한 변수
run = True # 메인 메뉴용 while
# subRun = True # 보조 메뉴용 while
session = None # 로그인한 사용자의 인덱스를 기억

# 필요한 리스트
# 회원에 대한 리스트
sns = [1] # 회원에 대한 번호
ids = ["admin"] # id에 대한 리스트
pws = ["1234"]  # 암호에 대한 리스트
groups = ["admin"] # 회원등급

# admin (관리자), stu(학생), guest(손님)

# 성적에 대한 리스트
pythonScore = [] # 파이썬 점수들
dbScore = [] # 데이터베이스 점수들
webScore = [] # 프론트 점수들
totalScore = []   # 총점 들
avgScore = [] # 평균 들
gradeScore = [] # 등급 들
stuIdx = [] # 학생의 인덱스(학번) <-> 회원의 sns

# 게시판에 대한 리스트
board_no = [] # 게시물의 번호
board_title = [] # 게시물의 제목
board_content = [] # 게시물의 내용
board_writer = [] # 게시물 작성자 <-> 회원의 sns

# 메뉴 구성
mainMenu = """
=============================
엠비씨 아카데미 LMS에 오신걸 환영합니다.

1. 로그인
2. 성적관리
3. 게시판
4. 관리자메뉴
9. 프로그램 종료

"""


memberMenu = """
-------------------------------
회원관리 메뉴입니다.

1. 로그인
2. 회원가입
3. 회원수정
4. 회원탈퇴
9. 회원관리 메뉴 종료

"""

scoreMenu = """
--------------------------------
성적관리 메뉴입니다.

1. 성적입력(교수전용)
2. 성적보기(학생용)
3. 성적수정(교수전용)
4. 성적백업(행정직원전용)
9. 뒤로가기
"""


boardMenu = """
----------------------------------
회원제 게시판 입니다.

1. 글쓰기
2. 글목록
3. 게시글 자세히 보기
4. 게시글 수정하기
5. 게시글 삭제하기
6. 게시글 검색
9. 뒤로가가
"""

adminMenu = """
------------------------------------
관리자 메뉴
1. 회원목록
2. 회원강제삭제
9. 뒤로가기
"""

# ======================================
# 메인 루프
# ======================================
while run:
    print(mainMenu) # 메인메뉴 출력용
    select = input(">>>") # 사용자가 주메뉴선택 값을 select 넣는다.

    # =======================================
    # 1. 로그인/회원가입
    # =======================================

    if select == "1":
        print("로그인메뉴로 진입합니다.")
        subRun = True
        while subRun: # 부메뉴 반복용
            print(memberMenu) # 회원관리 메뉴가 출력
            sub = input(">>>") # 회원 부메뉴 선택값을 subSelect에 넣음

         #   -----로그인------
            if sub == "1":
                uid = input("ID: ")
                upw = input("PW: ")

                if uid in ids:
                    idx = ids.index(uid)
                    if pws[idx] == upw:
                        session = idx
                        print(f"로그인 성공/ 권한 : {groups[idx]}") # f"를 사용하여 groups를 불러오기
                        subRun = False
                    else:
                        print("비밀번호 오류")
                else :
                    print("존재하지 않는 ID")

            elif sub == "2":
                print("회원가입메뉴로 진입합니다.")
                uid = input("새 ID: ")
                if uid in ids:
                    print("이미 존재하는 ID")
                    continue

                upw = input("PW: ")

                # =======ROLE 분기==========
                if session is None:
                    print("회원 유형 선택")
                    print("1. 학생")
                    print("2. 부모")

                    r = input("선택 : ")
                    if r == "1":
                        role = "stu"
                    elif r == "2":
                        role = "parent"
                    else:
                        print("잘못된 선택")
                        continue

                elif groups[session] == "admin":
                    print("권한 선택")
                    print("1. 관리자(admin)")
                    print("2. 교수(prof)")
                    print("3. 행정(staff)")
                    print("4. 학생(stu)")
                    print("5. 부모(parent)")

                    role_map = {
                        "1": "admin", # 관리자들의 선택번호별 역할을 딕셔너리로 정의
                        "2": "prof",
                        "3": "staff",
                        "4": "stu",
                        "5": "parent"
                    }

                    r = input("선택:")
                    if r in role_map:
                        role = role_map[r]
                    else:
                        print("잘못된 선택")
                        continue
                else:
                    print("관리자만 회원의 추가가 가능합니다.")
                    continue

                sns.append(len(sns)+1)
                ids.append(uid)
                pws.append(upw)
                groups.append(role)

                print(f"회원가입 완료 (권한:{role})")

            elif sub == "3":
                print("회원 수정 메뉴로 진입합니다.")
            elif sub == "4":
                print("회원 탈퇴 메뉴로 진입합니다.")
            elif sub == "9":
                print("회원 관리 메뉴를 종료합니다.")
                subRun = False # 회원 while문 종료

            else : # 1,2,3,4,9 말고 다른 키를 넣을 경우
                print("잘못된 메뉴를 선택하였습니다.")

        # ===========================
        # 2. 성적관리
        #============================

    elif select == "2":
        if session is None:
            print("로그인이 필요합니다.")
            continue

        subRun = True
        while subRun:
            print(scoreMenu)
            sub = input(">>>")
            # 성적입력(교수만)
            if sub == "1":
                if groups[session] != "prof": # 교수가 groups[session]에 없다면
                    print("교수만 입력 가능")
                    continue

                sid = int(input("학생 회원번호 : ")) # 숫자가 문자로 입력되지 않기위해 int로 감싼다
                py = int(input("Python: "))
                db = int(input("DB: "))
                web = int(input("Web: "))
                stuIdx.append(sid)
                pythonScore.append(py)
                dbScore.append(db)
                webScore.append(web)
                print("성적 입력 완료")

                # 성적보기(학생)
            elif sub == "2":
                if groups[session]!= "stu":
                    print("학생만 조회가능")
                    continue

                myNo = sns[session]
                if myNo in stuIdx:
                    i = stuIdx.index(myNo)
                    total = pythonScore[i] + dbScore[i] + webScore[i]
                    avg = total / 3
                    if avg >= 90:
                        grade = "A"
                    elif avg >= 80:
                        grade = "B"
                    elif avg >= 70:
                        grade = "C"
                    else:
                        grade = "F"

                    print("====내 성적====")
                    print("python: ", pythonScore[i])
                    print("DB: ", dbScore[i])
                    print("web: ", webScore[i])
                    print("평균 : ", avg)
                    print("총점 : ", total)
                    print("등급 : ", grade)
                else:
                    print("등록된 성적이 없습니다.")

            elif sub == "9":
                subRun = False

    # ======================
    # 3. 게시판
    # =====================

    elif select == "3":
        if session is None:
            print("로그인이 필요합니다.")
            continue

        subrun = True
        while subRun:
            print(boardMenu)
            sub = input(">>>")

            if sub == "1":
                title = input("제목 : ")
                content = input("내용 : ")

                board_no.append(len(board_no)+1)
                board_no.append(title)
                board_no.append(content)
                board_writer.append(sns[session])
                print("게시글 등록 완료")

            elif sub == "2":
                print("번호|제목|작성자")
                for i in range(len(board_no)):
                    print(board_no[i], board_title[i], board_writer[i])

            elif sub == "9":
                subRun = False
    # ===============
    # 4. 관리자 메뉴
    # ================
    elif select == "4":
        if session is None :
            print("관리자만 접근 가능")
            continue

    elif select == "9":
        print("프로그램 종료")
        run = False
    else:
        print("잘못된 선택")




