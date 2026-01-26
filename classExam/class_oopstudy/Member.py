class Member: # 클래스는 무조건 대문자
    def __init__(self, uid, pw, name, role = "user", active = True):
        self.id = uid
        self.pw = pw
        self.name = name
        self.role = role
        self.active = active

        # 파일 저장용 문자열 변환
    def to_line(self):
        return f"{self.id}|{self.pw}|{self.name}|{self.role}|{self.active}\n"

    @classmethod # 객체(self)가 아니라 클래스 자체를 다루는 메서드
    def from_line(cls, line): # line: 메모장의 1줄 문자열
        uid,pw,name,role,active = line.strip().split("|")

        return cls(uid,pw,name,role,active == "True")
