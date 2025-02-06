import pickle

# Load the diabetes model
with open('Diabetes_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Print the model's features with improved error handling
try:
    if hasattr(model, 'feature_names_in_'):
        print("Model features:", model.feature_names_in_)
    else:
        raise AttributeError("The model does not have feature names.")
except Exception as e:
    print(f"Error loading features: {e}")
