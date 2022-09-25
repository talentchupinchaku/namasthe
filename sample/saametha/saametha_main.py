import random
from datetime import datetime
from datetime import timedelta

import praw
import time
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# initialize with appropriate values
username = "nee_charithra_bot"
user_agent = "http-client"
responses = [
    "అందరికీ నేను లోకువ నాకు నంబి రామయ్య లోకువ \n\n Iam below all,but Nambi Ramayya is below me.",
    "పాండవులు గెలుచుకున్న రాజ్యం కౌరవుల తద్దినానికి ఖర్చు అయిపోయింది \n\n [translation](https://www.youtube.com/watch?v=Ubzh2lD52GM&t=392s)",
    "దరిద్రుడు ముడ్డి కడుగుదామని వెళ్తే సముద్రం ఎండిపోయిందట \n\n Translation: ??",
    "మొహమాటానికి పోయి కడుపు తెచ్చుకుందట \n\n Translation: ??",
    "సిగ్గు లేని వాడికి నవ్వే సింగారం \n\n Laughter is the ornament for the shameless",
    "శుభం పలకరా పెళ్ళికొడక అంటే పెళ్లికూతురు ముండ ఎక్కడ చచ్చింది అన్నాడంట \n\n The proverb is used to describe a person with a negative attitude and when doing something is very pessimistic about it.",
    "నిద్ర పోయే వాడిని లేపోవచ్చు కాని నిద్ర పోయినట్టు నటించే వాడిని నిద్ర లేపెలేము \n\n You can convince someone who is sincere, but impossible to convince someone who is pretending to be sincere.",
    "పొమ్మను వారు కాదు పొగ బెట్టు వారు \n\n If you cannot ask someone to leave, make the situation untenable for them to stay",
    "ఎంకి పెళ్లి సుబ్బి చావుకొచ్చింది \n\n A person is suffering to the maximum because of somebody else's cause(celebrations).",
    "తినడానికి ఏమి లేదు కానీ పెసరపప్పు కి ఎసరు పెట్టమన్నాడట మొగుడు \n\n Wife says its getting impossible (financially) and husband asks for green gram (a kind of lentils, considered premium). Indicates someone being out of touch with reality.",
    "ఎరిగేటప్పుడు తినద్దురా అంటే అద్దుకు తింటా అన్నాడట \n\n This is used in the context when the experience of others is not made to use and people do exactly opposite to what is suggested.",
    "తేలుకు పెత్తనం ఇస్తే తెల్లవార్లు కుట్టిందట \n\n Translation: ??",
    "పేనుకు పెత్తనం ఇస్తే తల అంత కొరికి పెట్టిందట \n\n Translation: ??",
    "బెల్లం ఉందా అంటే అల్లం ఉంది అన్నాడు అట \n\n Translation: ??",
    "సుఖం ఎక్కువ ఐతే ... మొహం కడుగుడు తీరదు...",
    "కొత్త బిచ్చగాడు పొద్దు ఎరుగడు",
    "మూడు నెలలు సాము నేర్చి...మూలనున్న ముసలి దాన్ని కొట్టినట్లు",
    "తినే ముందు రుచి అడుగకు, వినే ముందు కథ అడుగకు...",
    "చెరువు మీద అలిగి ముడ్డి కడుక్కోవటం మానేసాడట",
    "విత్తనం ఒకటి అయితే మొక్క ఇంకొకటి వస్తుందా",
    "అన్నీ సాగితే రోగమంత భోగం లేదు...",
    "ఆర్భాటం కొరకు ఎవరు మీసాలకు పువ్వులు పెట్టుకోరు..",
    "తొందర ఆలస్యానికి మొగుడు",
    "అమ్మా పెట్టదు, అడుక్కు తినా తిననీయదు",
    "అయినోణ్ణి అడిగేదానికంటే కానీ వాణ్ణి కాళ్ళు పట్టుకోవటం మేలు",
    "అన్నవారు బాగున్నారు పడినవారు బాగున్నారు, నడుమ ఉన్న వారే నలిగి చచ్చారు",
    "అన్నం తిన్నవారు, తన్నులు తిన్నవారు మరిచిపోరు",
    "అయ్యవారు రానంతమాత్రాన అమావాస్య ఆగుతుందా?",
    "ఊరికొక కోడి ఇస్తే ఇంటికొక ఈక వచ్చిందట",
    "తాడిచెట్టు కింద కూర్చుని పాలు తాగినా అది కల్లే అనుకుంటారు",
    "అయ్యకు ఆరాటమే కానీ పోరాటం తక్కువ",
    "ఊరికే ఉన్నవాడికి ఉపాయాలు ఎక్కువ",
    "నాట్యం చేయవే రంగసాని అంటే నేల వంకరగా ఉంది అందట",
    "కొండనాలుక కి మందు వేస్తే ఉన్న నాలుక ఊడిందట",
    "అమాయకుడుకి అక్షింతలు ఇస్తే పక్కకి వెళ్లి నోట్లో వేసుకున్నాడట",
    "చింత లేనమ్మ సంత లో నిద్రపోయిందట",
    "దయగల మొగుడు దర్వాజా దగ్గరేసి కొట్టాడట పెళ్ళాన్ని",
    "సిద్దడు అద్దంకి వెళ్లనూ వెళ్ళాడు, రానూ వచ్చాడు \n\n Translation: oka raatri Siddadu ni valla nanna, tellavaaragaane, "
    "addanki pampinchi, oka pani cheyinchukuni raavaali ani siddadi thalli tho chepthunnadu. "
    "Adhi siddadu vinesi thandri padukogaane addanki velli thellavaaresariki vachesadu. Idhe saametha పుల్లయ్య వ్యామవరం "
    "ani kuda antaaru",
    "ఇల్లు కాలి ఇల్లాలు ఏడుస్తుంటే బొగ్గుల వ్యాపారి బేరానికి వచ్చాడట",
    "జీతం, భత్యం లేకుండా తోడేలు  గొర్రెలని కాస్తానందట",
    "తిక్కలవాడు తిరనాళ్ళ కి వెళ్తే ఎక్కా, దిగా సరిపోయిందట",
    "అఆ లు రావు కానీ అగ్రతాంబూలం నాదే అన్నాడట",
    "గాజుల బేరం భోజనానికి సరి",
    "అద్దం అబద్దం చెప్పదు",
    "ఈతకు మించిన లోతు లేదు",
    "ఆహారానికి ముందుండాలి వ్యవహారానికి వెనకుండాలి",
    "పాపం అని పాత చీర ఇస్తే, గోడచాటుకి వెళ్లి మూరలేసుకుందట"
]

target_word_list = ["saametha", "sametha", "sameta", "saameta", "సామెత", "సామిత", "saamitha", "saamita", "samita", "samitha"]

def init():
    credential = ManagedIdentityCredential(client_id="49f9fa53-a238-4ac8-b4f2-ab82433075c0")
    # credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://bondha-vault.vault.azure.net/", credential=credential)

    password = client.get_secret("namasthe").value
    bot_id = client.get_secret("saametha-client").value
    bot_secret = client.get_secret("saametha-secret").value

    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    target_time = datetime.utcnow() - timedelta(minutes=55)
    my_comment_set = set()
    for comment in reddit.redditor("nee_charithra_bot").comments.new(limit=200):
        my_comment_set.add(comment.id)

    bondha_comments = list(reddit.subreddit('ni_bondha').comments(limit=500))

    for bondha_comment in bondha_comments:
        bondha_comment.refresh()
        bondha_comment_set = set(map(lambda comment_reply: comment_reply.id, bondha_comment.replies.list()))
        if datetime.utcfromtimestamp(bondha_comment.created_utc) > target_time:
            for target_word in target_word_list:
                if target_word in bondha_comment.body.lower() and bondha_comment.author.name != "nee_charithra_bot":
                    if (len(my_comment_set & bondha_comment_set)) == 0:
                        bondha_comment.reply(body=prepare_response(random.choice(responses)))
                        break
        else:
            break

def prepare_response(response):
    return response + "\n\n" + "(_this a bot account, upvote if you like the saametha, redirect abuse to u/insginificant_)"