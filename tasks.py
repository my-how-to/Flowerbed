import datetime
from sqlalchemy.orm import Session
import models
from telegram_bot import send_telegram_alert
from weather import get_current_weather_details

async def check_winter_leak_emergency(db: Session):
    """
    Evaluates infrastructure safety against off-season configuration rules.
    Triggers critical warning logs if well activity is detected while winterized.
    """
    status = db.query(models.SystemSeasonStatus).first()
    if not status:
        return

    if status.is_summer_season is False and status.well_valve_physically_open is True:
        alert_text = (
            "CRITICAL SYSTEM BREACH DETECTED\n\n"
            "The environment is configured for Winter Mode, but well pressure sensors report active liquid feed.\n"
            "High structural probability of pipeline burst hazards.\n\n"
            f"Timestamp: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
        await send_telegram_alert(alert_text)
        print("Log: Critical automated safety alert routed to notification pipeline.")

async def daily_watering_audit(db: Session):
    """
    Executes automated environmental validation sequence routines.
    Dispatches volunteer request updates under active thermal and seasonal parameters.
    """
    now = datetime.datetime.utcnow()
    
    if now.month < 6 or (now.month == 6 and now.day < 15) or now.month > 10:
        print(f"Log: Active cycle outside target seasonal parameters ({now.strftime('%Y-%m-%d')}). Execution suspended.")
        return

    one_week_ago = now - datetime.timedelta(days=7)
    recent_watering = db.query(models.WateringHistory).filter(
        models.WateringHistory.watered_at >= one_week_ago
    ).first()

    if recent_watering:
        print(f"Log: Active irrigation recorded inside parameters within 7 days. Notification suspended.")
        return

    weather_data = await get_current_weather_details()
    if not weather_data:
        print("Log: Missing response parameters from weather interface layer. Audit rescheduled.")
        return

    temp = weather_data["temp"]
    is_raining = weather_data["is_raining"]

    print(f"Log: Operational audit variables metrics - Temperature: {temp}C, Precipitation: {is_raining}")

    if temp > 30 and not is_raining:
        # Clean, punchy text block with zero fluff or broken links
        message = (
            f"⚠️ *IRRIGATION REQUIRED*\n"
            f"* **Status:** No watering logs for 7 days.\n"
            f"* **Weather:** {temp}°C, No precipitation."
        )
        
        # Dispatch the message triggering the show_button flag layout
        await send_telegram_alert(message, show_button=True)
        print("Log: Trigger met. Clean warning dispatched to communication channel.")
