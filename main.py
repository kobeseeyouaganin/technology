import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def get_news():
    api_key = os.environ['NEWS_API_KEY']
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=zh&pageSize=5&apiKey={api_key}'
    response = requests.get(url)
    articles = response.json().get('articles', [])

    content = "今日科技要闻：\n\n"
    for i, art in enumerate(articles, 1):
        content += f"{i}. {art['title']}\n链接: {art['url']}\n\n"
    return content

def send_email(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = sender

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header('每日科技早报', 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, [receiver], message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"发送失败: {e}")

if __name__ == "__main__":
    news_content = get_news()
    send_email(news_content)
