class ScoreService:

    def __init__(self):
        scores = []
    def run(self):
        subrun = True
        while subrun:
            print("""
-------------------------
1. 성적입력
2. 학생목록
3. 학생 성적조회
4. 성적수정
5. 성적삭제

9. 성적관리 서비스종료
""")
            subSelect = input(">>>")
            if subSelect == "1":
                print("성적입력 메서드 호출")

            elif subSelect == "2":
                print("학생목록 메서드 호출")

            elif subSelect == "3":
                print("학생성적조회 메서드 호출")
            elif subSelect == "4":
                print("학생성적삭제 메서드 호출")

            elif subSelect == "9":
                print("성적관리서비스 종료")
                subrun = False

            else:
                print("잘못된 메뉴를 선택하였습니다.")

