from bot.database import *

def funtion(name) :
    if(name == 'autoposting') :
        query = "SELECT * FROM function_bot WHERE name = 'autoposting'"
        result = db_connection(query)
        return result
    elif(name == 'autoRetweetNonEleved') :
        query = "SELECT * FROM function_bot WHERE name = 'autoRetweetNonEleved'"
        result = db_connection(query)
        return result
    elif(name == 'autoRepostNonEleved') :
        query = "SELECT * FROM function_bot WHERE name = 'autoRepostNonEleved'"
        result = db_connection(query)
        return result
    elif(name == 'autopostingAkunBackUp') :
        query = "SELECT * FROM function_bot WHERE name = 'autopostingAkunBackUp'"
        result = db_connection(query)
        return result
    elif(name == 'autoRepostAkunAyah') :
        query = "SELECT * FROM function_bot WHERE name = 'autoRepostAkunAyah'"
        result = db_connection(query)
        return result
    elif(name == 'autopostingTrendingTopik') :
        query = "SELECT * FROM function_bot WHERE name = 'autopostingTrendingTopik'"
        result = db_connection(query)
        return result
    elif(name == 'postingVideo') :
        query = "SELECT * FROM function_bot WHERE name = 'postingVideo'"
        result = db_connection(query)
        return result
    elif(name == 'posting') :
        query = "SELECT * FROM function_bot WHERE name = 'posting'"
        result = db_connection(query)
        return result
    elif(name == 'autoPostingTelegram') :
        query = "SELECT * FROM function_bot WHERE name = 'autoPostingTelegram'"
        result = db_connection(query)
        return result
    elif(name == 'autoPostingPinterest') :
        query = "SELECT * FROM function_bot WHERE name = 'autoPostingPinterest'"
        result = db_connection(query)
        return result
    elif(name == 'autoPostingFacebook') :
        query = "SELECT * FROM function_bot WHERE name = 'autoPostingFacebook'"
        result = db_connection(query)
        return result
        