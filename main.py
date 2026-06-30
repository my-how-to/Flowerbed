import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Local application module imports
import models
from database import engine, get_db
from tasks import check_winter_leak_emergency, daily_watering_audit


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application lifecycle startup and shutdown routines.
    Ensures correct production table mapping hooks execute before servicing traffic.
    """
    # Create production database tables safely upon service initialization
    models.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown resource cleanup routines can be placed here if necessary


# Initialize the application instance injecting the lifecycle manager context
app = FastAPI(title="Smart Flowerbed API Workspace", lifespan=lifespan)


@app.get("/")
def read_root():
    """
    Root application route handler providing service status information.
    """
    return {
        "identity": "Smart Flowerbed Management Service Interface Backend Running Instance",
        "documentation": "Route traffic explicitly to /docs interface path"
    }


@app.post("/sensor/well-status")
async def update_well_status(is_open: bool, db: Session = Depends(get_db)):
    """
    Endpoint for physical pressure sensors to push current well valve states.
    Triggers automated off-season structural breach evaluations.
    """
    status = db.query(models.SystemSeasonStatus).first()
    
    # Initialize seasonal configuration state tracking parameters if absent
    if not status:
        status = models.SystemSeasonStatus(is_summer_season=True)
        db.add(status)
        db.commit()
        db.refresh(status)
    
    status.well_valve_physically_open = is_open
    status.last_checked = datetime.datetime.utcnow()
    db.commit()
    
    # Evaluate current state data matrix against infrastructure risk patterns
    await check_winter_leak_emergency(db)
    return {"status": "updated", "well_valve_physically_open": is_open}


@app.put("/system/season")
def set_season(is_summer: bool, db: Session = Depends(get_db)):
    """
    Administrative endpoint to toggle system scheduling parameters between summer and winter rules.
    """
    status = db.query(models.SystemSeasonStatus).first()
    if not status:
        status = models.SystemSeasonStatus(is_summer_season=is_summer)
        db.add(status)
    else:
        status.is_summer_season = is_summer
    
    db.commit()
    return {"message": "System seasonal operational mode updated", "is_summer_season": is_summer}


@app.post("/action/mark-watered")
def mark_as_watered(user_id: int, db: Session = Depends(get_db)):
    """
    Allows fields volunteers to log completed irrigation event transactions.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден в системе")
        
    new_record = models.WateringHistory(
        user_id=user_id,
        watered_at=datetime.datetime.utcnow()
    )
    db.add(new_record)
    db.commit()
    
    return {
        "status": "success", 
        "message": f"Волонтер {user.name} успешно зафиксировал полив клумбы!",
        "date": new_record.watered_at
    }


@app.post("/system/test-daily-check")
async def test_daily_check(db: Session = Depends(get_db)):
    """
    Simulates automated cron routines evaluating multi-variable environmental thresholds.
    """
    await daily_watering_audit(db)
    return {"message": "Manual execution routine completed. Inspect logging streams."}
