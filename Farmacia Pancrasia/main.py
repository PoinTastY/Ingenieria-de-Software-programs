from Interface.db_repo import DbRepo
from Presentation.Views.login import Login

if __name__ == "__main__":
    try:
        print("Conectando a la base de datos...")
        connection_string = "mongodb://localhost:27017/"
        db_repo = DbRepo()
        app = Login(db_repo)
        print("Running")
        app.mainloop()
        print("Finishing")
    except Exception as e:
        print("Error al conectar a la base de datos")
        exit(1)
    finally:
        db_repo.__del__()
