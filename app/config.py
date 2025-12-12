import os

class Settings:
    RSS_URL = os.getenv("RSS_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMAIL_FROM = "mail2dinesh112@gmail.com"
    EMAIL_TO = "msg2mypersonal@gmail.com"
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "mail2dinesh112@gmail.com"
    SMTP_PASSWORD = "wfxq dbmw luql scqh"

settings = Settings()