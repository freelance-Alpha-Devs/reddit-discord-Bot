from re import sub
import praw
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import filtering
import os
import webhookURLs
import redditAcc

restartTime = 5
seenPostPath = "seen.txt"

# made for docker, if the environment variable doesn't exist use default forhire
envToken = os.environ.get("SUBREDDIT", False)
subreddit = envToken if envToken else "forhire"

subreddit_list = [
    "forhire",
]


def main():
    global subreddit

    reddit = praw.Reddit(
        client_id=redditAcc.client_id,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        client_secret=redditAcc.client_secret
    )
    while True:
        run_collector(reddit, subreddit)


def run_collector(reddit, subreddits):
    print("job collector started")
    try:
        job_collector(reddit, subreddits)
    except Exception as error:
        print("Error running the collector. Please take a look at the error given below. \n")
        print(error)
        log_errors(error)
        print(f"\nWaiting {restartTime} minutes before retrying")
        time.sleep(restartTime*60)


def log_errors(error):
    with open("debug.log", "a") as file:
        file.write(str(error.args) + "\n")


def job_collector(reddit, subreddits):
    subreddit = reddit.subreddit(subreddits)
    for submission in subreddit.stream.submissions(skip_existing=False,):
        print("the submission found: " )
        print(submission)
        process_submission(submission)


def process_submission(submission):
    print("submission processor started")
    title = str(submission.title.upper())
    if title.find("[HIRING]") != -1:
        post_job(submission)


def post_job(submission, waitTime = restartTime): #waitTime in minutes
    global subreddit
    print("job poster started")

    file = open(seenPostPath, "a+")
    file.seek(0)
    readed = file.read()

    id = str(submission.id)
    title = str(submission.title)
    contentOriginal = str(submission.selftext)
    author = str(submission.author)
    timestamp = submission.created

    if readed.find(id) == -1:
        content = title + contentOriginal

        content = content.lower()
        state = False

        for i in filtering.blackList:
            if content.find(i) != -1:
                state = True
                break

        if state:
            for j in filtering.whiteList:
                if content.find(f" {j} ") != -1:
                    state = False
                    break
        if not state:
            # if the job is related to programming
            url = webhookURLs.urls.incoming
        else:
            url = webhookURLs.urls.incoming_unrelated

        webhook = DiscordWebhook(url=url)
        if len(contentOriginal) > 1800:
            contentOriginal = contentOriginal[:1800] + "..."

        embed = DiscordEmbed(title=title, description=str(contentOriginal)[:1800],
                             color='03b2f8')
        embed.set_author(name=f'u/{author}')
        embed.set_timestamp(timestamp=timestamp)
        embed.add_embed_field(name=f"https://reddit.com/r/{subreddit}/comments/{id}",
                              value=f"https://reddit.com/u/{author}")
        webhook.add_embed(embed)
        response = webhook.execute()
        if response.status_code == 200:
            file.write(id + "\n")
        else:
            print(f"there was an error with the webhook, waiting {waitTime} seconds")
            time.sleep(waitTime*60)

    file.close()
    with open(seenPostPath, 'r') as fin:
        data = fin.read().splitlines(True)
    fin.close()
    if len(data) > 100:
        with open(seenPostPath, 'w') as fout:
            fout.writelines(data[1:])
        fout.close()


if __name__ == "__main__":
    main()