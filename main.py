import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

def get_rich_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # 抓取 TechCrunch 首页
    url = "https://techcrunch.com/"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 抓取文章容器（TechCrunch 的文章块通常是 post-block）
        articles = soup.find_all('div', class_='post-block', limit=5)
        
        html_content = """
        <html>
        <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="background-color: #02ad5f; color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">李明的科技图文内参</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.8;">深度爬取全球最新硬件与互联网动态</p>
                </div>
                <div style="padding: 20px;">
        """
        
        for art in articles:
            # 1. 抓取标题和链接
            title_tag = art.find('a', class_='post-block__title__link')
            title = title_tag.text.strip()
            link = title_tag['href']
            
            # 2. 抓取图片（这是关键！）
            img_tag = art.find('img')
            # 优先找 src，如果没有就找 data-src（应对懒加载）
            img_url = img_tag.get('src') or img_tag.get('data-src') if img_tag else None
            
            # 3. 抓取简介
            desc_tag = art.find('div', class_='post-block__content')
            description = desc_tag.text.strip() if desc_tag else ""

            # 拼接 HTML 卡片布局
            html_content += f"""
            <div style="margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 30px;">
                {f'<img src="{img_url}" style="width: 100%; height: auto; border-radius: 8px; margin-bottom: 15px;">' if img_url else ''}
                <h2 style="font-size: 20px; margin: 0 0 10px 0; color: #333;">{title}</h2>
                <p style="font-size: 15px; color: #666; line-height: 1.6;">{description[:150]}...</p>
                <a href="{link}" style="display: inline-block; margin-top: 10px; color: #02ad5f; text-decoration: none; font-weight: bold;">阅读深度报道 →</a>
            </div>
            """
        
        html_content += """
                </div>
                <div style="background-color: #f9f9f9; padding: 20px; text-align: center; color: #999; font-size: 12px;">
                    由您的 GitHub 云端机器人自动抓取发送
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    except Exception as e:
        return f"<h3>爬虫在寻找图片时迷路了:</h3><p>{e}</p>"

def send_email(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = sender 

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header('李明的科技图文内参', 'utf-8')

    smtp_obj = None
    try:
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, [receiver], message.as_string())
        print("图文邮件发送成功")
    except Exception as e:
        print(f"发送失败: {e}")
    finally:
        if smtp_obj:
            smtp_obj.quit()

if __name__ == "__main__":
    news_content = get_rich_news()
    send_email(news_content)
