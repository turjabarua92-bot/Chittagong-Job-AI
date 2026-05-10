import requests
from bs4 import BeautifulSoup

# আপনার দেওয়া সঠিক টোকেন এবং চ্যাট আইডি
TOKEN = '8686344565:AAFDx4LpXPWGeEu2wfzq79bAkL5wfqMGJdA'
CHAT_ID = '5237050315'

def send_telegram_msg(message):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML', 'disable_web_page_preview': False}
    try:
        requests.post(url, data=payload)
    except:
        pass

def scrape_jobs():
    send_telegram_msg("🚀 <b>চট্টগ্রাম ও সরকারি চাকরির খবর খোঁজা হচ্ছে...</b>")
    
    SOURCES = [
        {'name': 'BDJobs চট্টগ্রাম', 'url': 'https://bdjobs.com'},
        {'name': 'Teletalk সরকারি জব', 'url': 'https://teletalk.com.bd'}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    found_any = False

    for source in SOURCES:
        try:
            response = requests.get(source['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            count = 0
            for link in links:
                href = link['href'].lower()
                if ('job' in href or 'details' in href) and count < 3:
                    full_link = link['href'] if 'http' in link['href'] else source['url']
                    title = link.text.strip()[:100]
                    if len(title) > 10:
                        msg = f"<b>📌 {source['name']}</b>\n\n📄 {title}\n🔗 <a href='{full_link}'>লিঙ্ক এখানে</a>"
                        send_telegram_msg(msg)
                        count += 1
                        found_any = True
        except:
            continue

    if not found_any:
        send_telegram_msg("বর্তমানে নতুন কোনো সার্কুলার পাওয়া যায়নি।")

if __name__ == "__main__":
    scrape_jobs()
  
