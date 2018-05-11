Welcome to read me, I hope you enjoy reading me

This is a little bot to help reward people who help out in communit accounts. I personally am very forgetful so this bot is here to help thank those that keep our communities ticking.

Pre-requisite
Need to have:
python 
steem-python

To make it work: 
Download
Change filename keys.example.py to keys.py.

In keys.py
Put your private posting key as a string in front of =

In rewards.py
accountname - Put your posting account name here
targeted_tag - put the tag you're interested in monitoring here
judges and curator files. links to the files this allows two different voting levels to be set for different people.
Vote_Power - how much to upvote each person in either category
min_limit - number of comments required for person to qualify for an upvote
num_upvotes- number of upvotes to give for each person

exit.

Set up a cron job to run script every 24 hours. 

Bot will check every person in judges and curators list and count how many times they commented on a post withing the specific tag.
if they meet the minimum criteria then it will upvote a number of their comments in the tag. 
