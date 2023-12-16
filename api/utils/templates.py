def verification_email(username, verification_code):
    msg_html = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    text-align: center;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #007bff;
                }}
                a.button-link {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a.button-link:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>嗨 {username}!</h1>
                <p>感謝您註冊 TaleWeaver。請點擊下面的按鈕以驗證您的電子郵件地址。</p>
                <a href="http://localhost:3000/verify?username={username}&token={verification_code}" class="button-link">
                    驗證
                </a>
            </div>
        </body>
    </html>
    """
    return msg_html
