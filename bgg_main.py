import top_games
import game_ids
import bgg_stats
import bgg_stat_words
import bgg_model

# Get top games
games = top_games.top_games()

# Get game ids
game_ids = game_ids.get_game_ids(games)

# Get game stats
stats = bgg_stats.bgg_stats(game_ids)

# Get word stats
word_stats = bgg_stat_words.word_stats(stats)

# Preprocess data for model
X_train, X_test, y_train, y_test = bgg_model.preprocess_data(word_stats)

# Create and train model
bgg_model.create_model(X_train, X_test, y_train, y_test)