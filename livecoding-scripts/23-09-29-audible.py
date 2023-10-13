import pandas as pd


def lst_to_time(lst):
    if len(lst) == 0:
        return 0.0

    hrs = float(lst[0])
    if len(lst) == 1:
        return hrs

    return hrs + (float(lst[1]) / 60)


def stars_to_num_ratings(lst):
    if len(lst) == 3:
        return 0
    substr = lst[4][5:]
    substr = substr.replace(',', '')
    return int(substr)

def clean_audible_csv():
    # Load data
    audible = pd.read_csv('../livecoding-data/audible_uncleaned.csv')


    # Author/narrator columns
    audible['author'] = audible.author.str.split(':').apply(lambda x: x[-1])
    audible['narrator'] = audible.narrator.str.split(':').apply(lambda x: x[-1])
    audible['read_by_author'] = audible.author == audible.narrator


    # Simple rewriting of columns
    audible.releasedate = pd.to_datetime(audible.releasedate, format='%d-%m-%y')
    audible.price = audible.price.str.replace(',', '').str.replace('Free', '0').astype(float).astype(int)
    audible['runtime'] = (audible.time.str
                        .split()
                        .apply(lambda lst: [item for item in lst if item.isnumeric()])
                        .apply(lst_to_time))


    # Derived columns
    audible['score'] = (
        audible.stars.str
        .split()
        .apply(lambda lst: 0.0 if len(lst) == 3 else float(lst[0]))
    )
    audible['num_ratings'] = (
        audible.stars.str
        .split()
        .apply(stars_to_num_ratings)
    )
    audible['month'] = audible.releasedate.dt.month
    audible['day'] = audible.releasedate.dt.day


    # Dropping columns no longer used
    audible = audible.drop(columns=['time'])
    audible = audible.drop(columns=['stars'])

    return audible


if __name__ == '__main__':
    print('Starting the transformation...')
    cleaned_audible = clean_audible_csv()
    cleaned_audible.to_csv('clean_audible.csv', index=False)
    print('All done!')
