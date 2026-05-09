import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def get_news():
    api_key = os.environ['NEWS_API_KEY']
    # 将 language 改为 en 确保能抓取到全球科技头条
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
    
    response = requests.get(url)
    articles = response.json().get('articles', [])
    
    # 如果抓取到了内容，就开始拼接正文
    if not articles:
        return "今日暂无科技要闻（数据源可能为空）。"
        
    content = "今日科技要闻 (Global Tech News)：\n\n"
    for i, art in enumerate(articles, 1):
        # 英文标题和链接
        title = art.get('title', '无标题')
        url_link = art.get('url', '无链接')
        content += f"{i}. {title}\n链接: {url_link}\n\n"
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
