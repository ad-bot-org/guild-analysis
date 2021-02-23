import json
from functions.lang_detect import LangDetect
from functions.social_media import get_sm, get_sm_infos
from functions.richness_detect import getRichnessPerMember

def analysisGuild(g_data):
    df = {
        "guild_name": g_data["guild_name"],
        "guild_lang": None,
        "guild_name_words": g_data["guild_name"].split(" "),
        "guild_social_media": None,
        "guild_richness": None,
        "guild_member_count": None,
        "guild_categories": None
    }

    lang_detect = LangDetect()
    msg_lang = lang_detect.getMsg(g_data["guild_members"]["online_members"])
    chn_lang = lang_detect.getChannels(g_data["guild_channels"]["text_channels"])
    name_lang = lang_detect.getGuildName(g_data["guild_name"])
    perc = [60,20,20]
    langs_arr = [msg_lang, chn_lang, name_lang]
    most_freq_lang = lang_detect.calcTotal(perc, langs_arr)

    df["guild_lang"] = most_freq_lang

    try:
        try:
            sm_i = get_sm(g_data["guild_name"], "configs/social-media.json")
        except:
            print("Error: Cannot get Google Search urls.")
        if not sm_i == None:
            try:
                yt_resp, tw_resp, ig_resp = get_sm_infos(sm_i, "configs/api-keys.json")
                socials = {
                    "youtube": yt_resp,
                    "twitch": tw_resp,
                    "instagram": ig_resp,
                }
                df["guild_social_media"] = socials
            except:
                print("Error: Cannot process social medias.")
    except:
        print("Expect Occured!")
        df["guild_social_media"] = {
            "youtube": None,
            "twitch": None,
            "instagram": None,
        }

    percent_rich = float((int(getRichnessPerMember(g_data["guild_members"]["online_members"]))*100)/int(len(g_data["guild_members"]["online_members"])))
    df["guild_richness"] = int(percent_rich)

    df["guild_member_count"] = int(g_data["guild_member_count"])
    return df