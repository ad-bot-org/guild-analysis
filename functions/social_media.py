from googlesearch import search
import requests
import json
import time as t

def get_sm(guild_name, config_path):
    with open(config_path, "r") as sm_file:
        j_sm = json.load(sm_file)
    social_media = {
        "youtube": {
            "status": None,
            "url": None
        },
        "twitch": {
            "status": None,
            "url": None
        },
        "instagram": {
            "status": None,
            "url": None
        }
    }
    for resp_url in search(guild_name, tld="com", num=20, stop=20, pause=1):
        is_untrue_url = False
        for s_k in j_sm["sm"]:
            if resp_url.find(j_sm["sm"][s_k]["tld"]) < 13 and not resp_url.find(j_sm["sm"][s_k]["tld"]) == -1:
                for kw in j_sm["banned_key_words"][s_k]:
                    if kw in resp_url:
                        is_untrue_url = True
                if not is_untrue_url:
                    social_media[s_k]["status"] = True
                    social_media[s_k]["url"] = resp_url
    return social_media



def get_sm_infos(sm_status, ak_config_path):
    with open(ak_config_path, "r") as ak_file:
        j_ak = json.load(ak_file)

    youtube_sm = None
    twitch_sm = None
    instagram_sm = None

    if sm_status["youtube"]["status"]:
        part = "statistics,topicDetails,snippet"
        yt_ak = j_ak["google"]["youtube"]
        try:
            chn_id = str(sm_status["youtube"]["url"]).split("channel/",1)[1]
            get_type = "id"
        except:
            chn_id = str(sm_status["youtube"]["url"]).split("user/",1)[1]
            get_type = "forUsername"
        url = f"https://www.googleapis.com/youtube/v3/channels?part={part}&{get_type}={chn_id}&key={yt_ak}"
        res = requests.get(url)
        j_res = res.json()
        if not j_res["items"][0]["statistics"]["hiddenSubscriberCount"]:
            subs = j_res["items"][0]["statistics"]["subscriberCount"]
        else:
            subs = None
        video_count = int(j_res["items"][0]["statistics"]["videoCount"])
        view_count = int(j_res["items"][0]["statistics"]["viewCount"])
        snippet_country = str(j_res["items"][0]["snippet"]["country"]).lower()
        youtube_sm = {
            "id": chn_id,
            "subscriber_count": int(subs),
            "view_count": view_count,
            "video_count": video_count,
            "snippet_country": snippet_country
        }

    if sm_status["twitch"]["status"]:
        streamer_name = str(sm_status["twitch"]["url"]).split("twitch.tv/",1)[1]
        url = f"https://api.twitch.tv/helix/search/channels?query={streamer_name}"
        headers = {
            "client-id": j_ak["twitch"]["client-id"],
            "Authorization": "Bearer "+j_ak["twitch"]["oauth-token"]
        }
        res = requests.get(url, headers=headers)
        for u in res.json()["data"]:
            if u["broadcaster_login"] == streamer_name:
                tw_user_id = str(u["id"])
                url = f"https://api.twitch.tv/helix/users/follows?to_id={tw_user_id}&first=1"
                res = requests.get(url, headers=headers)
                twitch_sm = {
                    "id": tw_user_id,
                    "broadcaster_name": str(u["broadcaster_login"]),
                    "broadcaster_language": str(u["broadcaster_language"]),
                    "broadcaster_followers": int(res.json()["total"])
                }

    if sm_status["instagram"]["status"]:
        ig_name = str(sm_status["instagram"]["url"]).split("instagram.com/",1)[1]
        ig_name = str(ig_name).split("/",1)[0]

        instagram_sm = {
            "name": ig_name
        }

    return youtube_sm, twitch_sm, instagram_sm