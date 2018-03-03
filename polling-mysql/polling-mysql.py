import mysql.connector
import polling


def check_records():
    try:
        conn = mysql.connector.connect(user='deon',
                                       password='password',
                                       host='0.0.0.0',
                                       database='job_list')
        cursor = conn.cursor()
        cursor.execute("""
              select * from job where (status = 'completed') and (notified = false)
           """)
        completed_jobs = cursor.fetchall()
        if not completed_jobs:
            print("No completed jobs to process")
        else:
            for job in completed_jobs:
                (job_id, _, user_id, _, _) = job
                print("Notifying user {} that their job has been completed".format(user_id))
                cursor.execute("""
                    update job set notified = true where id = {}
                """.format(job_id))
                conn.commit()
    finally:
        conn.close()


polling.poll(
    lambda: check_records(),
    step=5,
    poll_forever=True)
