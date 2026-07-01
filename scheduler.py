import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import SessionLocal
from tasks import daily_watering_audit

def get_scheduler_db_context():
    """
    Creates an isolated database session block specifically for background workers.
    Ensures safe resource closure upon transaction cycle conclusion.
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

async def job_wrapper():
    """
    An intermediate routing worker block that spins up the audit execution loop,
    injecting a clean, dedicated database session into the task space.
    """
    print("--- [SCHEDULER RUNTIME] Commencing automated daily environmental audit sequence ---")
    db = get_scheduler_db_context()
    try:
        # Invoke the core business audit routine natively
        await daily_watering_audit(db)
    except Exception as e:
        print(f"Scheduler Error: Automated transaction sequence failure: {e}")
    finally:
        # Hard close the connection to clean up backend pool channels
        db.close()
        print("--- [SCHEDULER RUNTIME] Automated execution block complete. Session closed ---")

async def main():
    """
    Initializes the asynchronous task orchestration engine mapping out background intervals.
    """
    scheduler = AsyncIOScheduler()
    
    # Execution schedule rule definition layout mapping
    # Production parameter mapping: triggers automatically every day at 10:00 AM
    scheduler.add_job(job_wrapper, 'cron', hour=10, minute=0)
    
    # Development testing mapping: runs automatically every 60 seconds to inspect live logs
    #scheduler.add_job(job_wrapper, 'interval', seconds=60)
 
    
    scheduler.start()
    print("Log: Async background scheduling worker initialized and monitoring patterns actively.")
    
    # Keep the background tracking loop running continuously
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Boot the async execution script natively
    asyncio.run(main())
