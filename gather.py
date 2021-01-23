from datetime import datetime
import time
import praw
import json
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

def getTop15(log):
    my_secret = 'CV7Ui4ZdwpufqtXMOAIjhaZtbHySpw'
    my_client_id = "jezvxuib__DnCQ"
    my_user_agent = "windows:wsbprediction:v1.0.1 (by u/ItsNotDrew)"

    reddit = praw.Reddit(
        client_id=my_client_id,
        client_secret=my_secret,
        user_agent=my_user_agent
    )

    fields = ('author', 'created_utc', 'distinguished', 'id', 'is_original_content', 'is_self'
              , 'link_flair_text', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'score', 'selftext'
              , 'stickied', 'title', 'upvote_ratio', 'url', 'total_awards_received', 'gildings')

    log.debug("Gathering Hot 15")
    submissions = reddit.subreddit("wallstreetbets").hot(limit=15)

    list_top_15 = []
    log.debug("Iterating through submissions")
    for sub in submissions:
        to_dict = vars(sub)
        sub_dict = {field: to_dict[field] for field in fields}
        sub_dict['author'] = sub_dict['author'].name
        list_top_15.append(sub_dict)
    return list_top_15


def writeFile(time,posts,log):
    date = datetime.now()
    file_name = "top-15-"+str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"-"+str(time[0])+"-"+str(time[1])
    log.debug("writing file" + file_name)
    file = open(file_name,'w')
    try:
        json.dump(posts, file)
        log.debug("Successfully written file")
        return True
    except:
        print()
        log.debug("Failure while writing file")
        return False


def gatherPosts(time):
    return True

def initialize_logging():
    filename = 'primary.log'
    handlers_log = [logging.FileHandler(filename), logging.StreamHandler()]
    format_log = '%(asctime)s %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=format_log, handlers=handlers_log)


def main():

    initialize_logging()

    time_keeper = {"nine": False,"nine_thirty": False,"eleven": False,"one": False,"four": False,"ten": False}
    while(True):
        curr_time = datetime.now()
        logging.debug("Checking to see if time to gather posts")

        if curr_time.hour == 9 and curr_time.minute > 30 and time_keeper["nine_thirty"] == False:
            logging.info("Gathering posts at 9:30")
            top = getTop15(logging)
            writeFile((9, 3), top, logging)
            time_keeper['nine_thirty'] = True
        elif curr_time.hour == 11 and curr_time.minute > 0 and time_keeper["eleven"] == False:
            logging.info("Gathering posts at 11:00")
            top = getTop15(logging)
            writeFile((11, 0), top, logging)
            time_keeper['eleven'] = True
        elif curr_time.hour == 13 and curr_time.minute > 0 and time_keeper["one"] == False:
            logging.info("Gathering posts at 13:00")
            top = getTop15(logging)
            writeFile((13, 0), top, logging)
            time_keeper['one'] = True
        elif curr_time.hour == 16 and curr_time.minute > 0 and time_keeper["four"] == False:
            logging.info("Gathering posts at 16:00")
            top = getTop15(logging)
            writeFile((16, 0), top, logging)
            time_keeper['four'] = True
        elif curr_time.hour == 16 and curr_time.minute > 0 and time_keeper["four"] == False:
            logging.info("Gathering posts at 16:00")
            top = getTop15(logging)
            writeFile((16, 0), top, logging)
            time_keeper['four'] = True
        elif curr_time.hour == 0 and curr_time.minute < 2:
            logging.debug("Reseting time_keeper")
            time_keeper = dict.fromkeys(time_keeper,False)

        #Sleep for 30 seconds
        time.sleep(30)


    return 0


if __name__ == "__main__":
    #execute only if run as a script
    main()