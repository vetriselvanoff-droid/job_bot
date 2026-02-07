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
        "X-RapidAPI-Key": RAPID_API_KEY
    }

    res = requests.get(url, headers=headers, params=params).json()

    posts = []

    for job in res.get("data", []):

        country = job.get("job_country", "")
        city = job.get("job_city", "").lower()
        state = job.get("job_state", "").lower()
        country = job.get("job_country", "").lower()

        if not any(x in (city + state + country) for x in ["india", "bangalore", "chennai", "hyderabad", "pune", "mumbai", "delhi"]):
         continue


        title = job.get("job_title", "N/A")
        company = job.get("employer_name", "N/A")

        city = job.get("job_city", "")
        state = job.get("job_state", "")
        location = f"{city}, {state}"

        remote = "Remote" if job.get("job_is_remote") else "Onsite"
        job_type = job.get("job_employment_type", "Full-time")

        desc = job.get("job_description", "")
        desc = desc[:300] + "..." if len(desc) > 300 else desc

        link = job.get("job_apply_link", "")

        message = (
            f"💼 {title}\n\n"
            f"🏢 Company: {company}\n"
            f"📍 Location: {location}\n"
            f"🕒 Type: {job_type} | {remote}\n\n"
            f"📝 Details:\n{desc}\n\n"
            f"🔗 Apply:\n{link}"
        )

        posts.append(message)

    return posts


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

    all_posts = []

    for role in roles:
        all_posts += fetch_api_jobs(role)

    return all_posts



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

if not jobs:
        send_message("⚠️ No jobs found today. API returned empty.")
else:
        for job_post in jobs[:10]:
            send_message(job_post)
import time

jobs = get_all_jobs()

for job_post in jobs[:10]:   # send 10 jobs max daily
    send_message(job_post)
    time.sleep(3)





