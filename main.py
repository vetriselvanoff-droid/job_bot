import requests
import feedparser

BOT_TOKEN = "8279026565:AAE05nA3h_X02HPAdGSVuE8oo6bnM92izYE"
CHAT_ID = "@upgradedaily_jobs"

RAPID_API_KEY = "083ab6f14cmshe7666f791b52a5bp1b335ejsn95c3333c490"


# -------------------------
# TELEGRAM
# -------------------------
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


# -------------------------
# RAPIDAPI INDIA JOBS
# -------------------------
def fetch_api_jobs(role):
    url = "https://jsearch.p.rapidapi.com/search"

    params = {
        "query": role,
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": "083ab6f14cmshe7666f791b52a5bp1b335ejsn95c3333c490"
    }

    res = requests.get(url, headers=headers, params=params).json()

    jobs = []

    for job in res.get("data", [])[:5]:
        title = job["job_title"]
        company = job["employer_name"]
        city = job["job_city"]
        link = job["job_apply_link"]

        jobs.append((f"{title} – {company} – {city}", link))

    return jobs


# -------------------------
# RSS JOBS
# -------------------------
def fetch_rss(url):
    feed = feedparser.parse(url)
    jobs = []

    for job in feed.entries[:5]:
        jobs.append((job.title, job.link))

    return jobs


# -------------------------
# COMBINE ALL SOURCES
# -------------------------
def get_all_jobs():
    roles = [
        "software engineer india",
        "frontend developer india",
        "backend developer india",
        "python developer india",
        "devops engineer india",
        "qa engineer india",
        "cloud engineer india",
        "fresher software engineer india"
    ]

    all_jobs = []

    # API jobs
    for role in roles:
        all_jobs += fetch_api_jobs(role)

    # RSS jobs (backup)
    all_jobs += fetch_rss("https://www.python.org/jobs/feed/rss/")
    all_jobs += fetch_rss("https://weworkremotely.com/remote-jobs.rss")

    return all_jobs


# -------------------------
# FORMAT
# -------------------------
def format_jobs(jobs):
    # remove duplicates by link
    unique = list({link: (title, link) for title, link in jobs}.values())

    text = "🔥 India IT Jobs Daily\n\n"

    for i, (title, link) in enumerate(unique[:25], 1):
        text += f"{i}. {title}\n{link}\n\n"

    return text


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    jobs = get_all_jobs()
    message = format_jobs(jobs)
    send_message(message)

