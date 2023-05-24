from burrito.utils.db_preprocessor import LocalDataBasePreprocessor

LocalDataBasePreprocessor(
    {"filename": "./preprocessor_config.json"}
).apply_data()
