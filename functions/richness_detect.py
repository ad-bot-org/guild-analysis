def getRichnessPerMember(members):
    '''
    get the richness of the server
    '''
    mems_has_premium = 0
    for i in members:
        if not i["premium_since"] == None:
            mems_has_premium=mems_has_premium+1
    return mems_has_premium

