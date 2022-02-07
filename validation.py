import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import pymongo
from pprint import pprint
from logging import info, error
from sklearn.preprocessing import MinMaxScaler


# Normalizes all the columns of a Pandas DataFrame using sklearn's Min-Max Feature Scaling.
def normalize_dataframe(dataframe):
    pprint(dataframe)
    scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(dataframe)
    return pd.DataFrame(scaled, columns=dataframe.columns)


def validate_model(models_dir, job_id, model_type, documents, feature_fields, label_field, validation_metric, normalize=True):
    # Load MongoDB Documents into Pandas DataFrame
    features_df = pd.DataFrame(list(documents))

    # Normalize features, if requested
    if normalize:
        features_df = normalize_dataframe(features_df)

    # Pop the label column off into its own DataFrame
    label_df = features_df.pop(label_field)

    # Load model from disk
    model_path = f"{models_dir}/{job_id}"
    model = tf.keras.models.load_model(model_path)
    model.summary()
    validation_results = model.evaluate(features_df, label_df, batch_size=128, return_dict=True)
    print(f"\n\nValidation Results: {validation_results}")

