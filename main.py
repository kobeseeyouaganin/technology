import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

def get_news_by_scraping():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # 抓取 The Verge 的科技板块
    url = "https://www.theverge.com/tech"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 抓取前 5 条标题
        articles = soup.find_all('h2', limit=5)
        
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
            <div style="background-color: #e5127d; color: white; padding: 20px; text-align: center;">
                <h1>The Verge 深度科技快报</h1>
            </div>
            <div style="padding: 20px;">
        """
        
        for i, art in enumerate(articles, 1):
            link_tag = art.find('a')
            if link_tag:
                title = link_tag.text.strip()
                link = "https://www.theverge.com" + link_tag['href'] if not link_tag['href'].startswith('http') else link_tag['href']
                
                html_content += f"""
                <div style="margin-bottom: 25px; border-left: 4px solid #e5127d; padding-left: 15px;">
                    <h3 style="margin: 0 0 10px 0;">{i}. {title}</h3>
                    <a href="{link}" style="color: #e5127d; text-decoration: none; font-weight: bold;">查看深度报道 →</a>
                </div>
                """
        
        html_content += """
            </div>
            <p style="text-align: center; color: #888; font-size: 12px;">由您的 GitHub 云端机器人自动抓取发送</p>
        </body>
        </html>
        """
        return html_content
    except Exception as e:
        return f"<h3>爬取数据时遇到了一点小麻烦:</h3><p>{e}</p>"

def send_email(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = sender 

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header('每日科技深度爬取报告', 'utf-8')

    # 初始化变量，方便在 finally 中引用
    smtp_obj = None
    try:
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, [receiver], message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"发送失败: {e}")
    finally:
        # 无论成功还是失败，只要连接建立了，就强制退出
        if smtp_obj:
            smtp_obj.quit()
            print("SMTP 连接已安全关闭")

if __name__ == "__main__":
    news_content = get_news_by_scraping()
    send_email(news_content)
