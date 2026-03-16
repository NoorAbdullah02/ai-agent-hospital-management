#step 1. import database objects


from database import get_db, Appointment, init_db
init_db()


#step 3. create data contracts using pydantic models

import datetime as dt
from pydantic import BaseModel

class AppointmentRequest(BaseModel):
    patient_name: str
    reason: str
    start_time: dt.datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    reason: str | None
    start_time: dt.datetime
    canceled: bool
    created_at: dt.datetime

#Cancel appointment request and response models


class CancelRequest(BaseModel):
    patient_name: str
    date: dt.datetime

class CancelResponse(BaseModel):
    id: int
    patient_name: str
    reason: str | None
    start_time: dt.datetime | None
    canceled: bool
    created_at: dt.datetime | None




#step 2 create fastapi application & endpoints

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
app = FastAPI()

# schedule appoinement endpoint


@app.post("/schedule_appointments/")
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
   
   new_appointment = Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )
   db.add(new_appointment)
   db.commit()
   db.refresh(new_appointment)

   new_appointment_response = AppointmentResponse(
       id=new_appointment.id,
       patient_name=new_appointment.patient_name,
       reason=new_appointment.reason,
       start_time=new_appointment.start_time,
       canceled=new_appointment.canceled,
       created_at=new_appointment.created_at
   )

   return new_appointment_response


#cancel appointment endpoint

@app.post("/cancel_appointment/")
def cancel_appointment(request: CancelRequest, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(
        Appointment.patient_name == request.patient_name,
        Appointment.start_time == request.date,
        Appointment.canceled == False
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found or already canceled")

    appointment.canceled = True
    db.commit()
    db.refresh(appointment)

    cancel_response = CancelResponse(
        id=appointment.id,
        patient_name=appointment.patient_name,
        reason=appointment.reason,
        start_time=appointment.start_time,
        canceled=appointment.canceled,
        created_at=appointment.created_at
    )

    return cancel_response  

# list appointments endpoint
@app.get("/list_appointments/")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.canceled == False).all()
    return appointments


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=4444, reload=True)




#step 4. write actual code





#step 5. streamlite dashboard testing (just for testing)

