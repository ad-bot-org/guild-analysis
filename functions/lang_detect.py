class LangDetect():
    def getMsg(self, members):
        '''
        get the language of the messages
        '''
        from langdetect import detect as detect
        bot_cmd_prefix = ["+", "!", "/", "$"]
        last_msgs_lang = []
        for i in members:
            if i["last_message"] == None or i["bot"] == True:
                continue
            is_bot_cmd = False
            for k in bot_cmd_prefix:
                if i["last_message"].startswith(k):
                    is_bot_cmd = True
            if not is_bot_cmd:
                last_msgs_lang.append(detect(i["last_message"]))
        freq_msg_lang = max(set(last_msgs_lang), key=last_msgs_lang.count)
        return freq_msg_lang
    
    def getChannels(self, channels):
        '''
        get the language of the channels
        '''
        from langdetect import detect as detect
        txt_channels_langs = []
        for i in channels:
            if i["name"] == None:
                continue
            txt_channels_langs.append(detect(i["name"]))
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