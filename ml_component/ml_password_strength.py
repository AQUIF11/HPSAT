"""
Created on Sun Nov  22 15:33:41 2020

@author: Aquif R Mir
"""
"""
--MACHINE LEARNING COMPONENT
ml_password_strength module can be used to get Machine Learning Based classification
score of a given password-string.
"""

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def getTokens(inputString):
    tokens = []
    for i in inputString:
        tokens.append(i)
    return tokens


# path for password file
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, "data.csv")

data = pd.read_csv(filepath, sep=',', on_bad_lines='skip')
data.isnull().any()

data = pd.DataFrame(data)

X = data.iloc[:, 0].values
y = data.iloc[:, 1].values

# vectorizing the password strings
vectorizer = TfidfVectorizer(tokenizer=getTokens, token_pattern=None)
X = vectorizer.fit_transform(X)

# logistic regression classifier
lgs = LogisticRegression(penalty='l2', max_iter=1000)

# training
lgs.fit(X, y)


class MLPasswordStrength:
    def __init__(self, password):
        self.password = []
        self.password.append(password)
        self.score = self.__classification_score()[0] + 1

    def __classification_score(self):
        vect_password = vectorizer.transform(self.password)
        return lgs.predict(vect_password)

    def get_ml_score(self):
        return self.score


# For unit testing the MLPasswordStrength module.
def main():
    input_string = input("Enter password: ")
    ml_ps = MLPasswordStrength(input_string)
    print("Machine Learning Component Score (Min=1, Max=3): {:d}".format(ml_ps.get_ml_score()))


if __name__ == "__main__":
    main()
