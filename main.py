import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def get_news():
    api_key = os.environ['NEWS_API_KEY']
    # 依然使用英文源，因为图片质量和覆盖率更高
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={api_key}'
    
    response = requests.get(url)
    articles = response.json().get('articles', [])
    
    if not articles:
        return "<h3>今日暂无科技要闻。</h3>"
        
    # 开始构建 HTML 格式的正文
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px;">今日科技要闻 (Global Tech News)</h2>
    """
    
    for i, art in enumerate(articles, 1):
        title = art.get('title', '无标题')
        url_link = art.get('url', '无链接')
        img_url = art.get('urlToImage')
        description = art.get('description', '')

        html_content += f"""
        <div style="margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px;">
            <h3 style="margin-bottom: 10px;">{i}. {title}</h3>
            {f'<img src="{img_url}" style="width: 100%; max-width: 500px; border-radius: 8px; margin-bottom: 10px;">' if img_url else ''}
            <p style="font-size: 14px; color: #666;">{description}</p>
            <a href="{url_link}" style="display: inline-block; padding: 8px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-size: 14px;">阅读原文</a>
        </div>
        """
    
    html_content += "</body></html>"
    return html_content

def send_email(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = sender 

    # 注意：这里从 'plain' 变成了 'html'
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header('每日科技图文早报', 'utf-8')

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
