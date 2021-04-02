import praw
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import filtering

restartTime = 1

linux = False

if linux:
    seenPostPath = "/home/administrator/AlphaDevs/reddit-discord-Bot/seen.txt"
else:
    seenPostPath = "seen.txt"

subreddit_list = [
    "forhire",
]

debug = False

def main():
    global subreddit_list
    subreddits = ""
    for s in subreddit_list:
        subreddits += s + "+"
    subreddits = subreddits[:-1]

    reddit = praw.Reddit(
        client_id="AjOIfP4opzcd-w",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        client_secret="ZC6wBk25DprOIBqjoEuTu1x7yOAD_A"
    )
    run_collector(reddit, subreddits)

def run_collector(reddit, subreddits):
    print("job collector started")
    try:
        job_collector(reddit, subreddits)
    except Exception as error:
        print("Error running the collector. Please take a look at the error given below. \n")
        print(error)
        log_errors(error)
        print(f"\nWaiting {restartTime} seconds before retrying")
        time.sleep(restartTime)

def log_errors(error):
    with open("debug.log", "a") as file:
        file.write(str(error.args) + "\n")

def job_collector(reddit, subreddits):
    subreddit = reddit.subreddit(subreddits)
    for submission in subreddit.stream.submissions(skip_existing=False):
        print("the submission found: " )
        print(submission)
        process_submission(submission)

def process_submission(submission):
    print("submission processor started")
    title = str(submission.title.upper())
    if title.find("[HIRING]") != -1:
        post_job(submission)

def post_job(submission, waitTime = 0):
    print("job poster started")

    file = open(seenPostPath, "a+")
    #print("the problem is after opening the files")

    file.read()

    file.seek(0)
    readed = file.read()

    #print("the problem is after reading the file")

    id = str(submission.id)
    title = str(submission.title)
    content = str(submission.selftext)
    author = str(submission.author)

    if readed.find(id) == -1:

        content = title + content

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
        #print("the problem is after whitelist/black list")
        if not state:
            if not debug:
                url = 'https://discordapp.com/api/webhooks/826012159905366027/K7FZYc3ICVz9huzANY4xK0b2_8Se1Y96dZfpa-oif9C0LC2_uJn66VAeG-ju1ORmO1-t'  # programing related
            else:
                url = 'https://discordapp.com/api/webhooks/826805774474674337/6lZSS3_Ht6j1XSVQqZOQ063oxaJalHoKN9Hkwq7KC6VVdbqz4dkAIS4M_HJOULBPNvWa'
        else:
            if not debug:
                url = 'https://discordapp.com/api/webhooks/826082363997552650/fBYM_KPyenrAvPRy_kiLAQqljbkhWNq1GxHDQ1-iDdfnJJQzN9qEHOnjcMqt6-sdRICy'  # not related
            else:
                url = 'https://discordapp.com/api/webhooks/826805774474674337/6lZSS3_Ht6j1XSVQqZOQ063oxaJalHoKN9Hkwq7KC6VVdbqz4dkAIS4M_HJOULBPNvWa'

        webhook = DiscordWebhook(
            url=url, )
        embed = DiscordEmbed(title=title, description=str(content)[:1800],
                             color='03b2f8')
        embed.set_author(name=f'u/{author}')
        embed.set_timestamp()
        embed.add_embed_field(name="https://reddit.com/r/forhire/comments/" + id,
                              value="https://reddit.com/u/" + author)
        webhook.add_embed(embed)
        response = webhook.execute()
        if response.status_code == 200:
            file.write(id + "\n")
        else:
            print(f"there was an error with the webhook, waiting {waitTime} seconds")
            time.sleep(waitTime)
            post_job(submission, waitTime+1)
        #print("the problem is after sending the webhook")

    file.close()
    with open(seenPostPath, 'r') as fin:
        data = fin.read().splitlines(True)
    fin.close()
    #print("the problem is after fin.close()")
    if len(data) > 100:
        with open(seenPostPath, 'w') as fout:
            fout.writelines(data[1:])
        fout.close()
    #print("the problem is after testing length and writitng lines")

if __name__ == "__main__":
    main()