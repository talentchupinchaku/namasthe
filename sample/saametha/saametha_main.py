import random
from datetime import datetime
from datetime import timedelta

import praw
import time
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from random import randrange


class Saametha:
    # initialize with appropriate values
    username = "nee_charithra_bot"
    user_agent = "http-client"
    responses = [
        "అందరికీ నేను లోకువ నాకు నంబి రామయ్య లోకువ \n\n Iam below all,but Nambi Ramayya is below me.",
        "పాండవులు గెలుచుకున్న రాజ్యం కౌరవుల తద్దినానికి ఖర్చు అయిపోయింది \n\n [translation](https://www.youtube.com/watch?v=Ubzh2lD52GM&t=392s)",
        "దరిద్రుడు ముడ్డి కడుగుదామని వెళ్తే సముద్రం ఎండిపోయిందట",
        "మొహమాటానికి పోయి కడుపు తెచ్చుకుందట",
        "సిగ్గు లేని వాడికి నవ్వే సింగారం \n\n Laughter is the ornament for the shameless",
        "శుభం పలకరా పెళ్ళికొడక అంటే పెళ్లికూతురు ముండ ఎక్కడ చచ్చింది అన్నాడంట \n\n The proverb is used to describe a person with a negative attitude and when doing something is very pessimistic about it.",
        "నిద్ర పోయే వాడిని లేపోవచ్చు కాని నిద్ర పోయినట్టు నటించే వాడిని నిద్ర లేపెలేము \n\n You can convince someone who is sincere, but impossible to convince someone who is pretending to be sincere.",
        "పొమ్మను వారు కాదు పొగ బెట్టు వారు \n\n If you cannot ask someone to leave, make the situation untenable for them to stay",
        "ఎంకి పెళ్లి సుబ్బి చావుకొచ్చింది \n\n A person is suffering to the maximum because of somebody else's cause(celebrations).",
        "తినడానికి ఏమి లేదు కానీ పెసరపప్పు కి ఎసరు పెట్టమన్నాడట మొగుడు \n\n Wife says its getting impossible (financially) and husband asks for green gram (a kind of lentils, considered premium). Indicates someone being out of touch with reality.",
        "ఎరిగేటప్పుడు తినద్దురా అంటే అద్దుకు తింటా అన్నాడట \n\n This is used in the context when the experience of others is not made to use and people do exactly opposite to what is suggested.",
        "తేలుకు పెత్తనం ఇస్తే తెల్లవార్లు కుట్టిందట",
        "పేనుకు పెత్తనం ఇస్తే తల అంత కొరికి పెట్టిందట",
        "బెల్లం ఉందా అంటే అల్లం ఉంది అన్నాడు అట",
        "సుఖం ఎక్కువ ఐతే.. మొహం కడుగుడు తీరదు",
        "కొత్త బిచ్చగాడు పొద్దు ఎరుగడు",
        "మూడు నెలలు సాము నేర్చి..మూలనున్న ముసలి దాన్ని కొట్టినట్లు",
        "తినే ముందు రుచి అడుగకు, వినే ముందు కథ అడుగకు",
        "చెరువు మీద అలిగి ముడ్డి కడుక్కోవటం మానేసాడట",
        "విత్తనం ఒకటి అయితే మొక్క ఇంకొకటి వస్తుందా",
        "అన్నీ సాగితే రోగమంత భోగం లేదు",
        "ఆర్భాటం కొరకు ఎవరు మీసాలకు పువ్వులు పెట్టుకోరు",
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
        "సూది కోసం సోదికెళ్తే పాత రంకంతా బైట పడిందట",
        "ఏ మొగుడూ దొరక్కుంటే అక్క మొగుడే దిక్కన్నట్లు",
        "తలపాగా చుట్టడం రాక తల వంకర అన్నాడట",
        "తాను వలచింది రంభ తాను మునిగింది గంగ",
        "నిజం గడప దాటే లోపు అబద్ధం ఊరంతా తిరిగి వస్తుంది",
        "గాడిద మొహాన బూడిద పామినట్టు",
        "పిల్లి గుడ్డిదైతే ఎలుక వెక్కిరించిందట",
        "అన్నీ తెలిసినమ్మా అమావాస్య నాడు చస్తే ఏమి తెలియనమ్మ ఏకాదశి నాడు చచ్చిందట",
        "ఏబ్రాసి కి పనెక్కువ లోభికి ఖర్చెక్కువ",
        "నడిమంత్రపు సిరికి నెత్తి మీద కళ్ళు",
        "అంబరాన బిడ్డ పుడితే ఆముదం పెట్టి ముడ్డి కడిగిందట",
        "కొండకు వెంట్రుక ముడి వేస్తే వస్తే కొండ పోతే వెంట్రుకే",
        "ప్రేమగా ఏం వండిపెట్టను అంటే వెన్న తో అట్టేయమనే రకం",
        "పపతివ్రత పరవాన్నం వండితే తెల్లారేదాకా చల్లారలేదట",
        "అమ్మకు అన్నం పెట్టాడు కానీ పిన్నమ్మకు బంగారు గాజులు చేయిస్తా అన్నాడట",
        "మన బంగారం మంచిదైతే కంసాలిని వన్నె అడగటం దేనికి",
        "ఒడ్డునుండి ఎన్నైనా చెప్తారు",
        "నూరు నోములు ఒక్క రంకుతో సరి",
        "ఇంట్లో ఇనప సీల బైట బంగారపు సీల",
        "జుట్టున్నమ్మ ఏ కొప్పు అయినా పెడుతుంది",
        "ఇడిసేసింది ఈదికి పెద్ద ఉంచుకున్నది ఊరికి పెద్ద",
        "కొండముచ్చు పెళ్ళికి కోతి పేరంటాళ్ళు",
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
        "అద్దం అబద్ధం చెప్పదు",
        "ఈతకు మించిన లోతు లేదు",
        "ఆహారానికి ముందుండాలి, వ్యవహారానికి వెనకుండాలి",
        "పాపం అని పాత చీర ఇస్తే, గోడచాటుకి వెళ్లి మూరలేసుకుందట",
        "ఒప్పుకున్న పెళ్ళికి వాయించక తప్పదు",
        "గాడిద సంగీతానికి ఒంటె ఆశ్చర్యపోతే, ఒంటె అందానికి గాడిద మూర్ఛపోయిందట",
        "తగువెలా వస్తుంది జంగందేవరా అంటే బిచ్చం పెట్టవే బొచ్చుముండ అన్నాడుట!",
        "అయ్యకు కోపం సంవత్సరానికి రెండు సార్లే వస్తుంది, వచ్చింది ఆరేసి నెలలు ఉంటుంది",
        "అల్లం అంటే నాకు తెలీదా బెల్లంలా పుల్లగా ఉంటదన్నాడట",
        "అందరూ శ్రీ వైష్ణవులే - ఋట్టెడు రొయ్యలు మాయమయ్యాయి",
        "మన దీపమని ముద్దులాడితే మూతి కాలకుండా వుంటుందా?",
        "ఒడ్డు చేరేదాకా ఓడ మల్లయ్య - ఒడ్డు చేరాక బోడి మల్లయ్య",
        "అయినవాళ్ళకు ఆకులలోను, కాని వాళ్ళకు కంచాలలోను.",
        "ఊహలు ఊళ్ళేలుతుంటే, ఖర్మం కట్టెలు మోస్తుంది, ఋద్ది భూములు ఏలదామంటే రాత గాడిదలు కాస్తానంటుంది.",
        "చెడి స్నేహితుడింటికి పోవచ్చు గానీ, చుట్టాలింటికి పోరాదు",
        "తద్దినానికి భోజనానికి పిలిస్తే, రోజూ మీ ఇంట్లో ఇలానే జరగాలన్నాడట",
        "ఛీ కుక్కా అంటే ఏమక్కా..! అన్నదట",
        "తోటివాడు తొడ కోసుకుంటే మనం మెడ కోసుకుంటామా?",
        "వేలు ఇస్తే చెయ్యి గుంజిందట"
    ]
    used_set = set()
    target_word_list = ["saametha", "sametha", "sameta", "saameta", "సామెత",
                        "సామిత", "saamitha", "saamita", "samita", "samitha"]
    curr_responses_used = len(responses) - 1
    credential = None
    # credential = DefaultAzureCredential()
    client = None
    saametha_secret = None
    saametha_client = None
    password = None

    def init(self):
        if Saametha.credential is None:
            Saametha.credential = ManagedIdentityCredential(client_id="b0b16c58-d25f-4878-8f38-eb21f62a6321")
            # Saametha.credential = DefaultAzureCredential()

        if Saametha.client is None:
            Saametha.client = SecretClient(vault_url="https://bondha-keyvault.vault.azure.net/",
                                           credential=Saametha.credential)
        if Saametha.saametha_client is None:
            Saametha.saametha_client = Saametha.client.get_secret("saametha-client").value
        if Saametha.password is None:
            Saametha.password = Saametha.client.get_secret("namasthe").value

        if Saametha.saametha_secret is None:
            Saametha.saametha_secret = Saametha.client.get_secret("saametha-secret").value

        # creating an authorized reddit instance
        reddit = praw.Reddit(client_id=Saametha.saametha_client,
                             client_secret=Saametha.saametha_secret,
                             username=Saametha.username,
                             password=Saametha.password,
                             user_agent=Saametha.user_agent)

        target_time = datetime.utcnow() - timedelta(minutes=55)
        my_comment_set = set()
        for comment in reddit.redditor("nee_charithra_bot").comments.new(limit=200):
            my_comment_set.add(comment.id)

        bondha_comments = list(reddit.subreddit('ni_bondha').comments(limit=500))
        for bondha_comment in bondha_comments:
            bondha_comment.refresh()
            bondha_comment_set = set(map(lambda comment_reply: comment_reply.id, bondha_comment.replies.list()))
            if datetime.utcfromtimestamp(bondha_comment.created_utc) > target_time:
                for target_word in Saametha.target_word_list:
                    if target_word in bondha_comment.body.lower() and bondha_comment.author.name != "nee_charithra_bot":
                        if (len(my_comment_set & bondha_comment_set)) == 0:
                            random_index = randrange(Saametha.curr_responses_used + 1)
                            Saametha.responses[random_index], Saametha.responses[Saametha.curr_responses_used] = \
                                Saametha.responses[Saametha.curr_responses_used], Saametha.responses[random_index]
                            Saametha.curr_responses_used -= 1
                            if Saametha.curr_responses_used < 40:
                                Saametha.curr_responses_used = len(Saametha.responses) - 1
                            bondha_comment.reply(body="You said variations of proverb somewhere in your comment and I'm supposed to respond with a one, but I disabled this work temporarily. I will make some changes and reenable this in few weeks")
                            # bondha_comment.reply(body=Saametha.prepare_response(self, Saametha.responses[random_index]))
                            break
            else:
                break

    def prepare_response(self, response):
        return response + "\n\n" + "^(made by) [^(u/insginificant)](https://www.reddit.com/user/insginificant) ^(|) " \
                                   "[^(About me)](https://www.reddit.com/r/nee_charithra_bot/comments/xp8nw4/introduction/)"
