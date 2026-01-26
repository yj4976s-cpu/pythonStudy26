# 상품에 대한 crud를 구현해보자
# C -> 새상품 등록
# R -> 전체상품 목록
# R -> 단일상품 자세히보기
# U -> 상품 수정
# D -> 상품 품절(매진)


# 사용할 변수 전역변수(상품 DB역할)
run = True

item_names = ["노트북", "모니터"] # 상품명
unit_prices = [1200000, 400000] # 단가
quantity = [40, 25] # 수량
product_info = ["AI용 삼성노트북", "LG24인치 LED"] # 상품 정보
category = ["가전", "잡화"] # 상품분류

# --------------------
# C : 새 상품 등록
# ---------------------

# 사용할 함수(메서드)
def new_item():
    # 새상품 추가용 실행문
    # print("new_item() 함수 호출 완료") # 나중에 주석처리해도 됨
    print("\n[새로운 상품 등록]")

    name = input("상품명: ")
    price = int(input("단가: ")) # input은 입력하면 문자로 나오기 때문에 int로 감싸줌
    qty = int(input("수량: "))
    info = input("상품 설명: ")

    item_add_menu() # 밑의 카테고리 선택을 위해 item 메뉴를 다시 보여준다.

    cat_num = input("카테고리 선택: ") # 카테고리 선택 입력을 넣어 번호마다 카테고리를 다르게 설정한다.

    if cat_num == "1":
        cat = "교재"
    elif cat_num == "2":
        cat = "잡화"
    elif cat_num == "3":
        cat = "음식"
    elif cat_num == "4":
        cat = "패션"
    elif cat_num == "5":
        cat = "가전"
    else:
        print("잘못된 카테고리 선택")
        return

    item_names.append(name) # 상품등록이 끝나면 append로 불러와 등록을 완료한다.
    unit_prices.append(price)
    quantity.append(qty)
    product_info.append(info)
    category.append(cat)

    print("상품등록이 완료되었습니다.")

# -----------------------------
# R : 전체 상품 목록
# -----------------------------

def item_list():
    # print("item_list() 함수 호출 완료")
    print("\n[상품목록]")
    print("번호 | 상품명 | 가격 | 수량 | 카테고리")
    print("-"*40) # *로 -를 40개 출력

    # 리스트 출력용 for item in item names:
    for i in range(len(item_names)):
        print(f"{i}| {item_names[i]} | {unit_prices[i]} | {quantity[i]} | {category[i]}")

# ------------------------------
# R : 상품 상세 보기
# ------------------------------
# 상품에 대한 상세정보 표시

def item_view():
    # print("item_view() 함수 호출 완료")
    item_list()
    idx = int(input("\n상세 조회할 상품 번호 : "))

    if 0 <= idx < len(item_names): # 0 <= idx : 0부터 시작하는 인덱스가 음수가되면 안됨
                                    # idx < len(item_names): 인덱스는 리스트의 개수보다 항상 작아야함 인덱스는 1이아니라 0부터 시작하기 때문
        print("\n[상품 상세정보]")
        print("상품명: ", item_names[idx])
        print("가격: ", unit_prices[idx])
        print("수량: ", quantity[idx])
        print("카테고리: ", category[idx])
        print("설명: ", product_info[idx])
    else:
        print("존재하지 않는 상품입니다.")

# -----------------------------
# U : 상품 수정
# -----------------------------

# 상품에 대한 내용 수정하기
def item_update():
    # print("item_update() 함수 호출 완료")
    item_list()
    idx = int(input("\n수정할 상품 번호: "))

    if 0 <= idx < len(item_names):
        print("수정하지 않으려면 Enter")

        name = input(f"상품명({item_names[idx]}): ")
        price = input(f"가격({unit_prices[int(idx)]}): ")
        qty = input(f"수량({quantity[int(idx)]}): ")
        info = input(f"설명({product_info[idx]}): ")

        if name: # 수정하지 않으면 Enter쳐서 넘어가라고 써놓아서 else는 안써도됨
            item_names[idx] = name
        if price:
            unit_prices[int(idx)] = int(price)
        if qty:
            quantity[int(idx)] = int(qty)
        if info:
            product_info[idx] = info

        print("상품 수정완료")
    else:
        print("존재하지 않는 상품입니다.")

# ---------------------------
# D : 상품 품절 처리
# ---------------------------
# 상품 품절, 삭제하기
def item_delete():
    # print("item_delete() 함수 호출 완료")
    item_list()
    idx = int(input("\n품절 처리할 상품 번호: "))

    if 0 <= idx < len(item_names):
        quantity[idx] = 0
        print(f"[{item_names[idx]}] 상품이 품절되었습니다.")
    else:
        print("존재하지 않는 상품입니다.")


def main_menu():
    print("""
=================================
엠비씨 아카데미 쇼핑몰 입니다.

1. 상품등록
2. 상품목록
3. 상품 상세보기
4. 상품 수정하기
5. 상품 삭제하기

9. 프로그램 종료
    """)

def item_add_menu():
    print("""
======상품 추가용 메뉴에 진입======
1. 교재
2. 잡화
3. 음식
4. 패션
5. 가전

9. 종료
    """)

# 프로그램 주실행 코드 시작
while run :
    main_menu() # 메인메뉴 함수 호출하여 출력

    select = input("숫자입력 : ")
    if select == "1":
        item_add_menu() # 아이템 추가용 메뉴 함수
        new_item() # 아이템 추가용 코드

    elif select == "2":
        item_list()
    elif select == "3":
        item_view()
    elif select == "4":
        item_update()
    elif select == "5":
        item_delete()
    elif select == "9":
        run = False

    else:
        print("잘못된 숫자를 입력하셨습니다.")
        print("다시 입력하세요!!!")



