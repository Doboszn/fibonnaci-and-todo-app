import psycopg2
from psycopg2 import sql
from datetime import datetime

db_conn = {
    'dbname':'todo_db',
    'user':'postgres',
    'password':'humble',
    'host':'localhost',
    'port':'5432'
}
def conn_db():
    try:
        conn = psycopg2.connect(**db_conn)
        return conn
    except psycopg2.Error as e:
        print(f'error connect to db:{e}')
        return None
    
def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            );
        """)
        conn.commit()
        print("Table 'tasks' created successfully.")

    except psycopg2.Error as e:
        print(f'Error creating table:{e}')
        conn.rollback()
    finally:
        if cur:
            cur.close()

def add_task(conn, description):
    try:
        cur = conn.cursor()
        cur.execute(" INSERT INTO tasks (description) VALUES (%s)", (description,))
        conn.commit()
        print(f"Task '{description}'added.")
    except  psycopg2.Error as e:
        print(f"Error adding task: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def get_tasks(conn, show_completed=True):
    try:
        cur = conn.cursor()
        if show_completed:
            cur.execute("SELECT * FROM tasks")
        else:
            cur.execute("SELECT *FROM tasks WHERE completed = FALSE ")    
        tasks = cur.fetchall()
        return tasks 
    except psycopg2.Error as e:
        print(f"Error retrieving tasks: {e}")
        return None
    finally:
        if cur:
            cur.close()


def update_task(conn, task_id, new_description=None, completed=None):
    try:
        cur = conn.cursor()
        updates = []
        values = []
        if new_description is not None:
            updates.append(sql.SQL("description = %s"))
            values.append(new_description)
        if completed is not None:
            updates.append(sql.SQL("completed = %s"))
            values.append(completed)

        if updates:
            query = sql.SQL("UPDATE tasks SET {} WHERE id = %s").format(  # The fix is here!
                sql.SQL(", ").join(updates)
            )
            cur.execute(query, (*values, task_id))
            conn.commit()
            print(f"Task {task_id} updated successfully.")
        else:
            print("No updates provided for the task.")
    except psycopg2.Error as e:
        print(f"Error updating task: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()



# def update_task(conn, task_id, new_description=None, completed=None):
#     try:
#         cur = conn.cursor()
#         updates = []
#         values = []
#         if new_description is not None:
#             updates.append(sql.SQL("description = %s"))
#             values.append(new_description)
#         if completed is not None:
#             updates.append(sql.SQL("completed = %s"))
#             values.append(completed)
#         if updates:
#             query = sql.SQL('UPDATE tasks SET {} WHERE id = %s').format(  
#                 sql.SQL(", ").join(updates)
#             )
#             cur.execute(query, (*values, task_id))
#             conn.commit()
#             print(f"Task {task_id} updated successfully.")
#         else:
#             print("No updates provided for the task.") 
#     except psycopg2.Error as e:
#         print(f"Error updating task: {e}")
#         conn.rollback()
#     finally:
#         if cur:
#             cur.close()


def delete_task(conn, task_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        print(f"Task {task_id} deleted successfully.") 
    except psycopg2.Error as e:
        print(f"Error deleting task: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()


def main():
    conn = conn_db()
    if conn:
        create_table(conn)
        while True:
            action = input('enter action(add,get,update,delete,exit):').lower()
            if action == 'add':
                description = input('enter task description:')
                add_task(conn, description)
            elif action == 'get':
                show_completed_str = input('show completed tasks?(y/n):').lower()
                show_completed = show_completed_str == 'y'
                tasks = get_tasks(conn, show_completed)
                if tasks:
                    for task in tasks:
                        print(task)
                else:
                    print("No tasks found.")
            elif action == 'update':
                try:
                    task_id = int(input('enter task id to update:'))
                    new_description = input('enter new description(leave blank to keep current):')
                    completed_str   = input('mark as completed?(y/n):').lower()
                    completed = completed_str == 'y'

                    update_task (conn, task_id, new_description if new_description else None, completed)     
                except ValueError:
                    print("Invalid task ID, Please enter a number")    
            elif action == 'delete':
                try:
                    task_id  = int(input('enter task id to delete:'))
                    delete_task(conn, task_id)
                except ValueError:
                    print('invalid task ID, please enter a number')
            elif action == 'exit':
                break
            else:
                print('invalid action')
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()