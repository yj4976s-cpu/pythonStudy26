import os
import uuid

from DATA.common import Session

class PostService:
    @staticmethod
    def save_post(member_id, title, content, files=None, upload_folder='uploads/'):
        # 게시글과 첨부파일 동시에 저장(트랜젝션)
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql_post = "insert into posts (member_id, title, content) values (%s, %s, %s)"
                cursor.execute(sql_post, (member_id, title, content))

                # 방금 INSERT한 게시글의 ID를 가져오기
                post_id = cursor.lastrowid

                # 3. 다중파일 처리
                if files:
                    for file in files:
                        if file and file.filename != '':
                            origin_name = file.filename
                            ext = origin_name.rsplit('.', 1)[1].lower()
                            save_name = f"{uuid.uuid4().hex}.{ext}"  # 상단에 import uuid
                            file_path = os.path.join(upload_folder, save_name)  # 상단에 import os

                            file.save(file_path)  # 서버에 저장 uploads/

                            # attachments 테이블에 각각 저장
                            sql_file = """INSERT INTO attachments (post_id, origin_name, save_name, file_path)
                                          VALUES (%s, %s, %s, %s)"""
                            cursor.execute(sql_file, (post_id, origin_name, save_name, file_path))

                conn.commit()
                return True

        except Exception as e:
            print(f"error saving post: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # 파일게시물 목록
    @staticmethod
    def get_posts():
        # 작성자 이름과 첨부파일 개수를 함께 조회함
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 서브쿼리를 사용해 게시글의 첨부파일 개수(file_count)를 가져온다.

                sql = """
                        SELECT p.*, m.name as writer_name,
                               (SELECT COUNT(*) FROM attachments WHERE post_id = p.id) as file_count
                        FROM posts p
                        JOIN members m ON p.member_id = m.id
                        ORDER BY p.created_at DESC
                    """
                cursor.execute(sql)


                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_post_detail(post_id):
        # 게시글 상세정보와 첨부파일 정보를 같이 조회

        conn= Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 조회수 증가
                cursor.execute("UPDATE posts SET view_count = view_count +1 WHERE id = %s", (post_id,))

                # 2. 게시글 정보 조회 (작성자 이름 포함)
                sql_post = """
                        SELECT p.*, m.name as writer_name 
                        FROM posts p
                        JOIN members m ON p.member_id = m.id
                        WHERE p.id = %s
                    """
                cursor.execute(sql_post, (post_id,))
                post = cursor.fetchone()

                # 3. 첨부파일 정보 조회
                cursor.execute("SELECT * FROM attachments  WHERE post_id = %s", (post_id,))
                files = cursor.fetchall()
                conn.commit()
                return post, files
        finally:
            conn.close()


    @staticmethod
    def delete_post(post_id, upload_folder='uploads/'):
        """게시글 및 관련 실제 파일 삭제"""
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 삭제 전 첨부파일 정보 조회 (파일 삭제를 위해)
                cursor.execute("SELECT save_name FROM attachments WHERE post_id = %s", (post_id,))
                files = cursor.fetchall()

                # 2. 서버에서 실제 파일 삭제
                for f in files:
                    file_path = os.path.join(upload_folder, f['save_name'])
                    if os.path.exists(file_path):
                        os.remove(file_path)  # 실제 하드에서 삭제 진행

                # 3. 게시글 삭제 (DB 외래키 ON DELETE CASCADE 설정 덕분에 attachments도 자동 삭제됨)
                # 삭제시 cascade 옵션을 하지 않으면 자식 테이블 데이터를 선 삭제후 부모테이블 데이터를 삭제

                sql = "DELETE FROM posts WHERE id = %s"
                cursor.execute(sql, (post_id,))

                conn.commit()
                return True
        except Exception as e:
            print(f"Delete Error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()


    @staticmethod  # 다중파일 수정 처리(기존파일 지우고 업데이트)
    def update_post(post_id, title, content, files=None, upload_folder='uploads/'):
        # 게시글 및 다중파일 수정
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 기본 정보 수정
                cursor.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s", (title, content, post_id))

                # 2. 새 파일들이 들어왔을 경우만 기존 파일 삭제 및 교체
                # (아무 파일도 선택 안 하면 기존 파일 유지)
                if files and any(f.filename != '' for f in files):

                    # A. 기존 물리적 파일 삭제를 위해 save_name 조회
                    cursor.execute("SELECT save_name FROM attachments WHERE post_id = %s", (post_id,))
                    old_files = cursor.fetchall()
                    for old in old_files:
                        old_path = os.path.join(upload_folder, old['save_name'])
                        if os.path.exists(old_path):
                            os.remove(old_path)

                    # B. DB에서 기존 첨부파일 기록 삭제
                    cursor.execute("DELETE FROM attachments WHERE post_id = %s", (post_id,))

                    # C. 새로운 파일들 저장
                    for file in files:
                        if file and file.filename != '':
                            origin_name = file.filename
                            ext = origin_name.rsplit('.', 1)[1].lower()
                            save_name = f"{uuid.uuid4().hex}.{ext}"
                            file_path = os.path.join(upload_folder, save_name)
                            file.save(file_path)

                            cursor.execute("""
                                       INSERT INTO attachments (post_id, origin_name, save_name, file_path)
                                       VALUES (%s, %s, %s, %s)
                                   """, (post_id, origin_name, save_name, file_path))

                conn.commit()
                return True
        except Exception as e:
            print(f"Update Error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()










