from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult
import psycopg2
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def check_book_availability(book_id):
    """Check if the book with the given ID is available."""
    conn = None
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="aass",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        # Create a new cursor
        cur = conn.cursor()

        # Execute a SQL query to check the availability
        cur.execute("SELECT available FROM book_library_book WHERE id = %s", (book_id,))
        # Fetch one record and return the availability status
        available = cur.fetchone()
        cur.close()
        logging.info(f"Book ID {book_id}: Availability checked, found: {available}")
        return available[0] if available else False
    except Exception as e:
        logging.error(f"Database connection failed due to {e}")
        return False
    finally:
        if conn is not None and conn.closed == 0:
            conn.close()

    return False


def handle_check_availability(task: ExternalTask) -> TaskResult:
    book_id = task.get_variable('book_id')
    is_available = check_book_availability(book_id)
    logging.info(f"Processing task for book ID {book_id}: Book available = {is_available}")
    return task.complete({"bookAvailable": True})

def handle_process_rental(task: ExternalTask) -> TaskResult:
    # Assume necessary variables and business logic for processing the rental
    book_id = task.get_variable('book_id')
    print(book_id)
    # Further processing logic here
    return task.complete({"rentalConfirmation": True})




if __name__ == '__main__':
    config = {
        "auth_basic": {"username": "demo", "password": "demo"},
        "maxTasks": 1,
        "lockDuration": 60000,
        "asyncResponseTimeout": 5000,
        "retries": 3,
        "retryTimeout": 5000,
        "sleepSeconds": 30
    }

    # Worker 1 subscribes to checkBookAvailability
    worker1 = ExternalTaskWorker(worker_id="demo", config=config)
    worker1.subscribe("checkBookAvailability", handle_check_availability)

    # Worker 2 subscribes to processRental
    #worker2 = ExternalTaskWorker(worker_id="2", config=config)
    #worker2.subscribe("processRental", handle_process_rental)

