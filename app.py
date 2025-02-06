import pickle
from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained model from model.pkl
with open("Diabetes_model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/")
def home():
    # Render the index.html from the templates folder
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Retrieve form data from the request
    try:
        # Mandatory fields
        bmi = float(request.form["bmi"])
        age = float(request.form["age"])
        physHlth = float(request.form["physHlth"])
        mentHlth = float(request.form["mentHlth"])
        genHlth = float(request.form["genHlth"])
        
        # Optional fields; if empty, default to 0 or appropriate value
        # For yes/no fields, we'll convert 'yes' to 1 and 'no' to 0.
        def yes_no(val):
            if val.lower() == "yes":
                return 1
            elif val.lower() == "no":
                return 0
            else:
                return 0

        highBP = yes_no(request.form.get("highBP", ""))
        fruits = float(request.form.get("fruits", 0) or 0)
        smoker = yes_no(request.form.get("smoker", ""))
        veggies = float(request.form.get("veggies", 0) or 0)
        physActivity = float(request.form.get("physActivity", 0) or 0)
        
        # For Sex, assume "male" maps to 1, "female" to 0.
        sex_raw = request.form.get("sex", "").lower()
        sex = 1 if sex_raw == "male" else 0
        
        highChol = yes_no(request.form.get("highChol", ""))
        diffWalk = yes_no(request.form.get("diffWalk", ""))
        heartDisease = yes_no(request.form.get("heartDisease", ""))
        noDocbcCost = yes_no(request.form.get("noDocbcCost", ""))
        stroke = yes_no(request.form.get("stroke", ""))
        anyHealthcare = yes_no(request.form.get("anyHealthcare", ""))
        hvyAlcoholConsump = yes_no(request.form.get("hvyAlcoholConsump", ""))
        cholCheck = yes_no(request.form.get("cholCheck", ""))
        
        # Construct the input vector in the expected order.
        # [BMI, Age, PhysHlth, MentHlth, GenHlth, HighBP, Fruits, Smoker, Veggies,
        #  PhysActivity, Sex, HighChol, DiffWalk, HeartDisease, NoDocbcCost, Stroke,
        #  AnyHealthcare, HvyAlcoholConsump, CholCheck]
        input_features = [
            bmi, age, physHlth, mentHlth, genHlth, highBP, fruits, smoker,
            veggies, physActivity, sex, highChol, diffWalk, heartDisease,
            noDocbcCost, stroke, anyHealthcare, hvyAlcoholConsump, cholCheck
        ]
        
        # Make prediction using the pre-loaded model
        # (Ensure your model was trained with features in this exact order.)
        prediction = model.predict([input_features])[0]
        
        # Interpret the prediction (assuming binary classification: 1 for positive, 0 for negative)
        result_text = "Diabetes Positive" if prediction == 1 else "Diabetes Negative"
    
    except Exception as e:
        result_text = f"Error in input data: {str(e)}"
    
    # Render the same index.html with a prediction result
    return render_template("index.html", prediction_text=result_text)

if __name__ == "__main__":
    # Run the Flask app in debug mode (remove debug=True for production)
    app.run(debug=True)
