import os

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from DATA.common import Session
from DATA.domain.Board import Board
from DATA.domain.Score import Score
from DATA.service import PostService

app = Flask(__name__)
app.secret_key = 'you_secret_key'
# 세션을 사용하기 위해 보안키 설정 (아무 문자열이나 입력)

@app.route('/login', methods=['GET','POST'])

def login():
    if request.method == 'GET': # 처음접속하면 GET방식으로 회면 출력용
        return render_template('login.html')
        # get방식으로 요청하면 login.html 화면이 나옴

    # login.html에서 action="/login" method="POST"처리용 코드
    # login.html에서 넘어온 폼 데이터는 uid / upw
    uid = request.form.get('uid') # 요청한 폼내용을 가져온다
    upw = request.form.get('upw') # request form get
    # print("/login에서 넘어온 폼 데이터 출력 테스트")
    # print(uid,upw)
    # print("====================================")

    conn = Session.get_connection() #  db에 접속용 객체
    try : # 예외발생 가능성 있음
        with conn.cursor() as cursor: # db에 커서객체 사용

            sql = """select id,name, uid, role 
            From members
            where uid = %s AND password = %s"""
            #                   uid가 동일 & pwd가 동일
            #   id, name, uid, role을 가져온다.
            cursor.execute(sql, (uid, upw)) # 쿼리문 실행
            user = cursor.fetchone()  # 쿼리 결과 1개를 가져와 user 변수에 넣음

            if user:
                # 찾은 계정이 있으면 브라우져의 세션영역에 보관한다.
                session['user_id'] = user['id'] # 계정일련번호(회원번호)
                session['user_name'] = user['name'] # 계정이름
                session['user_uid'] = user['uid'] # 계정로그인명
                session['user_role'] = user['role'] # 계정권한
                # 세션에 저장완료
                # 브라우저에서 f12번 누르고 애플리케이션 탭에서 쿠키 항목에 가면 session객체가 보임
                # 이것을 삭제하면 로그아웃 처리 됨
                return redirect(url_for('index'))
                # 처리후 이동하는 경로 http://localhost:/index로 감(get 메서드 방식)

            else:
                # 찾은 계정이 없다.
                return "<script>alert('아이디 혹은 비밀번호가 틀렸습니다.');history.back();</script>"
            #                   경고창발생                         뒤로가기

    finally:
        conn.close() # db 연결 종료

@ app.route('/logout') # 기본동작이 get방식이라, methods =['GET'] 생략가능
def logout():
    session.clear() # 세션 비우기
    return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST']) # 회원가입용 함수
def join(): # http:localhost:5000/ get메서드(화면출력) post(화면폼처리용)
    if request.method == 'GET': # 로그인화면용 프론트로 보냄
        return render_template('join.html')

    # POST 메서드 인 경우 (폼으로 데이터가 넘어올때 처리)
    uid = request.form.get('uid')
    password = request.form.get('password')
    name = request.form.get('name') # 폼에서 넘어온 값을 변수에 넣음

    conn = Session.get_connection() # db에 연결
    try: # 예외발생 가능성이 있는 코드
        with conn.cursor() as cursor:
            cursor.execute("select * from members where uid = %s;", (uid,))
            if cursor.fetchone():
                return"<script>alert('이미 존재하는 아이디입니다.');history.back();</script>"

            # 회원 정보 저장 (role,active는 기본값이 들어감)
            sql = "INSERT INTO members (uid, password, name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (uid, password, name))
            conn.commit()

            return "<script>alert('회원가입이 완료되었습니다!'); location.href = '/login';</script>"

    except Exception as e: # 예외발생시 실행문
        print(f"회원가입 에러: {e}")
        return "가입 중 오류가 발생했습니다. /n join()메서드를 확인하세요!!!"

    finally: # 항상 실행문
        conn.close()

@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if 'user_id' not in session: # 세션에 user_id가 없으면
        return redirect(url_for('login')) # 로그인 경로로 보냄

    # 있으면 db연결 시작!
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                # 기존 정보 불러오기
                cursor.execute("select * from members where id = %s;", (session['user_id'],))
                user_info = cursor.fetchone()
                return render_template('member_edit.html', user=user_info)
                #                      가장 중요한 포인트   get요청시 페이지      객체전달용 코드
            # POST 요청: 정보 업데이트
            new_name = request.form.get('name')
            new_pw = request.form.get('password')

            if new_pw: # 비밀번호 입력 시에만 변경
                sql = "update members set name = %s, password = %s where id = %s"
                cursor.execute(sql, (new_name, new_pw, session['user_id'],))
            else: # 이름만 변경
                sql =  "UPDATE members SET name = %s WHERE id = %s"
                cursor.execute(sql, (new_name, session['user_id'],))

            conn.commit()
            session['user_name'] = new_name # 세션 이름정보도 갱신
            return "<script>alert('정보가 수정되었습니다.'); location.href='/mypage';</script>"


    except Exception as e: # 예외발생시 실행문
        print(f"회원수정 에러:{e}")
        return "수정 중 오류가 발생했습니다. /n member_edit()메서드를 확인하세요!!!"

    finally: # 항상 실행문
        conn.close()

@app.route('/mypage')
def mypage():
    if 'user_id' not in session: # 로그인상태인지 확인
        return redirect(url_for('login'))
    conn = Session.get_connection() # db연결
    try:
        with conn.cursor() as cursor:
            # 내 상세 정보 조회
            cursor.execute("select * from members WHERE id = %s;", (session['user_id'],))
            # 로그인한 정보를 가지고 db에서 찾아온다
            user_info = cursor.fetchone()


            cursor.execute("select count(*) as board_count From boards WHERE member_id = %s;", (session['user_id'],))
            #                                                   board 테이블에 조건 member_id값을 가지고 찾아옴
            #                       개수를 세어 fetchone()넣음 -> board_count 이름으로 개수를 가지고 있음

            board_count = cursor.fetchone()['board_count']
            return render_template('mypage.html', user=user_info, board_count=board_count)
            # 결과를 리턴한다.                         mypage.html 에게 user객체와 board_count객체를 담아 보냄
            # 프론트에서 사용하려면 {{ user.????}}    {{ board_count }}
    finally:
        conn.close()

@app.route('/mypage/member/delete', methods= ['POST'])
def mypage_member_delete():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1) 성적(자식) 삭제
            cursor.execute(
                "DELETE FROM scores WHERE member_id = %s;",
                (session['user_id'],))


            # 2) 게시글(자식) 삭제
            cursor.execute(
                "DELETE FROM boards WHERE member_id = %s;",
                (session['user_id'],))

            # 3) 파일 게시판 첨부파일(자식) 삭제
            cursor.execute("""
                SELECT a.save_name
                FROM attachments a
                JOIN posts p ON a.post_id = p.id
                WHERE p.member_id = %s
            """, (user_id,))
            files = cursor.fetchall()

            for f in files:
                file_path = os.path.join(UPLOAD_FOLDER, f["save_name"])
                if os.path.exists(file_path):
                    os.remove(file_path)

            # 3) 회원(부모) 삭제
            cursor.execute(
                "DELETE FROM members WHERE id = %s;",
                (session['user_id'],)
            )


            conn.commit()
            session.clear()
            return "<script>alert('회원 탈퇴 완료'); location.href='/'</script>"
    finally:
        conn.close()

@ app.route('/board/my')
def board_my():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 나의  ID로만 조회
            sql = "SELECT * FROM boards WHERE member_id = %s"
            cursor.execute(sql, (session['user_id'],))
            rows = cursor.fetchall()
            print(rows) # dict 타입으로 결과물 들어옴
            boards =  [Board.from_db(row) for row in rows]

            return render_template('board_my.html', boards=boards)
    finally:
        conn.close()

############################# 회원 끝 ################################
########################### 게시판 ###################################
@app.route('/board/write', methods=['GET', 'POST'])
def board_write():
    # 1. 사용자가 '글쓰기' 버튼을 눌러서 들어왔을 때 (화면 보여주기)
    if request.method == 'GET':
        # 로그인 체크 (로그인 안 했으면 글 못쓰게)
        if 'user_id' not in session:
            return '<script>alert("로그인 후 이용 가능합니다."); location.href="/login";</script>'
        return render_template('board_write.html')
        # 2. 사용자가 '등록하기' 버튼을 눌러서 데이터를 보냈을 때(DB 저장)

    elif request.method == 'POST':
        print("POST 들어옴!", request.form)
        title = request.form.get('title')
        content = request.form.get('content')
        # 세션에 저장된 로그인 유저의 id(member_id)
        member_id = session.get('user_id')

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO boards (member_id, title, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (member_id, title, content))
                conn.commit()
            return redirect(url_for('board_list')) # 저장 후 목록으로 이동

        except Exception as e:
            print(f"글쓰기 에러: {e}")
            return "저장 중 에러가 발생했습니다."

        finally:
            conn.close()

# 1. 게시판 목록 조회
@ app.route('/board')
def board_list():
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 작성자 이름을 함께 가져오기 위해 JOIN 사용
            sql = """
                SELECT b.*, m.name as writer_name
                FROM boards b
                JOIN members m ON b.member_id = m.id
                ORDER BY b.id DESC
                """
            cursor.execute(sql)
            rows = cursor.fetchall()
            boards = [Board.from_db(row) for row in rows]
            return render_template('board_list.html', boards=boards)
    finally:
        conn.close()

# 2. 게시글 자세히 보기
@app.route('/board/view/<int:board_id>')
def board_view(board_id):
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # JOIN을 통해 작성자 정보(name, uid)를 함께 조회
            sql = """
                SELECT b.*, m.name as writer_name, m.uid as writer_uid
                FROM boards b
                JOIN members m ON b.member_id = m.id
                WHERE b.id = %s
            """
            cursor.execute(sql, (board_id,))
            row = cursor.fetchone()
            print(row) # db에서 나온 dict타입 콘솔에 출력 테스트용

            if not row:
                return "<script>alert('존재하지 않는 게시글 입니다.'); history.back();</script>"

            # Board 객체로 변환(앞서 작성한 Board.py의 from_db 활용)
            board = Board.from_db(row)

            return render_template('board_view.html', board=board)
    finally:
        conn.close()

@app.route('/board/edit/<int:board_id>', methods=['GET', 'POST'])
def board_edit(board_id):
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 화면 보여주기 (기존 데이터 로드)
            if request.method == 'GET':
                sql =  "SELECT * from boards WHERE id = %s"
                cursor.execute(sql, (board_id,))
                row = cursor.fetchone()

                if not row:
                    return "<script>alert('존재하지 않는 게시글입니다.'); history.back();</script>"

                # 본인 확인 로직(필요시 추가)
                if row['member_id'] != session.get('user_id'):
                    return "<script>alert('수정 권한이 없습니다.'); history.back();</script>"
                print(row) # 콘솔에 출력 테스트용
                board = Board.from_db(row)
                return render_template('board_edit.html', board=board)

            # 2. 실제 DB 업데이트 처리
            elif request.method == 'POST':
                title = request.form.get('title')
                content = request.form.get('content')

                sql = "update boards set title = %s, content = %s where id = %s"
                cursor.execute(sql, (title, content, board_id))
                conn.commit()
                return redirect(url_for('board_view', board_id=board_id))
    finally:
        conn.close()

@app.route('/board/delete/<int:board_id>')
def board_delete(board_id):

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE from boards WHERE id = %s" # 저장된 테이블명 boards 사용
            cursor.execute(sql, (board_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"게시글 {board_id}번 삭제 성공")
            else:
                return "<script>alert('삭제할 게시글이 없거나 권한이 없습니다.'); history.back();</script>"
        return redirect(url_for('board_list'))
    except Exception as e:
        print(f"삭제 에러: {e}")
        return "삭제 중 오류가 발생했습니다."
    finally:
        conn.close()
# 주의사항 : ROLE에 ADMIN과 MANAGER만 CUD를 제공한다.
# 일반 사용자는 ROLE이 USER이고 자신의 성적만 볼 수 있다.

########################### 게시판 끝 ##################################
############################## 성적 ###################################
@app.route('/score/add')
def score_add():
    if session.get('user_role') not in ('admin', 'manager'):
        return "<script>alert('권한이 없습니다.'); history.back();</script>"

    # request.args는 URL을 통해서 넘어오는 값 주소뒤에 ?K=V&K=V ~~~~~
    target_uid = request.args.get('uid')
    target_name = request.args.get('name')

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 대상 학생의 id 찾기
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid,))
            student = cursor.fetchone()

            # 2. 기존 성적이 있는지 조회
            existing_score = None
            if student:
                cursor.execute("SELECT * FROM scores WHERE member_id = %s", (student['id'],))
                row = cursor.fetchone()
                print(row) # 테스트용 코드로 dict 타입으로 콘솔 출력
                if row:
                    # 기존에 만든 Score.from_db 활용
                    existing_score = Score.from_db(row)


            return render_template('score_form.html',
                                   target_uid=target_uid,
                                   target_name=target_name,
                                   score=existing_score)  # score 객체 전달

    finally:
        conn.close()

@app.route('/score/save', methods=['POST'])
def score_save():
    if session.get('user_role') not in ('admin', 'manager'):
        return "권한 오류", 403
        # 웹페이지에 오류 페이지로 교체

    # 폼 데이터 수집
    target_uid = request.form.get('target_uid')
    kor = int(request.form.get('korean', 0))
    eng = int(request.form.get('english', 0))
    math = int(request.form.get('math', 0))

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 대상 학생의 id(PK) 가져오기 -> 학생의 번호를 가져옴
            cursor.execute("SELECT id FROM members WHERE uid = %s", (target_uid,))
            student = cursor.fetchone()
            print(student)  # 학번 출력
            if not student:
                return "<script>alert('존재하지 않는 학생입니다.'); history.back();</script>"

            # 2. Score 객체 생성 (계산 프로퍼티 활용)
            temp_score = Score(member_id=student['id'], kor=kor, eng=eng, math=math)
            #            __init__ 를 활용하여 객체 생성

            # 3. 기존 데이터가 있는지 확인
            cursor.execute("SELECT id FROM scores WHERE member_id = %s", (student['id'],))
            is_exist = cursor.fetchone()  # 성적이 있으면 id가 나오고 없으면 None

            if is_exist:
                # UPDATE 실행
                sql = """
                    UPDATE scores SET korean=%s, english=%s, math=%s, 
                                      total=%s, average=%s, grade=%s
                    WHERE member_id = %s
                """
                cursor.execute(sql, (temp_score.kor, temp_score.eng, temp_score.math,
                                     temp_score.total, temp_score.avg, temp_score.grade,
                                     student['id']))
            else:
                # INSERT 실행
                sql = """
                    INSERT INTO scores (member_id, korean, english, math, total, average, grade)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (student['id'], temp_score.kor, temp_score.eng, temp_score.math,
                                     temp_score.total, temp_score.avg, temp_score.grade))

            conn.commit()
            return f"<script>alert('{target_uid} 학생 성적 저장 완료!'); location.href='/score/list';</script>"
    finally:
        conn.close()

@ app.route('/score/list')
def score_list():
    # 1. 권한 체크 (관리자나 매니저만 볼 수 있게 설정)
    if session.get('user_role') not in ('admin', 'manager'):
        return"<script>('권한이 없습니다.'); history.back();</script>"
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # 2. JOIN을 사용하여 학생 이름(name)과 성적 데이터를 함께 조회
            # 성적이 없는 학생은 제외하고, 성적이 있는 학생들만 총점 순으로 정렬
            sql = """
                select m.name, m.uid, s.* FROM scores s
                join members m on s.member_id = m.id
                order by s.total 
            """
            cursor.execute(sql)
            datas = cursor.fetchall()
            # 3. DB에서 가져온 딕셔너리 리스트를 Score 객체 리스트로 변환
            score_objects = []
            for data in datas:
                s = Score.from_db(data)
                s.name = data['name']
                s.uid = data['uid']
                score_objects.append(s)
            return render_template('score_list.html', scores=score_objects)
    finally:
        conn.close()

@app.route('/score/members')
def score_members():
    if session.get('user_role') not in ('admin', 'manager'):
        "<script>alert('권한이 없습니다.'); history.back();</script>"
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            # LEFT JOIN을 통해 성적이 없으면 s.id가 숫자로, 없으면 NULL로 나옵니다.
            sql = """
               SELECT m.id, m.uid, m.name, s.id AS score_id
               FROM members m
               LEFT JOIN scores s ON m.id = s.member_id
               WHERE m.role = 'user'
               ORDER BY m.name ASC
            """
            cursor.execute(sql)
            members = cursor.fetchall()
            return render_template('score_member_list.html', members=members)

    finally:
        conn.close()

@ app.route('/score/my')
def score_my():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "select * from scores where member_id = %s"
            cursor.execute(sql, (session['user_id'],))
            row = cursor.fetchone()
            print(row)

            score = Score.from_db(row) if row else None
            return render_template('score_my.html', score=score)

    finally:
        conn.close()
############################## 성적 끝 ###################################
########################## 파일게시판 #####################################

# 1. 단일/다중파일 업로드처리
## 2. 서비스 패키지 이용
## 3. /uploads라는 폴더를 사용한다 / 용량제한 16mb
## 4. db에서 부모객체가 삭제되면 자식 객체도 삭제 되게 cascade 처리
# 파일명 중복방지용 코드 활용

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    # 폴더 생성용 코드

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 최대 업로드 용량 제한(16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/filesboard/write', methods = ['GET', 'POST'])
def filesboard_write():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        files = request.files.getlist('files')
        # 파일 처리시 html에 필수 코드 : enctype = "multipart/form-data"

        if PostService.save_post(session['user_id'], title, content, files):
            return "<script>alert('게시글이 등록되었습니다.'); location.href='/filesboard';</script>"
        else:
            return "<script>alert('등록 실패'); history.back();</script>"

    return render_template('filesboard_write.html')

# 파일게시판 목록
@app.route('/filesboard')
def filesboard_list():
    posts = PostService.get_posts()
    return render_template('filesboard_list.html', posts=posts)

# 파일게시판 상세 보기
@app.route('/filesboard/view/<int:post_id>')
def filesboard_view(post_id):
    post, fiies = PostService.get_post_detail(post_id)
    if not post:
        return "<script>alert('해당 게시글이 없습니다.'); location.href='/filesboard';</script>"
    return render_template('filesboard_view.html', post=post, fiies=fiies)

# send_from_directory를 사용해 자료 다운로드 가능

@app.route('/download/<path:filename>')
def download_file(filename):
    # render_template 웹브라우저로 보낼 파일명
    # templates라는 폴더에서 main.html을 찾아 보냄
    # 브라우저가 다운로드할 때 보여줄 원본 이름을 쿼리 스트링으로 받거나 DB에서 가져와야 한다.
    origin_name = request.args.get('origin_name')
    return send_from_directory('/uploads', filename, as_attachment=True, download_name=origin_name)
    #   return send_from_directory('uploads/', filename)는 브라우져에서 바로 열어버림
    #   as_attachment=True 로 하면 파일 다운로드 창을 띄움
    #   저장할 파일명은 download_name=origin_name 로 지정

@app.route('/filesboard/delete/<int:post_id>')
def filesboard_delete(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))


    # 삭제 전 작성자 확인을 위해 정보 조회
    post, _ = PostService.get_post_detail(post_id)
    # _은 리턴값을 사용하지 않겠다 라는 관례적인 표현 (_) 사용하지 않는 변수

    if not post:
        return "<script>alert('이미 삭제된 게시글입니다.'); location.href='/filesboard';</script>"

    # 본인 확인 (또는 관리자 권한)
    if post['member_id'] != session['user_id'] and session.get('user_role') != 'admin':
        return "<script>alert('삭제 권한이 없습니다.'); history.back();</script>"

    if PostService.delete_post(post_id):
        return "<script>alert('성공적으로 삭제되었습니다.'); location.href='/filesboard';</script>"
    else:
        return "<script>alert('삭제 중 오류가 발생했습니다.'); history.back();</script>"

@app.route('/filesboard/edit/<int:post_id>', methods=['GET', 'POST'])
def filesboard_edit(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        files = request.files.getlist('files')  # 다중 파일 가져오기

        if PostService.update_post(post_id, title, content, files):
            return f"<script>alert('수정되었습니다.'); location.href='/filesboard/view/{post_id}';</script>"
        return "<script>alert('수정 실패'); history.back();</script>"

    # GET 요청 시 기존 데이터 로드
    post, files = PostService.get_post_detail(post_id)
    if post['member_id'] != session['user_id']:
        return "<script>alert('권한이 없습니다.'); history.back();</script>"

    return render_template('filesboard_edit.html', post=post, files=files)

#################################### 파일게시판 끝 #############################################

@app.route("/") # url 생성용 코드
def index():
    return render_template('main.html')

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5350, debug=True)


