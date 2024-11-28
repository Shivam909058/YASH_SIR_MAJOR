from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

class LogisticRegressionClassifier:
    def __init__(self, model=None):
        self.classifier = model if model is not None else LogisticRegression(C=0.1, penalty="l2", random_state=42)
    
    def train(self, X_train_vec, Y_train):
        self.classifier.fit(X_train_vec, Y_train)
        return self.classifier
        
    def predict(self, X_test_vec):
        try:
            return self.classifier.predict(X_test_vec)
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            # Return safe default in case of error
            return np.zeros(X_test_vec.shape[0], dtype=int)
        
    def score(self, Y_pred, Y):
        return accuracy_score(Y_pred, Y) * 100