import requests
import feedparser

BOT_TOKEN = "8279026565:AAE05nA3h_X02HPAdGSVuE8oo6bnM92izYE"
CHAT_ID = "@upgradedaily_jobs"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)


def fetch_jobs():
    feed = feedparser.parse("https://weworkremotely.com/remote-jobs.rss")

    jobs_text = "🔥 Daily Remote Jobs\n\n"

    count = 0
    for job in feed.entries[:10]:
        count += 1
        jobs_text += f"{count}. {job.title}\n{job.link}\n\n"

    return jobs_text


if __name__ == "__main__":
    message = fetch_jobs()
    send_message(message)
