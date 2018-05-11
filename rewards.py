

from steem import steem as st
from steem import steemd as std
from steem.account import Account

from steem.post import Post

import datetime
import calendar
import time
import random

# import keys
try: from keys import Posting_Key as posting_key
except: posting_key = ['PRIV POSTING KEY HERE']

#accountname = 'idikuci'
#accountname = 'comedyopenmic'
accountname = ['Account Name Here']

#targeted_tag = 'comedyopenmic'
targeted_tag = ['tag being monitored']

# Variables:
judgesfile = './projects/rewards/judges.txt'
curatorsfile = './projects/rewards/curators.txt'
Vote_Power = [2, 1] # Vote power for different categories of people (currently 2)
min_limit = ['Var 1'] # Minimum number of comments required to get rewarded
num_upvotes = ['Var 2'] # Number of upvotes given per day


rewardees = []


nodes = ['rpc.buildteam.io',"steemd.minnowsupportproject.org","rpc.steemliberator.com","rpc.steemviz.com"]
pattern = '%Y-%m-%dT%H:%M:%S'

# cut off time in seconds
cutofftime = 86400 # Cutoff 24hrs

# Read in values from file (update list of people we're tracking)
def read_writers(filename='~/projects/rewards/judges.txt'):
    following = []

    readit = False
    with open(filename,'r') as file:
        for line in file:
            if not readit:
                readit = True
                continue
            # remove new line char
            following.append(line[:-1])

    return following

def epochVote(e):
#    return (time.mktime(time.strptime(e['timestamp'], pattern)))
    return (calendar.timegm(time.strptime(e['timestamp'], pattern)))

def epochDiff():
    # Get current UTC time in seconds
    now = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    epoch_diff = (now - epoch).total_seconds()

    return (epoch_diff)

def getUpvoteCandidate(account):
    """ Gets link to comments author has not voted on but is within voting window
    Args:
        account: A Steem Account object.
    Returns:
        identifier of posts/comments within voting window not already voted on
    """
    # Make sure we have the latest data
    account.refresh()
    epoch_last_vote = 0

    # Get last 2000 votes from account
    history = account.get_account_history(-1,1000,filter_by='comment')

    current_time = epochDiff()
    oldest_id = []
    print('got history, now filtering...')
    for event in history:
        try:
            # Make sure we are the author
            if(event['author'] == account.name):
                # Not really needed due to filter
                if(event['type'] == 'comment'):
                    # Double confirmation of comment
                    if event['permlink'].startswith("re-"):
                        epoch_last_vote = epochVote(event)
                        elapsed_time = current_time - epoch_last_vote
                        # Is post in within time limit
                        if elapsed_time < cutofftime:
                            # Get details of main post
                            identifier = "@" + event['parent_author'] + "/" + event['parent_permlink']
                            parent = Post(identifier,s)
                            while not parent.is_main_post():
                                identifier = "@" + parent['parent_author'] + "/" + parent['parent_permlink']
                                parent = Post(identifier,s)
                            # Make sure Original post is in desired tag
                            if targeted_tag in parent['tags']:
                                identifier = "@" + event['author'] + "/" + event['permlink']
                                # Store comment if it meets conditions
                                oldest_id.append(identifier)
                        else:
                            # Everything else will be older than cutoff
                            break
        except Exception as e:
            print('issue with history: ' + str(e))
#    print(oldest_id)
    print('completed history search')
    return list(reversed(oldest_id))


# Main Work here:

# Power up Steem
s = st.Steem(nodes=nodes)
upvoter = st.Steem(nodes=nodes, keys=posting_key)

#Read in list of people to upvote.
judge = read_writers(judgesfile)
curate = read_writers(curatorsfile)

# Append to create list
rewardees.append(judge)
rewardees.append(curate)

# go through list of beneficiaries and upvote them
for idx, votinglist in enumerate(rewardees):
    for acc in votinglist:
        account = Account(acc, s)
        posts = getUpvoteCandidate(account)
        # confirm number of comments made
        if len(posts) >= min_limit:
            selection = random.shuffle(posts)
            voted = 0
            votingon = 0
            # vote on comments
            while voted < num_upvotes:
                things = posts[votingon]
                votingon += 1
                P = Post(things,upvoter)
                # make sure not already voted on
                if not accountname in P['active_votes']:
                    try:
                        print('upvote: ' + str(things) + ' / ' + str(Vote_Power[idx]) + '%... ', end='',flush=True)
                        P.upvote(Vote_Power[idx], accountname)
                        voted += 1
                        print('Success')
                        # sleep for 5 seconds, make sure we can vote again
                        time.sleep(5)
                    except Exception as e:
                        print("Error Voting: " + str(e))
