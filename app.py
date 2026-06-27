from flask import Flask, render_template, request
import pymysql
from flask_cors import CORS


app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)


CORS(app)



def get_connection():

    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Deepasri",
        database="prediction_db",
        cursorclass=pymysql.cursors.DictCursor
    )





@app.route('/')
def home():

    return render_template(
        'index.html',
        page="home"
    )





@app.route('/crop')
def crop():

    return render_template(
        'index.html',
        page="crop"
    )





@app.route('/price')
def price():

    return render_template(
        'index.html',
        page="price"
    )





@app.route('/pest')
def pest():

    return render_template(
        'index.html',
        page="pest"
    )









@app.route('/predict_crop', methods=['POST'])
def predict_crop():


    soil = request.form.get('soil')
    ph = float(request.form.get('ph'))
    rainfall = float(request.form.get('rainfall'))
    temperature = float(request.form.get('temperature'))
    season = request.form.get('season')



    connection = get_connection()
    cursor = connection.cursor()



    query = """
    SELECT recommended_crop FROM crop_recommendations
    WHERE soil_type=%s AND season=%s
    AND ph BETWEEN %s AND %s
    AND rainfall BETWEEN %s AND %s
    AND temperature BETWEEN %s AND %s
    """



    cursor.execute(
        query,
        (
            soil,
            season,
            ph-0.5,
            ph+0.5,
            rainfall-50,
            rainfall+50,
            temperature-5,
            temperature+5
        )
    )



    result = cursor.fetchone()

    connection.close()



    output = (
        f"Recommended Crop: {result['recommended_crop']}"
        if result
        else
        "No recommendation found"
    )



    return render_template(
        'index.html',
        page="crop",
        result=output
    )









@app.route('/predict_price', methods=['POST'])
def predict_price():


    crop = request.form.get('crop')
    month = request.form.get('month')



    connection = get_connection()
    cursor = connection.cursor()



    query = """
    SELECT price_per_kg, export_place, crop_type
    FROM price_predicts
    WHERE crop_name=%s AND month=%s
    """



    cursor.execute(
        query,
        (crop, month)
    )



    result = cursor.fetchone()

    connection.close()




    output = (

        f"Price per kg: {result['price_per_kg']}\n"
        f"Export Place: {result['export_place']}\n"
        f"Crop Type: {result['crop_type']}"

        if result

        else

        "Data not available"
    )



    return render_template(
        'index.html',
        page="price",
        result=output
    )











@app.route('/predict_pest', methods=['POST'])
def predict_pest():


    crop = request.form.get('crop')
    symptoms = request.form.get('symptoms')



    connection = get_connection()
    cursor = connection.cursor()



    query = """
    SELECT pest, pesticide, application_method
    FROM pest_predicts
    WHERE crop=%s AND symptoms=%s
    """



    cursor.execute(
        query,
        (crop, symptoms)
    )



    result = cursor.fetchone()


    connection.close()





    output = (

        f"Pest: {result['pest']}\n"
        f"Pesticide: {result['pesticide']}\n"
        f"Application Method: {result['application_method']}"

        if result

        else

        "Data not available"

    )





    return render_template(
        'index.html',
        page="pest",
        result=output
    )







if __name__ == "__main__":

    app.run(debug=True)