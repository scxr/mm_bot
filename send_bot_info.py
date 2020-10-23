import requests
webhook_url = 'https://discordapp.com/api/webhooks/768938734241710111/IhC2KD4nagztUAYUd2PZgIsZmXj55LjI-3jh455LvIB7J8PnZ608nZApmJT0nx9U3lTn'

def phished(webhook):
    poglul = {
        "avatar_url":"https://s3.amazonaws.com/media.eremedia.com/uploads/2016/07/05124748/middlemen.jpg",
        "name":"Middler",
        "embeds": [
            {
                "title": "MM Bot Information :)",
                "description": f"Are you tired of waiting for MM's to come online?\n"\
                    "Are you tired of paying these extorniate fees even on small deals?\n"\
                        "Are you tired of these fake MMs trying to exit scam for a couple hundred?\n"\
                            "Are you tired of waiting for MMs to deliver the fees even once the deal is over?\n"\
                                "Well! Look no further, this bot solves all the problems above! It is a middleman, without the man, a middler online 24/7 and has no bias at all."\
                                    "With a mm fee of 2.5% regardless of how big/small the transaction is, never have to pay high amounts ever again!\n"\
                                        "To use this all you have to do is type `!deal @user amount(usd)` and the rest is very self explanatority :)",
                "color": 15146294,
                "footer":{
                    "text":"made by xo#0111"
                    },
            }
        ]
    }
    req = requests.post(webhook, json=poglul)
    print(req.status_code)
phished(webhook_url)