class AppConfig:
    app_name: str = "Mercor Project"
    debug: bool = False
    database_url: str = "mongodb+srv://prathamrasal6:1m9RxrgFY1KNr2n4@mercor.377aio6.mongodb.net/?retryWrites=true&w=majority&appName=Mercor"
    origins = [
    "http://localhost:3000",
    ]   

config = AppConfig()