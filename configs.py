file = open("subreddits.conf")
subreddits = file.read().split("\n")

for subreddit in subreddits:
    if subreddit == "":
        subreddits.remove(subreddit)
file.close()

file = open("backups.conf")
backups = file.read().split("\n")
backupsCopy = []

for backup in backups:
    if backup == "":
        backups.remove(backup)
    else:
        backupsCopy.append(backup.split("&"))

backupWeight = backupsCopy[0][0]
backupIps = backupsCopy[1:]

file.close()

if __name__ == "__main__":
    print(subreddits)
    print(backupWeight)
    print(backupIps)
