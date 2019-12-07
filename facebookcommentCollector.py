from requests import *
from time import sleep
from re import *
from bs4 import *
from time import sleep
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000
csvfile = open('audience.txt',"w")
csvfile.write('|token id |\t|full name of user|\t|content comment|\t|cursor_comment|\n')

o = 1
import json

url_login = 'https://www.facebook.com/login/device-based/regular/login'
url_ajax = 'https://www.facebook.com/api/graphql/'

session = Session()
email = '***********************'
password = '**************************************'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Referer': url_login

}

cookies = {
    "datr": ''

}

data = {

    'jazoest': '',
    'lsd': '',
    'legacy_return': '',
    'lgnrnd': '',
    'lgnjs': '',
    'email': email,
    'pass': password
}




def parse_post(session, header, cookie, id, hash,doc_id):
    jojo = {
   "after":None,
   "before":None,
   "commentProfilePictureSizeDepth0":32,
   "commentProfilePictureSizeDepth1":20,
   "displayCommentsFeedbackContext":{
      "bump_reason":None,
      "comment_expand_mode":3,
      "comment_permalink_args":{
         "comment_id":None,
         "reply_comment_id":None
      },
      "interesting_comment_fbids":[],
      "is_location_from_search":False,
      "last_seen_time":None,
      "log_ranked_comment_impressions":False,
      "probability_to_comment":0,
      "story_location":9,
      "story_type":0
   },
   "displayCommentsContextEnableComment":None,
   "displayCommentsContextIsAdPreview":None,
   "displayCommentsContextIsAggregatedShare":None,
   "displayCommentsContextIsStorySet":None,
   "feedLocation":None,
   "feedbackID":"",
   "feedbackSource":17,
   "first":None,
   "focusCommentID":None,
   "includeNestedComments":True,
   "isInitialFetch":False,
   "isComet":False,
   "containerIsFeedStory":True,
   "containerIsWorkplace":False,
   "containerIsLiveStory":False,
   "containerIsTahoe":False,
   "last":None,
   "scale":1,
   "topLevelViewOption":None,
   "useDefaultActor":True,
   "viewOption":"RANKED_UNFILTERED",
   "UFI2CommentsProvider_commentsKey":None
}
    has_next_line = True
    after=None
    end=None

    jojo['displayCommentsFeedbackContext']='{"bump_reason":null,"comment_expand_mode":3,"comment_permalink_args":{"comment_id":null,"reply_comment_id":null},"interesting_comment_fbids":[],"is_location_from_search":false,"last_seen_time":null,"log_ranked_comment_impressions":false,"probability_to_comment":null,"story_location":null,"story_type":null}'
    jojo['feedbackID']=hash
    while has_next_line == True:

        ro = session.post(url_ajax, headers=headers, cookies=cookies, data={
            "fb_dtsg": fb_dtsg,
            "__a": "1",
            "__user": cookies['c_user'],
            "av":cookies["c_user"],
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "UFI2CommentsProviderPaginationQuery",
            'variables':json.dumps(jojo),
            "doc_id": doc_id

        })

        js = json.loads(ro.text)
        has_next_line = js['data']['feedback']['display_comments']["page_info"]['has_next_page']
        if js['data']['feedback']['display_comments']['edges'] != []:
            after = js['data']['feedback']['display_comments']['edges'][len(js['data']['feedback']['display_comments']['edges'])-1]['cursor']
        else:
            after=""
        end = js['data']['feedback']['display_comments']["page_info"]['end_cursor']
        jojo['before']=end
        jojo['after']=after
        print("homw much people comment : "+str(js['data']['feedback']['display_comments']['count']))
        print('*********************************************************************************')
        for d in js['data']['feedback']['display_comments']['edges']:
            if d['node']['__typename'] == 'Comment':
                try:

                    csvfile.write("["+str(d['node']['author']['id'])+"\\"+d['node']['legacy_fbid']+"] "+"["+d['node']['author']['name']+"]  ["+d['node']['body']['text']+"]\t\t["+d['cursor']+"]\n")
                    print('['+d['node']['author']['id']+"]")
                    print(d['node']['author']['name'])
                    print(d['node']['body']['text'])
                except:
                    print('')

def enter_inside_post(session, headers, cookies, id, hash,doc_id):
    data["variables"] = '{"feedbackTargetID":"' + hash + '"}'
    ro = session.post(url_ajax, headers=headers, cookies=cookies, data={
        "fb_dtsg": fb_dtsg,
        "__a": "1",
        "__user": cookies['c_user'],
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "UFI2SharesCountTooltipContentQuery",
        "variables": '{"feedbackTargetID":"' + hash + '"}',
        "doc_id": "*****************"

    })
    js = json.loads(ro.text)
    for ids in js["data"]["feedback"]["legacy_resharers"]:
        if ids["__typename"] == "User":
            print("[" + ids["id"] + "] " + ids["name"] + " is share this post ! ")


res = session.get(url_login)

b = BeautifulSoup(res.text, 'html.parser')

ins = b.find_all('input')

for input in ins:
    try:
        if input['name'] == 'jazoest' or input['name'] == 'lsd' or input['name'] == 'lgnrnd' or input[
            'name'] == 'lgnjs':
            data[input['name']] = input['value']
    except KeyError:
        print('')

res = session.post(url_login, headers=headers, cookies=session.cookies.get_dict(), data=data)

cookies = session.cookies.get_dict()

target_pg = 'https://www.facebook.com/pg/adidas/photos/'
page_id = "********************"

headers['Referer'] = 'https://www.facebook.com/'
res = session.get(target_pg, headers=headers, cookies=cookies)

fb_dtsg = findall('"token":"([a-zA-Z0-9\-\._:,;]+)', res.text)[0]

cursors = findall('cursor:"([a-zA-Z0-9\-\._:,;]+)', res.text)
print(cursors)

headers['Referer'] = target_pg
ping_cursor = cursors[5]
res = session.post(url_ajax, headers=headers, cookies=cookies, data={
    "fb_dtsg": fb_dtsg,
    "__a": "1",
    "__user": cookies['c_user'],
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "PagePhotosTabAllPhotosGridPaginationQuery",
    "variables": '{"count":28,"cursor":"' + ping_cursor + '","pageID":"' + page_id + '"}',
    "doc_id": "*************************"

})

js = json.loads(res.text)
ping_cursor = js["data"]["page"]["posted_photos"]["page_info"]["end_cursor"]
has_next_page = js["data"]["page"]["posted_photos"]["page_info"]["has_next_page"]

for edge in js["data"]["page"]["posted_photos"]["edges"]:
    print("Reactor : " + str(edge["node"]["feedback"]["reactors"]["count"]) + " feedback_ID = " +
          edge["node"]["feedback"]["id"])
    parse_post(session, headers, cookies, edge["node"]["id"], edge["node"]["feedback"]["id"],"2711243315563730")

print("[*] sleep  30 second !")
sleep(30)

while has_next_page:
    print("===============================================================================================================================================================")
    res = session.post(url_ajax, headers=headers, cookies=cookies, data={
        "fb_dtsg": fb_dtsg,
        "__a": "1",
        "__user": cookies['c_user'],
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PagePhotosTabAllPhotosGridPaginationQuery",
        "variables": '{"count":28,"cursor":"' + ping_cursor + '","pageID":"' + page_id + '"}',
        "doc_id": "1887586514672506"})
    js = json.loads(res.text)
    ping_cursor = js["data"]["page"]["posted_photos"]["page_info"]["end_cursor"]
    has_next_page = js["data"]["page"]["posted_photos"]["page_info"]["has_next_page"]

    for edge in js["data"]["page"]["posted_photos"]["edges"]:
        winsound.Beep(frequency, duration)
        print("Reactor : " + str(edge["node"]["feedback"]["reactors"]["count"]) + " feedback_ID = " +
              edge["node"]["feedback"]["id"])
        parse_post(session, headers, cookies, edge["node"]["id"], edge["node"]["feedback"]["id"],"2711243315563730")

    print("[*] sleep  30 second !")
    sleep(30)


session.post('https://www.facebook.com/login/device-based/regular/logout', headers=headers, cookies=cookies,
                 data={'fb_dtsg': fb_dtsg})


csvfile.close()