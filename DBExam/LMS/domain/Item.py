class Item:
    # 카테고리 상수 및 리스트정의
    CATEGORY_ETC= "잡화"
    CATEGORY_DRINK = "음료"
    CATEGORY_IT = "IT"
    CATEGORY_BOOK = "도서"

    # 서비스에서 메뉴를 뿌릴 떄 사용할 리스트
    CATEGORIES = [CATEGORY_ETC, CATEGORY_DRINK, CATEGORY_IT, CATEGORY_BOOK]

    def __init__(self,code,name,category,price,stock, id = None , created_at = None):
        self.code = code
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.id = id
        self.created_at = created_at