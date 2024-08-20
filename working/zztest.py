import joblib
# import features_extraction
import sys
from extractnew import main as extract_features
import numpy as np


def main():
    url = sys.argv[1]

        # Extract features
    features = extract_features(url)
    # features = [0, 0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0, 0,  0, 0, 0]
    features_array = np.array([features])  # Convert to 2D array for prediction
    print(features_array)

    # Load the trained model
    clf = joblib.load('xgb_model.joblib')
    # clf2 = joblib.load('best_random_forest_model.joblib')

    # Predict
    pred = clf.predict(features_array)
    # pred2 = clf2.predict(features_array)

    print(pred)


    # Print the probability of prediction (if needed)
    # prob = clf.predict_proba(features_array)
    # print("probability")
    # print(prob)
    # print 'Features=', features_test, 'The predicted probability is - ', prob, 'The predicted label is - ', pred
    #    print "The probability of this site being a phishing website is ", features_test[0]*100, "%"

    if int(pred[0]) == 1:
        # print "The website is safe to browse"
        print("SAFE")
    elif int(pred[0]) == 0:
        # print "The website has phishing features. DO NOT VISIT!"
        print("PHISHING")

        # print 'Error -', features_test


if __name__ == "__main__":
    main()