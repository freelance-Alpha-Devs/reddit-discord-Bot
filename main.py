import asyncpraw
import requests
import asyncio
import configs
from discord_webhook import DiscordWebhook, DiscordEmbed
import time


jobQueue: asyncio.Queue
retry = 60  # retry after 1 minute
failExtra = 10  # wait 10 times the retry length after failing problemMax times
problemMax = 20  # failing times


async def main():
    global jobQueue
    jobQueue = asyncio.Queue()

    poster = asyncio.create_task(job_poster())

    reddit = asyncpraw.Reddit(
        client_id="AjOIfP4opzcd-w",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        client_secret="ZC6wBk25DprOIBqjoEuTu1x7yOAD_A"
    )

    await run_collector(reddit)

    await poster


async def run_collector(reddit, restart=0):
    print("job collector started")
    try:
        await job_collector(reddit)
    except Exception as err:
        print("error encountered in job collector")
        print(err)
        if restart >= problemMax:
            print(f"waiting {retry * failExtra} seconds before retrying")
            await asyncio.sleep(retry * failExtra)  # wait more
            restart = -1
            # todo implement some reporting path and maybe exit instead of restarting
        else:
            print(f"waiting {retry} seconds before retrying")
        await asyncio.sleep(retry)
        print("restarting:", end=" ")
        await run_collector(reddit, restart + 1)


async def job_collector(reddit):
    subreddit = await reddit.subreddit("forhire")
    async for submission in subreddit.stream.submissions():
        await process_submission(submission)


async def process_submission(submission):
    global jobQueue
    title = str(submission.title.upper())
    if title.find("[HIRING]") != -1:
        text = submission.selftext
        data = {
            "username": str(submission.author),
            "title": submission.title,
            "content": text,
            "id": submission.id,
        }

        await jobQueue.put(data)

# doing the posting separately in case the
async def job_poster():
    global jobQueue
    print("job poster started")
    while True:
        item = await jobQueue.get()
        if item is None:
            # use none to break out
            break

        print(f"job listed: {item}")
        webhook = DiscordWebhook(
            url='https://discordapp.com/api/webhooks/826045724809887774/DEbM7HPU5xiEX_WZnEZ21JfTWRMWyAh6fqbgIEIbB2jEJzceEbDz89fLWvR29PDiVFlA',)

        print(item["title"])

        embed = DiscordEmbed(title=item["title"], description = str(item["content"])[:1800],color='03b2f8')

        embed.set_author(name=f'u/{item["username"]}')

        embed.set_timestamp()

        embed.add_embed_field(name="https://reddit.com/r/forhire/comments/"+ item["id"], value="https://reddit.com/u/"+item["username"])

        webhook.add_embed(embed)

        response = webhook.execute()

if __name__ == "__main__":
    asyncio.run(main())

