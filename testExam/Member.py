
class Member:
    def __init__(self, uid, pw, name, email, role="user",active=True):
        self.id = uid
        self.pw = pw
        self.name = name
        self.email = email
        self.role = role
        self.active = active

    def to_line(self): # 파일저장용 문자열 변환
        return f"{self.id}|{self.pw}|{self.name}|{self.email}|{self.role}|{self.active}\n"

    # 파일에서 불러온 내용 객체처리
    @classmethod # 객체가 아닌 클래스(cls)를 다루는 메서드정의
    def from_line(cls, line):
        uid, pw, name, email, role, active = line.strip().split("|")
        return cls(uid, pw, name, email, role, active == "True")


