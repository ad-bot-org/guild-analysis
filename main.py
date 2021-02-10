import time as t
import json
from lang_detect import LangDetect
from social_media import get_sm, get_sm_infos
import pandas as pd

with open("data/guild_data.json", "r") as j_file:
    g_data = json.load(j_file)

lang_detect = LangDetect()
msg_lang = lang_detect.getMsg(g_data["guild_members"]["members"])
chn_lang = lang_detect.getChannels(g_data["guild_channels"]["text_channels"])
name_lang = lang_detect.getGuildName(g_data["guild_name"])
perc = [60,20,20]
langs_arr = [msg_lang, chn_lang, name_lang]
most_freq_lang = lang_detect.calcTotal(perc, langs_arr)
print(most_freq_lang)

df = pd.read_csv("data/yt-channels.csv")
err = 0
for i in df["Name"]:
    print(i)
    try:
        sm_i = get_sm(i)
        yt_resp, tw_resp, ig_resp = get_sm_infos(sm_i)
        socials = {
            "youtube": yt_resp,
            "twitch": tw_resp,
            "instagram": ig_resp,
        }
        print(socials)
        t.sleep(1)
    except:
        print("Expect Occured!")
        err = err+1
        t.sleep(5)

print("Totals Errors: "+str(err)+"/"+str(len(df["Name"])))