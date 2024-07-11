email_format_static = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
    <style>
        body {
            font-family: Verdana, Geneva, Tahoma, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background-color: rgb(0, 69, 173);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 2px 2px 1px rgba(0, 0, 0, 0.945);
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
        }
        .header img {
            width: 100px;
        }
        .content {
            text-align: center;
        }
        .content h1 {
            color: rgb(255, 255, 255);
        }
        .content p {
            line-height: 1.6;
            color: rgb(255, 255, 255);
        }
        .button {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007bff;
            text-decoration: none;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #a3a3a3;
        }
        .verification_link{
            color: #ff5e00;
        }
    </style>
</head>
"""

email_format_dynamic = """
<body>
    <div class="container">
        <div class="header">
            <img src="https://i.ibb.co/mzpLDq0/logo1.png" alt="EchoDAT Logo">
        </div>
        <div class="content">
            <h1>Email Verification</h1>
            <p>Dear {},</p>
            <p>Thank you for registering with EchoDAT! Please click the button below to verify your email address and complete your registration:</p>
            <a href="{}" class="button">Verify Email</a>
            <p>Or copy and paste this link into your browser:</p>
            <p class="verification_link"><a href="{}">{}</a></p>
            <p>If you did not register for an account, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 EchoDAT. All rights reserved.</p>
        </div>
    </div>
</body>
</html>

"""


def generate_email(username, verification_link):
    return email_format_static + email_format_dynamic.format(username, verification_link, verification_link, verification_link)
