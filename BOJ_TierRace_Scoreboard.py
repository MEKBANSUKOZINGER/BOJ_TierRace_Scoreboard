'''
          _______.____    __    ____  ______    .______     ______          __          
         /       |\   \  /  \  /   / /      |   |   _  \   /  __  \        |  |         
 ______ |   (----` \   \/    \/   / |  ,----'   |  |_)  | |  |  |  |       |  |  ______ 
|______| \   \      \            /  |  |        |   _  <  |  |  |  | .--.  |  | |______|
     .----)   |      \    /\    /   |  `----.   |  |_)  | |  `--'  | |  `--'  |         
     |_______/        \__/  \__/     \______|   |______/   \______/   \______/          
.___________. __   _______ .______         .______          ___       ______  _______   
|           ||  | |   ____||   _  \        |   _  \        /   \     /      ||   ____|  
`---|  |----`|  | |  |__   |  |_)  |       |  |_)  |      /  ^  \   |  ,----'|  |__     
    |  |     |  | |   __|  |      /        |      /      /  /_\  \  |  |     |   __|    
    |  |     |  | |  |____ |  |\  \----.   |  |\  \----./  _____  \ |  `----.|  |____   
    |__|     |__| |_______|| _| `._____|   | _| `._____/__/     \__\ \______||_______|  
                                                    
2024 / 10 / 09 Made by Dongjun Shin
- Unauthorized distribution is prohibited. -
'''

# To edit notion
from notion.client import NotionClient
from notion.block import CollectionViewBlock

# To read BOJ solved.ac API
import requests
import json

# To read google form answers (exported in csv file)
import csv

# Put csv file in same directory with this .py file. (Name must be [Info.csv])
csvFile = open('Info.csv', 'r', encoding='cp949')
reader = csv.reader(csvFile)

BOJ_TOTAL_INFO = {}

for line in reader :
    tempDict = {}
    tempDict["Name"] = line[1]
    tempDict['ID'] = line[2]
    tempDict['OriginTier'] = line[3]
    BOJ_TOTAL_INFO[line[0]] = tempDict
# Year 2024 - 2nd semester BOJ Tier Race participants Info

BOJ_TIERS = [
             'Unranked',                                                               # Unranked
             'Bronze V', 'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I',           # Bronzes
             'Silver V', 'Silver IV', 'Silver III', 'Silver II', 'Silver I',           # Silvers
             'Gold V', 'Gold IV', 'Gold III', 'Gold II', 'Gold I',                     # Golds
             'Platinum V', 'Platinum IV', 'Platinum III', 'Platinum II', 'Platinum I', # Platinums
             'Diamond V', 'Diamond IV', 'Diamond III', 'Diamond II', 'Diamond I',      # Diamonds
             'Ruby V', 'Ruby IV', 'Ruby III', 'Ruby II', 'Ruby I',                     # Rubies
             'Master',                                                                 # Master
            ]

# Score per tier
BOJ_SCORES = [0,0,1,2,3,4,5,7,9,11,13,15,18,21,24,27,30,35,40,45,50,55,65,75,75,75,75,75,75,75,75,75]

# For all users
for user in BOJ_TOTAL_INFO.keys():
    # Search user information in solved.ac
    _BOJ_USER_URL = f"https://solved.ac/api/v3/search/user?query={BOJ_TOTAL_INFO[user]['ID']}"
    userInfo = requests.get(_BOJ_USER_URL)
    userTemp = json.loads(userInfo.content.decode('utf-8')).get('items')
    if len(userTemp) > 1 :
        for userDict in userTemp :
            if userDict['handle'] == BOJ_TOTAL_INFO[user]["ID"] :
                userTemp = [userDict]
    # If user did nothing, set all 0
    if userTemp == [] :
        BOJ_TOTAL_INFO[user]["CurrentTier"] = BOJ_TIERS[0]
        BOJ_TOTAL_INFO[user]["Score"] = 0
        continue

    # Set user's current tier and it's score
    userTierIndex = userTemp[0]['tier']
    userTier = BOJ_TIERS[userTierIndex]
    BOJ_TOTAL_INFO[user]["CurrentTier"] = userTier
    userScore = 0
    while BOJ_TIERS[userTierIndex] != BOJ_TOTAL_INFO[user]["OriginTier"] :
        if userTierIndex == 1 or userTierIndex == 0 : 
            break
        userScore += BOJ_SCORES[userTierIndex]
        userTierIndex -= 1
    # For debug
    print(f"origin tier is {BOJ_TOTAL_INFO[user]['OriginTier']}, and current tier is {BOJ_TOTAL_INFO[user]['CurrentTier']}, so score is {userScore}")
    BOJ_TOTAL_INFO[user]["Score"] = userScore

# For debug
print(BOJ_TOTAL_INFO)

# You can find token in notion website -> development kit -> cookies -> token_v2.
MY_TOKEN = 'v02%3Auser_token_or_cookies%3Ajluj_mPB5Kf3sJHLJ5_TAN3bwHNmBiJWvkri84hd50s9rCtlMJfOY0PVbXEn7vDH__r2IkofkmHtuvSk1N0ADzK-W_ewOsm_jVnSYvJ6wv6jdaS6uT3JXWsUbU7kgONGxhQ0%2B%2Bv03%3AeyJhbGciOiJkaXIiLCJraWQiOiJwcm9kdWN0aW9uOnRva2VuLXYzOjIwMjQtMDctMTAiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0..c68b0RMfr6bzTkCS69bFDA.mLL1k6Qb3eSw5tiC0wF_H-sK6hWlWRGAng7qjLq3d-7ZDSFPKWFYolA7I_e0ed2ch4BiCzh0WgYNV6YiG0E60YO2GWyeKg_vlFgMu6eAlQ8dVZ2I2RFl33ugBPwK-LoHD6CiySWMljVn5CJw-ybot0GnKwEwz2CJnbfw4iSgt2NF2uoTXC3nxO0H7HI6fNhzL0PM0kSIj_8CJEpk7iChHUYV-g5WnA2JKXHx0suoau1g3MXaKd2SWgHkKbKZhcdKXMVz44ClW1gG9xEiual3nnqVP4zxOFBU3tGzraNoS8rPJqA1zHo3YHz-5AHmohIx.XzkZKrnylRP-BDuauZCTPf70IPpA8-RZ6tcGoacfc2A'
# URL of notion page that will be used. (test page is recommended.) / ! Not the website publish link !
_PAGE_URL = 'https://www.notion.so/yaejida/Refresh-Leaderboard-0e9cedb217b444548fbea84113185e09?pvs=4'

'''
-------- Notion selection tag color query ---------
- Default
- Gray
- Brown
- Orange
- Yellow
- Green
- Blue
- Purple
- Red
---------------------------------------------------
'''

def ScoreBoard() :
    return {
        # Title type name
        "title" : {"name" : "이름", "type" : "title"},
        # Select type original tier
        "priority1" : {"name" : "시작티어", "type" : "select",
            "options" : [
                {
                    "color" : "default",
                    "value" : "Unranked",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze V",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze IV",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze III",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze II",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze I",
                },
                {
                    "color" : "gray",
                    "value" : "Silver V",
                },
                {
                    "color" : "gray",
                    "value" : "Silver IV",
                },
                {
                    "color" : "gray",
                    "value" : "Silver III",
                },
                {
                    "color" : "gray",
                    "value" : "Silver II",
                },
                {
                    "color" : "gray",
                    "value" : "Silver I",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold V",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold IV",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold III",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold II",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold I",
                },
                {
                    "color" : "green",
                    "value" : "Platinum V",
                },
                {
                    "color" : "green",
                    "value" : "Platinum IV",
                },
                {
                    "color" : "green",
                    "value" : "Platinum III",
                },
                {
                    "color" : "green",
                    "value" : "Platinum II",
                },
                {
                    "color" : "green",
                    "value" : "Platinum I",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond V",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond IV",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond III",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond II",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond I",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby V",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby IV",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby III",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby II",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby I",
                },
                {
                    "color" : "purple",
                    "value" : "Master",
                }
            ]},
        # Select type current tier
        "priority2" : {"name" : "현재티어", "type" : "select",
            "options" : [
                {
                    "color" : "default",
                    "value" : "Unranked",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze V",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze IV",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze III",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze II",
                },
                {
                    "color" : "brown",
                    "value" : "Bronze I",
                },
                {
                    "color" : "gray",
                    "value" : "Silver V",
                },
                {
                    "color" : "gray",
                    "value" : "Silver IV",
                },
                {
                    "color" : "gray",
                    "value" : "Silver III",
                },
                {
                    "color" : "gray",
                    "value" : "Silver II",
                },
                {
                    "color" : "gray",
                    "value" : "Silver I",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold V",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold IV",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold III",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold II",
                },
                {
                    "color" : "yellow",
                    "value" : "Gold I",
                },
                {
                    "color" : "green",
                    "value" : "Platinum V",
                },
                {
                    "color" : "green",
                    "value" : "Platinum IV",
                },
                {
                    "color" : "green",
                    "value" : "Platinum III",
                },
                {
                    "color" : "green",
                    "value" : "Platinum II",
                },
                {
                    "color" : "green",
                    "value" : "Platinum I",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond V",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond IV",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond III",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond II",
                },
                {
                    "color" : "blue",
                    "value" : "Diamond I",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby V",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby IV",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby III",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby II",
                },
                {
                    "color" : "pink",
                    "value" : "Ruby I",
                },
                {
                    "color" : "purple",
                    "value" : "Master",
                }
            ]} ,
        # number type current score
        "score" : {"name" : "점수", "type" : "number"},
        #"bjid" : {"name" : "백준아이디", "type" : "rich_text"},
    }

# Run
if __name__ == '__main__' :
    client = NotionClient(token_v2=MY_TOKEN)
    page = client.get_block(_PAGE_URL)

    # Create new table block
    child = page.children.add_new(CollectionViewBlock)
    child.collection = client.get_collection(
        client.create_record(
            "collection", parent=child, schema = ScoreBoard()
        )
    )
    child.title='백준 티어 레이스 리더보드'
    child.views.add_new(view_type="table")

    # For garbage value
    init = True

    # Enter all participants' information in notion table
    for participants in BOJ_TOTAL_INFO.keys() :
        if not init :
            #print(BOJ_TOTAL_INFO[participants]["Name"])
            row = child.collection.add_row()
            row.set_property("title", BOJ_TOTAL_INFO[participants]["Name"])
            #print(BOJ_TOTAL_INFO[participants]["OriginTier"])
            row.set_property("priority1", BOJ_TOTAL_INFO[participants]["OriginTier"])
            #print(BOJ_TOTAL_INFO[participants]["CurrentTier"])
            row.set_property("priority2", BOJ_TOTAL_INFO[participants]["CurrentTier"])
            #print(BOJ_TOTAL_INFO[participants]["Score"])
            row.set_property("score", BOJ_TOTAL_INFO[participants]["Score"])
        init = False


