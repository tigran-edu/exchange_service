CREATE_TABLE = "CREATE TABLE IF NOT EXISTS {} ({})"
DELETE_TABLE = "DROP TABLE {}"

CREATE_USER = "INSERT INTO users ({}) VALUES ({})"
SELECT_USER = "SELECT * FROM users WHERE login='{}'"
SELECT_USER_LOGIN = "SELECT login FROM users WHERE user_id='{}'"
UPDATE_USER = "UPDATE users SET {} WHERE login = '{}'"

CREATE_POST = "INSERT INTO posts ({}) VALUES ({})"
SELECT_POST = "SELECT * FROM posts WHERE post_id = '{}'"
UPDATE_POST = "UPDATE posts SET {} WHERE post_id = '{}'"
DELETE_POST = "DELETE FROM posts WHERE post_id = '{}'"

SELECT_STATS = (
    "SELECT DISTINCT actor_id, action_type FROM log_db.action_log WHERE post_id = '{}'"
)

SELECT_TOP_POSTS = """SELECT post_id, owner_id, COUNT() as amount FROM 
                      (SELECT DISTINCT post_id, owner_id, actor_id FROM log_db.action_log WHERE action_type = {}) 
                      GROUP BY post_id, owner_id ORDER BY amount DESC"""

SELECT_TOP_USERS = """SELECT owner_id, COUNT() as amount FROM
                      (SELECT DISTINCT post_id, owner_id, actor_id FROM log_db.action_log WHERE action_type = 2) 
                      GROUP BY owner_id ORDER BY amount DESC"""
