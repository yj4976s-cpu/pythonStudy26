
import pymysql
# pip install pymysql 터미널 설치 필수
# pip install cryptography mysql 인증문제 해결용

class Session:

    login_member = None

    @staticmethod
    def get_connection(): # 데이터베이스에 연결용 코드
        print("get_connection()메서드 호출 - mysql에 접속됩니다.")

        return pymysql.connect(
            host='192.168.0.171',
            user='yjs',
            password='2345',  # 본인의 비밀번호로 변경
            db='DATA',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            # dict 타입으로 처리함 (딕셔너리타입 k : v )
        )

    @classmethod
    def login(cls, member): #  MemberService에서 로그인시 객체를 담아놈
        cls.login_member = member

    @classmethod
    def logout(cls):  # 로그아웃 기능 (세션에 있는 객체를 None 처리함)
        cls.login_member = None

    @classmethod
    def is_login(cls): # 로그인 상태를 확인
        return cls.login_member is not None
        # 로그인 했으면 True / None False

    # 추가: 권한 체크 메서드 (서비스 계층에서 사용됨)
    @classmethod
    def is_admin(cls):  # 로그인한 객체가 admin이냐??
        return cls.is_login() and cls.login_member.role == "admin"
        #     로그인 했고 role이 admin이면 True / None False

    @classmethod
    def is_manager(cls):
        # 매니저이거나 어드민이면 참 (보통 어드민이 매니저 권한을 포함함)
        return cls.is_login() and cls.login_member.role in ("manager", "admin")