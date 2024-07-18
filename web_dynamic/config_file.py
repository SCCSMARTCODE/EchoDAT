"""
This module contains the necessary configuration for the flask app
"""


class Config:
    SECRET_KEY = "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"
    ECHODAT_GMAIL_ACCOUNT = 'sccsmart247@gmail.com'
    ECHODAT_GMAIL_PASSWORD = 'rece wlek kwfj tynh'
    ECHODAT_REG_ADMIN_MAIL_ACCOUNT = 'app.echodat@gmail.com'
    ECHODAT_REG_ADMIN_PASSWORD = "0242c002f7b3ec790596fa68"
    GOOGLE_CLIENT_ID = '507577884511-7g8q7a94q8ue0n6l5f0t85m33v0r4nrt.apps.googleusercontent.com'
    REDIRECT_URL = "http://localhost:5000/callback"
    FLOW_SCOPE_1 = "https://www.googleapis.com/auth/userinfo.profile"
    FLOW_SCOPE_2 = "https://www.googleapis.com/auth/userinfo.email"
