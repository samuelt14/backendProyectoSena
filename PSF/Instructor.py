from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector

#Connect to the database
mydb = mysql.connector.connect (
    host = "bq96ldxibxxeubxnxzpa-mysql.services.clever-cloud.com",
    user = "usiv06zwsjtem3rd",
    password = "KYfpMEsmyeqDaoxzP7jH",
    database = "bq96ldxibxxeubxnxzpa",
    port = 3306
)

#Create a cursor object
cursor = mydb.cursor ()

app = FastAPI()

#Class
class Instructor (BaseModel):
    idInstructor: int
    Nombre: str
    Correo: str
    Cedula: int
    TipoContrato: str
    Contacto: int


@app.get("/Instructor", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Instructor"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Instructor/{idInstructor}", status_code=status.HTTP_200_OK)
def get_user_by_id(idInstructor: int):
    select_query = "SELECT * FROM Instructor WHERE idInstructor = %s"
    cursor.execute(select_query, (idInstructor,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
@app.post("/Instructor", status_code=status.HTTP_201_CREATED)
def insert_user(Instructor: Instructor):

    insert_query = """
    INSERT INTO Instructor (idInstructor, Nombre, Correo, Cedula, TipoContrato, Contacto)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (Instructor.idInstructor, Instructor.Nombre, Instructor.Correo, Instructor.Cedula, Instructor.TipoContrato, Instructor.Contacto)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Instructor inserted successfully"}

@app.put("/Instructor/{idInstructor}", status_code=status.HTTP_200_OK)
def update_user(idInstructor: int, Instructor: Instructor):

    update_query = """
    UPDATE Instructor
    SET Nombre = %s, Correo = %s, Cedula = %s, TipoContracto = %s, Contacto = %s
    WHERE idInstructor = %s
    """
    values = (Instructor.Nombre, Instructor.Correo, Instructor.Cedula, Instructor.TipoContrato, Instructor.Contacto, Instructor.idInstructor)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor updated successfully"}

@app.delete("/Instructor/{idInstructor}", status_code=status.HTTP_200_OK)
def delete_user(idInstructor: int):
    delete_query = "DELETE FROM Instructor WHERE idInstructor = %s"
    cursor.execute(delete_query, (idInstructor,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor deleted successfully"}