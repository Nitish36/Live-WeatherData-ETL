from database_feeder import feed_database
from prefect import flow, task


@task
def database_pipeline():
    feed_database()

@flow(log_prints=True)
def push_to_database():
    print("Pipeline is running")
    database_pipeline()

if __name__ == "__main__":
    push_to_database()