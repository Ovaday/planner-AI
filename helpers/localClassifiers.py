import pickle
from io import BytesIO

import numpy as np
import pandas as pd
from helpers.resourcesPacker import read_encrypted
from open_ai.helpers import fill_classification_template


def load_classifier():
    loaded_model_raw, f = read_encrypted('finalized_model_classification_95528.sav', is_normal_read=False)
    loaded_vectorizer_raw, f = read_encrypted('vectorizer_BOTH_v2.sav', is_normal_read=False)

    loaded_model = pickle.load(BytesIO(loaded_model_raw))
    loaded_vectorizer = pickle.load(BytesIO(loaded_vectorizer_raw))

    return loaded_model, loaded_vectorizer


async def predict_class(message):
    model, vectorizer = load_classifier()
    mine_df = pd.DataFrame({'message': [str(message)]})
    mine_test = vectorizer.transform(mine_df['message'])
    classification_results = np.array(model.predict(mine_test))
    return fill_classification_template(classification_results[0])