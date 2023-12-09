def verification_email(username, verfication_code):
    msg_html = f"""
    <h1>Hi {username}!</h1>
    <p>Thanks for signing up for TaleWeaver. Please verify your email address by clicking on the botton below.</p>
    <a href="http://localhost:3000/user/verify/{verfication_code}">
        <button>Verify</button>
    </a>
    """
    return msg_html
