import requests
import json
import glob
import functools

def getbookmarks():
    url = 'https://twitter.com/i/api/graphql/DtY7ITw1NhpU1CcuOhx41Q/Bookmarks?variables=%7B%22count%22%3A150%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Atrue%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D'

    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-twitter-client-language' : 'fr',
        'x-csrf-token' : 'd40e0b5ca37b50aab3782cf1232ab092d438477564317742634648c906a923b3d6f54d766a91920590957850fea7b0e551e34b14912c4496c7a1f4b3e9b3a85b01d2b5687bb3f42bebfb5c06806d2163',
        'x-twitter-auth-type' : 'OAuth2Session',
        'x-twitter-active-user' : 'yes',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'content-type' : 'application/json',
        'Accept' : '*/*',
        'Sec-GPC' : '1',
        'host' : 'twitter.com'
    }

    cookies = {
        'auth_token' : 'd274517bc947547526afea1f04653959a2a2560f',
        'ct0' : 'd40e0b5ca37b50aab3782cf1232ab092d438477564317742634648c906a923b3d6f54d766a91920590957850fea7b0e551e34b14912c4496c7a1f4b3e9b3a85b01d2b5687bb3f42bebfb5c06806d2163',
        'd_prefs' : 'MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'des_opt_in' : 'N',
        'dnt' : '1',
        'g_state' : '{"i_p":1649276405153,"i_l":1}',
        'guest_id' : 'v1%3A164978824735677186',
        'kdt' : 'w82HiQnanDlhOZInBP8MA72RHO41GvGl7Xhjjk4d'
    }

    r = requests.get(url, headers=headers, cookies=cookies)
    print(" - Tentative d'acc??s ?? l'url...")
    if r.status_code == 200:
        print(" - Tentative r??ussie.")
        print(" - Sauvegarde des signets...")
        data = r.json()
        txt = json.dumps(data)
        f = open('JSONBookmarks/signets.json', 'w')
        f.write(txt)
        f.close()
        print(" - Signets sauvegard??s avec succ??s ! ")
    else:
        print("Erreur dans l'acc??s ?? l'url")
        exit(1)

getbookmarks()

signets = []
md_file = open("bookmarks.txt", "w+", encoding="utf-8")

files = [file for file in glob.glob("JSONBookmarks/*")]
for file_name in files:
    with open(file_name, encoding="utf-8") as bk:
        data = json.load(bk)
        signets.append(data)

def constructUrl(tweet_id, username):
    return "https://twitter.com/" + str(username) + "/status/" + str(tweet_id)
    #Cr??ation du lien du signet

def deep_get(dictionary, keys, default=None):
    return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

for data in signets:
    instructions_list = deep_get(data, "data.bookmark_timeline.timeline.instructions")
    tweet_entries_list = deep_get(instructions_list[0], "entries")
    for tweet_entry in tweet_entries_list:
        result = deep_get(tweet_entry, "content.itemContent.tweet_results.result")
        username = deep_get(result, "core.user_results.result.legacy.screen_name")
        text = deep_get(result, "legacy.full_text")
        tweet_id = deep_get(result, "rest_id")
        url = constructUrl(tweet_id, str(username))
        extrait = 'TWEET : ' + str(text).replace('\n', '') + ';;;' + 'AUTEUR : ' + str(username).replace('\n','') + ';;;' + 'URL : ' + url.replace('\n', '') + ';;;\n'
        md_file.write(str(extrait))
    print(" --- G??n??ration du fichier CSV termin??e ! --- ")