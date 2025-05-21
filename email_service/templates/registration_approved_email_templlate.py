REGISTRATION_APPROVED_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }}
        .header {{ background-color: #002855; padding: 20px; text-align: center; }}
        .header img {{ max-width: 160px; }}
        .content {{ padding: 30px; background-color: #ffffff; }}
        h1 {{ font-size: 24px; color: #002855; margin-bottom: 20px; }}
        p {{ font-size: 16px; line-height: 1.6; margin-bottom: 20px; }}
        .footer {{ background-color: #E9ECEF; padding: 20px; text-align: center; font-size: 14px; color: #555; }}
        .footer a {{ color: #007BFF; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <img src="https://trumpetproject.eu/wp-content/uploads/2023/02/logo-trumpet-white-color.svg" alt="TRUMPET Project Logo" />
    </div>
    <div class="content">
        <h1>Registration Approved</h1>
        <p>Dear User,</p>
        <p>Your registration has been approved successfully.</p>
        <p>You can now log in and start using the system.</p>
        <p>If you have any questions, feel free to reach out to our support team.</p>
        <p>Best regards,<br/>System Admin</p>
    </div>
    <div class="footer">
        <p>
            This is an automated message from the researcher server system.<br/>
            Please do not reply to this email.
        </p>
        <p>
            Email: <a href="mailto:no-reply@system-domain">no-reply@system-domain</a>
        </p>
    </div>
</body>
</html>
"""
