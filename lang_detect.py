class LangDetect():
    def getMsg(self, members):
        '''
        get the language of the messages
        '''
        from langdetect import detect as detect
        bot_cmd_prefix = ["+", "!", "/"]
        last_msgs_lang = []
        for i in members:
            if i[15] == None or i[8] == True:
                continue
            is_bot_cmd = False
            for k in bot_cmd_prefix:
                if i[15].startswith(k):
                    is_bot_cmd = True
            if not is_bot_cmd:
                last_msgs_lang.append(detect(i[15]))
        freq_msg_lang = max(set(last_msgs_lang), key=last_msgs_lang.count)
        return freq_msg_lang
    
    def getChannels(self, channels):
        '''
        get the language of the channels
        '''
        from langdetect import detect as detect
        txt_channels_langs = []
        for i in channels:
            if i[1] == None:
                continue
            txt_channels_langs.append(detect(i[1]))
        freq_channels_lang = max(set(txt_channels_langs), key=txt_channels_langs.count)
        return freq_channels_lang

    def getGuildName(self, guild_name):
        from langdetect import detect as detect
        return detect(guild_name)

    def calcTotal(self, percentages, langs):
        t_lang = []
        for i in range(len(percentages)):
            for o in range(percentages[i]):
                t_lang.append(langs[i])
        freq_t_lang = max(set(t_lang), key=t_lang.count)
        return freq_t_lang


# '''
# get the richness of the server
# '''
# mems_has_premium = 0
# for i in g_data["guild_members"]["members"]:
#     if i[8] == True:
#         continue
#     if not i[10] == None:
#         mems_has_premium=+1
# print(str(mems_has_premium)+"/"+str(g_data["guild_member_count"]))