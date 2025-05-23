RESET_PASSWORD_EMAIL_TEMPLATE = """
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
        .verify-button {{ display: inline-block; padding: 12px 24px; background-color: #007BFF; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        .verify-button {{ padding: 12px 24px; background-color: #002855; color: #fff; text-decoration: none; }}
        .footer {{ background-color: #E9ECEF; padding: 20px; text-align: center; font-size: 14px; color: #555; }}
        .footer a {{ color: #007BFF; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <img src="https://trumpetproject.eu/wp-content/uploads/2023/02/logo-trumpet-white-color.svg" alt="TRUMPET Project Logo" />
    </div>
    <div class="content">
        <h1>Password Reset Request</h1>
        <p>Dear User,</p>
        <p>We received a request to reset your password for your account associated with this email address.</p>
        <p>Please click the button below to set a new password. This link will expire in 30 minutes.</p>

        <p style="text-align:center;">
            <a href="{host}/password-reset?token={token}" class="verify-button">Reset Password</a>
        </p>
        <p>If you didn’t request a password reset, you can safely ignore this email.</p>
        <p>Best regards,<br/>TRUMPET Project Team</p>
    </div>
    <div class="footer">
        <p>
            Funded by the European Union’s Horizon Europe Programme<br/>
            Grant Agreement No. 101070038
        </p>
        <p>
            Website: <a href="https://trumpetproject.eu">trumpetproject.eu</a><br/>
            Email: <a href="mailto:info@trumpetproject.eu">info@trumpetproject.eu</a>
        </p>
        <p>
            &copy; 2023 Istituto Romagnolo per lo Studio dei Tumori “Dino Amadori” – IRST S.r.l.
        </p>
    </div>
</body>
</html>
"""

