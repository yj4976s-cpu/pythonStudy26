class Board:
    def __init__(self, id, title, content, member_id, active=True, writer_name=None, writer_uid=None, created_at=None):
        self.id = id  # DB의 PK
        self.title = title
        self.content = content
        self.member_id = member_id  # 작성자의 고유 번호(FK)
        self.active = active  # 삭제 여부 (boolean 1/0)

        # JOIN을 통해 가져올 추가 정보들 (선택 사항)
        self.writer_name = writer_name
        self.writer_uid = writer_uid
        self.created_at = created_at

    @classmethod
    def from_db(cls, row: dict):
        # db에 있는 내용의 1줄을 dict타입으로 가져와 객체로 만듬
        if not row: return None
        return cls(
            id=row.get('id'),
            title=row.get('title'),
            content=row.get('content'),
            member_id=row.get('member_id'),
            active=bool(row.get('active')),
            # JOIN 쿼리 시 사용할 이름과 아이디
            writer_name=row.get('writer_name'),
            created_at=row.get('created_at'),
            writer_uid=row.get('writer_uid')
        )
