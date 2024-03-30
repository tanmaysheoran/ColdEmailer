from classes.Entities.Waitlist.Model import Waitlist
from classes.Entities.Waitlist.Factory import mongoDBManager
from classes.SendGrid.API import SendGrid
from pydantic import EmailStr


def email(name: str, email: EmailStr):
    subject = " 🚀 Woohoo! You've Joined thehightabl Waitlist! 🚀"
    email_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to thehightabl!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333333;
            text-align: center;
        }
        p {
            color: #666666;
            font-size: 16px;
            line-height: 1.5;
        }
        .cta-button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px auto;
            transition: background-color 0.3s;
        }
        .cta-button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Woohoo! You've Joined thehightabl Waitlist! 🚀</h1>
        <p>Hey [Name],</p>
        <p>Huge virtual high-fives and confetti showers for taking the leap and joining thehightabl waitlist! 🎉🌟</p>
        <p>We're thrilled to have you aboard! Seriously, your mere presence here is making our virtual office do the happy dance. 💃✨</p>
        <p>You're officially in line to experience networking like never before. Picture this: effortlessly gliding through a sea of incredible connections, finding your networking soulmates with the grace of a swan in a pond. That's the kind of magic we're cooking up at thehightabl!</p>
        <p>Here's a little sneak peek of what awaits you:</p>
        <ul>
            <li>🚀 <strong>Effortless Connection:</strong> Say goodbye to awkward icebreakers and hello to seamless networking. With thehightabl, you'll be zipping through connections faster than a rocket on a mission.</li>
            <li>🔍 <strong>Tailored Search:</strong> Looking for someone specific? No problemo! Whether it's by name, industry, or expertise, our search feature will have you feeling like a networking ninja in no time.</li>
            <li>📧 <strong>Personalized Outreach:</strong> Crafting the perfect email doesn't have to be a chore. Whip up personalized templates faster than you can say "connections are my superpower" and watch your networking game reach new heights.</li>
        </ul>
        <p>So, grab your virtual passport because you're about to embark on an epic networking adventure with us!</p>
        <p>Keep an eye on your inbox for updates, sneak peeks, and maybe even a surprise or two. 💌</p>
        <p>Until then, stay awesome and get ready to soar to new networking heights!</p>
        <p>Cheers,<br>[Your Name]<br>Chief Networking Enthusiast at thehightabl</p>
    </div>
</body>
</html>
'''

    email_template = email_template.replace("[Name]", name)
    email_template = email_template.replace("[Your Name]", "Tanmay Sheoran")
    send_grid = SendGrid()
    return send_grid.send_email(to_email=email, subject=subject,
                                content=email_template)


def email_already_exists(email: EmailStr):
    items = mongoDBManager.read_documents({"email": email, "isDeleted": False})
    return len(items) > 0


def insert_waitlist(waitlist: Waitlist):
    if email_already_exists(waitlist.email):
        return True

    if mongoDBManager.insert_document(waitlist):
        email(waitlist.name, waitlist.email)
        return True
    else:
        return False
