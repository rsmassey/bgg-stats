from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform

mlflow.set_tracking_uri('file://mlruns')

def preprocess_data(bgg_stats):
    X = bgg_stats.drop(['Name', 'Rating'], axis=1)
    y = bgg_stats['Rating']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X[['Min_players', 'Max_players', 'Min_playtime', 'Max_playtime', 'Weight']])
    X_scaled_df = pd.DataFrame(X_scaled, columns=['scaled_Min_players', 'scaled_Max_players', 'scaled_Min_playtime', 'scaled_Max_playtime', 'scaled_Weight'])

    X_final = pd.concat([X_scaled_df, X.drop(['Min_players', 'Max_players', 'Min_playtime', 'Max_playtime', 'Weight'], axis=1)], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def create_model(X_train, X_test, y_train, y_test):
    # Create a GradientBoostingRegressor object
    gbr = GradientBoostingRegressor()

    # Define the hyperparameter grid to search over
    param_dist = {
        'n_estimators': sp_randint(100, 1000),
        'max_depth': sp_randint(3, 10),
        'learning_rate': sp_uniform(0.01, 0.5),
        'subsample': sp_uniform(0.5, 0.5),
        'loss': ['ls', 'lad', 'huber', 'quantile']
    }

    # Start MLflow run
    with mlflow.start_run():
        # Create a RandomizedSearchCV object to search over the hyperparameter grid
        random_search = RandomizedSearchCV(gbr, param_distributions=param_dist, n_iter=10)

        # Fit the RandomizedSearchCV object to the data
        random_search.fit(X_train, y_train)

        # Print the best hyperparameters found by RandomizedSearchCV
        print("Best hyperparameters:", random_search.best_params_)

        # Use the best hyperparameters to create a final GradientBoostingRegressor object
        final_gbr = GradientBoostingRegressor(**random_search.best_params_)

        # Train the final GradientBoostingRegressor object on the full dataset
        final_gbr.fit(X_train, y_train)
        
        # Log the model to MLflow
        mlflow.sklearn.log_model(final_gbr, "model")

        y_pred = final_gbr.predict(X_test)
        mse_final_gbr = mean_squared_error(y_test, y_pred)

        print(mse_final_gbr)
        
        # Log the MSE to MLflow
        mlflow.log_metric("mse", mse_final_gbr)