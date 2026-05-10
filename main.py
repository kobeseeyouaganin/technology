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
    # 使用 The Verge 的科技板块，它的结构更适合新手学习抓取
    url = "https://www.theverge.com/tech"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 智能搜索：先找所有的 h2 标题，因为新闻标题通常都在 h2 里
        articles_data = []
        headings = soup.find_all('h2', limit=8) 
        
        for h2 in headings:
            link_tag = h2.find('a')
            if not link_tag: continue
            
            title = link_tag.text.strip()
            link = link_tag['href']
            # 处理相对路径
            if not link.startswith('http'):
                link = "https://www.theverge.com" + link
            
            # 寻找图片：在标题附近的容器里找 img 标签
            # 逻辑：向上找两层父级，再在里面搜图片
            parent = h2.parent.parent
            img_tag = parent.find('img') if parent else None
            
            img_url = ""
            if img_tag:
                # 尝试抓取 src 属性
                img_url = img_tag.get('src') or ""

            if title and link:
                articles_data.append({
                    'title': title,
                    'link': link,
                    'img': img_url
                })
            
            if len(articles_data) >= 5: break

        # 如果抓取失败的兜底提示
        if not articles_data:
            return "<h3 style='color:red;'>未能抓取到新闻，请检查网络或网站结构。</h3>"

        html_content = """
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="background-color: #e5127d; color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 26px;">李明的科技图文内参</h1>
                    <p style="margin: 8px 0 0 0; opacity: 0.9;">实时监控 The Verge 全球深度硬件资讯</p>
                </div>
                <div style="padding: 25px;">
        """
        
        for i, item in enumerate(articles_data, 1):
            html_content += f"""
            <div style="margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 30px;">
                <h2 style="font-size: 20px; line-height: 1.4; margin-bottom: 15px; color: #111;">{i}. {item['title']}</h2>
                {f'<img src="{item["img"]}" style="width: 100%; height: auto; border-radius: 8px; margin-bottom: 15px; display: block;">' if item['img'] else ''}
                <div style="margin-top: 15px;">
                    <a href="{item['link']}" style="display: inline-block; padding: 12px 25px; background-color: #e5127d; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">阅读详细报道</a>
                </div>
            </div>
            """
        
        html_content += """
                </div>
                <div style="background-color: #f9f9f9; padding: 20px; text-align: center; color: #888; font-size: 12px;">
                    由您的 GitHub 云端机器人自动抓取并渲染
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    except Exception as e:
        return f"<h3>爬取过程中出现错误:</h3><p>{str(e)}</p>"

def send_email(content):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = sender 

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header('李明的每日科技内参', 'utf-8')

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
