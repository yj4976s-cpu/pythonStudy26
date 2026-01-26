class Member:

    # member = Member("id","pw","name","role")
    def __init__(self, uid, pw, name, role="user", active=True):
        # 객체가 생성될때 초기값 처리함
        self.uid = uid
        self.pw = pw
        self.name = name
        self.role = role  # (admin / manager / user)
        self.active = active


    def __str__(self):  # print(member) 처리되는용 (테스트용)
        status = "활성" if self.active else "비활성"
        return f"{self.uid}|{self.name}|{self.role}|{status}"


    def to_line(self):
        # 파일 저장용 (직렬화) : 메모리에 있는 객체를 메모장으로 저장할 문자열로 변환
        return f"{self.uid}|{self.pw}|{self.name}|{self.role}|{self.active}"


    @staticmethod  # 객체가 아니라 문자열 처리!!! -> session.py에 @classmethod 처리함
    def from_line(line: str):
        uid, pw, name, role, active = line.strip().split("|")
        return Member(
            uid=uid,
            pw=pw,
            name=name,
            role=role,
            active=(active == "True")
        )


    def is_admin(self):
        return self.role == "admin"


    def is_manager(self):
        return self.role == "manager"