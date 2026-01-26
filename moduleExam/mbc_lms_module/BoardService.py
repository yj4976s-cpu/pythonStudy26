
class BoardService:
    def __init__(self):
        boards = []
    def run(self):
        subrun = True
        while subrun:
            print("""
-------------------------
1. 자료업로드
2. 자료목록
3. 자료검색
4. 공지사항

9. 자료게시판 서비스종료
""")
            subSelect = input(">>>")
            if subSelect == "1":
                print("자료업로드 메서드 호출")


            elif subSelect == "2":
                print("자료목록 호출")

            elif subSelect == "3":
                print("자료검색 메서드 호출")

            elif subSelect == "4":
                print("공지사항 메서드 호출")

            elif subSelect == "9":
                print("성적관리서비스 종료")
                subrun = False

            else:
                print("잘못된 메뉴를 선택하였습니다.")


