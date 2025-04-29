EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .verify-button {{ padding: 12px 24px; background-color: #007BFF; color: #fff; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>Email Verification</h1>
    <p>Click below to verify:</p>
    <a href="http://www.example.com/verify-email?token={token}" class="verify-button">Verify Email</a>
</body>
</html>
"""
