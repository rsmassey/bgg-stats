from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def custom_tokenizer(text):
    return [t.strip() for t in text.split(',') if t.strip()]

def word_stats(bgg_stats):
    
    bgg_stat_words = pd.DataFrame()
    
    # bgg_stat_words['Designers'] = df['Designers']
    
    # The designers added far too many columns when count vectorized
    
    bgg_stat_words['Categories'] = bgg_stats['Categories']
    bgg_stat_words['Mechanics'] = bgg_stats['Mechanics']
    
    count = CountVectorizer(tokenizer=custom_tokenizer, stop_words='english')
    
    # count_designers = count.fit_transform(bgg_stat_words['Designers'])
    # count_designers_df = pd.DataFrame(count_designers.toarray(), columns=count.get_feature_names_out(), index=bgg_stat_words.index)

    count_categories = count.fit_transform(bgg_stat_words['Categories'])
    count_categories_df = pd.DataFrame(count_categories.toarray(), columns=count.get_feature_names_out(), index=bgg_stat_words.index)

    count_mechanics = count.fit_transform(bgg_stat_words['Mechanics'])
    count_mechanics_df = pd.DataFrame(count_mechanics.toarray(), columns=count.get_feature_names_out(), index=bgg_stat_words.index)

    bgg_stats = pd.merge(bgg_stats, bgg_stats_cat_mech, left_index=True, right_index=True)
    
    return bgg_stats