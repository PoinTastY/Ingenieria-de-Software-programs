from Data.db_repo import DBRepo
from Presentation.login import Login

if __name__ == "__main__":
    try:
        print("Conectando a la base de datos...")
        db_repo = DBRepo()
        app = Login(db_repo)
        print("Running")
        app.mainloop()
        print("Finishing")
    except Exception as e:
        print("Error al conectar a la base de datos")
        exit(1)
    finally:
        db_repo.__del__()
