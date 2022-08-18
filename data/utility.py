import json
import re
import preprocessor as tpre

infile_directory = "24ur comments/"

infile_name = "4346886"

infile_ext = ".json"

outfile_directory = "labelled/"
file_name = "2021_40"
labels = ['desno', 'nevtralno', 'levo']

full_f_name = file_name + infile_ext

# Tweet preprocessor
tpre.set_options(tpre.OPT.URL, tpre.OPT.MENTION, tpre.OPT.HASHTAG)

def take_n_tweets(fromN, toN, vol):
    d = []
    with open(f'2021/{full_f_name}', 'r', encoding='utf8') as sample_data:
        data = json.load(sample_data)

        for i in range(fromN, toN):
            tweet = data[i]

            tweet_full_text = tweet['full_text']
            tweet_id = tweet['id']
            tweet_hashtags = [t['text'] for t in tweet['entities']['hashtags']]
            tweet_mentions = [t['screen_name'] for t in tweet['entities']['user_mentions']]
            tweet_user_name = tweet['user']['name']
            tweet_user_screen_name = tweet['user']['screen_name']
            tweet_user_description = clean_tweet_text(tweet['user']['description']).lower()
            tweet_created_at = tweet['created_at']

            d.append({
                "id": tweet_id,
                "created_at": tweet_created_at,
                "full_text": clean_tweet_text(tweet_full_text),
                "hashtags": tweet_hashtags,
                "mentions": tweet_mentions,
                "user": {
                    "name": tweet_user_name,
                    "screen_name": tweet_user_screen_name,
                    "description": tweet_user_description
                }
            })

        # Save the smaller sample subset
        with open(f'2021/{file_name}/{file_name}_{vol}{infile_ext}', 'w', encoding='utf8') as outdata:
            json.dump(d, outdata, ensure_ascii=False)


def clean_tweet_text(tweet_text):
    tweet_text = tpre.clean(tweet_text)
    tweet_text = re.sub("&gt;|&lt;", "", tweet_text)
    tweet_text = remove_emojis(tweet_text)
    return tweet_text


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def label_comments(input_file, output_file=None):
    data = []
    with open(input_file, 'r', encoding='utf8') as sample_data:
        data = json.load(sample_data)

    labelled_data = []
    unlabelled_data = []

    for i, sample in enumerate(data):
        o = ask_for_label(sample)
        if o is None:
            unlabelled_data = data[i:len(data)]
            break
        elif not o:
            continue
        labelled_data.append(o)

    # Save labelled data
    if len(labelled_data) > 0:
        with open(f'{input_file}_labelled.json' if output_file is None else output_file, 'w',
                  encoding='utf8') as labels_file:
            json.dump(labelled_data, labels_file, ensure_ascii=False)

    # Save the rest of data
    if len(unlabelled_data) > 0:
        with open(f'{input_file}_unlabelled.json' if output_file is None else output_file, 'w',
                  encoding='utf8') as labels_file:
            json.dump(unlabelled_data, labels_file, ensure_ascii=False)


def ask_for_label(sample):
    print(f'Nickname: {sample["nickname"]}\n')
    print(f'Text: \n{sample["text"]}\n')
    print('-------------------------------------------------')
    ans = input('Enter: {d - desno}, {n - nevtralno}, {l - levo}, {s - skip}, {c - cancel}, {else type the label name}: ')

    sample.pop("nickname")

    if ans == 'd':
        sample['label'] = 'desno'
    elif ans == 'n':
        sample['label'] = 'nevtralno'
    elif ans == 'l':
        sample['label'] = 'levo'
    elif ans == 's':
        return []
    elif ans == 'c':
        return None
    else:
        sample['label'] = ans
    print('-------------------------------------------------')
    return sample


# Labelling code

#label_comments(str(infile_directory + infile_name + infile_ext))

# Cut into smaller subsets of twitter data
def cut_tweet_data(filename):
    i = 0
    j = 1
    while i <= 100000:
        take_n_tweets(i, i + 10000, j)
        print(f'Done volume {j}')
        i = i + 10000
        j = j + 1


cut_tweet_data(full_f_name)

