from flask import Flask, jsonify, render_template, request, redirect,  flash, abort, url_for
from project import app
from project import app,db
from project.models import *
import requests
import pickle
import os   
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# import joblib

@app.route('/')
def index1():
    return render_template('index.html')

@app.route('/index',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submit = 'X'
        api_key = '30d4741c779ba94c470ca1f63045390a'

        # user_input = input("Enter city: ")
        user_input = request.form['location']

        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

        if weather_data.json()['cod'] == '404':
            #print("No City Found")
            # return redirect('/index')
            return render_template("index.html", submit= submit)
        else:
            temp = weather_data.json()['main']['temp']
            wind_speed = weather_data.json()['wind']['speed']
            wind_deg = weather_data.json()['wind']['deg']
            cloud_cover = weather_data.json()['clouds']['all']
            humidity = weather_data.json()['main']['humidity']
            location = weather_data.json()['name']

            # if 0 <= wind_deg < 90:
            #     wind_direction = "North-East"
            #     wind_dir = 4
            # elif 90 <= wind_deg < 180:
            #     wind_direction = "South-East"
            #     wind_dir = 5
            # elif 180 <= wind_deg < 270:
            #     wind_direction = "South-West"
            #     wind_dir = 6
            # else:
            #     wind_direction = "North-West"
            #     wind_dir = 7

            if 337.5 <= wind_deg <= 360 or 0 <= wind_deg < 22.5:
                wind_direction = "North"
                wind_dir = 0
            elif 22.5 <= wind_deg < 67.5:
                wind_direction = "North-East"
                wind_dir = 4
            elif 67.5 <= wind_deg < 112.5:
                wind_direction = "East"
                wind_dir = 1
            elif 112.5 <= wind_deg < 157.5:
                wind_direction = "South-East"
                wind_dir = 5
            elif 157.5 <= wind_deg < 202.5:
                wind_direction = "South"
                wind_dir = 2
            elif 202.5 <= wind_deg < 247.5:
                wind_direction = "South-West"
                wind_dir = 6
            elif 247.5 <= wind_deg < 292.5:
                wind_direction = "West"
                wind_dir = 3
            else:
                wind_direction = "North-West"
                wind_dir = 4

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')

            # load
            with open(MODEL_PATH ,'rb') as f:
                model = pickle.load(f)


            #predict
            # orientation = model.predict([[temp, wind_speed, wind_dir]])
            orientation = model.predict([[temp, wind_dir]])
            match orientation[0]:
                case 0:
                    orientation_out = 'North-South'
                case 1:
                    orientation_out = 'East-West'
                case 2:
                    orientation_out = 'South-North'
                case 3:
                    orientation_out = 'West-East'
            # print(f"The weather in {user_input} is: {weather}")
            # print(f"The temperature in {user_input} is: {temp}ºF")
            # print(f"The Wind speed in {user_input} is: {wind_speed}Km/h")
            # print(weather_data.json())

            #Material selection
            # Material properties
            wall_mat_path = os.path.join(BASE_DIR, 'static','data', 'wall_mat.csv')
            wall_mat_data = pd.read_csv(wall_mat_path)
            door_mat_path = os.path.join(BASE_DIR, 'static','data', 'door_mat.csv')
            door_mat_data = pd.read_csv(door_mat_path)
            window_mat_path = os.path.join(BASE_DIR, 'static','data', 'window_mat.csv')
            window_mat_data = pd.read_csv(window_mat_path)
            # materials = [
            #     {"Material": "Hempcrete", "U_min": 0.09, "U_max": 0.12, "R_min": 8.3, "R_max": 11.1, "TM_min": 500, "TM_max": 800, "A_min": 0.6, "A_max": 0.75},
            #     {"Material": "CLT (Cross-Laminated Timber)", "U_min": 0.13, "U_max": 0.17, "R_min": 5.9, "R_max": 7.7, "TM_min": 800, "TM_max": 1200, "A_min": 0.5, "A_max": 0.7},
            #     {"Material": "Engineered Timber", "U_min": 0.14, "U_max": 0.22, "R_min": 4.5, "R_max": 7.1, "TM_min": 900, "TM_max": 1300, "A_min": 0.5, "A_max": 0.7},
            #     {"Material": "Wood Wool Panels", "U_min": 0.07, "U_max": 0.12, "R_min": 8.3, "R_max": 14.3, "TM_min": 600, "TM_max": 1000, "A_min": 0.5, "A_max": 0.7},
            #     {"Material": "Gypsum", "U_min": 0.16, "U_max": 0.2, "R_min": 5.0, "R_max": 6.3, "TM_min": 700, "TM_max": 1000, "A_min": 0.5, "A_max": 0.7}
            # ]
            wall_materials = material_select(temp,cloud_cover,humidity,wall_mat_data)
            door_materials = material_select(temp,cloud_cover,humidity,door_mat_data)
            window_materials = material_select(temp,cloud_cover,humidity,window_mat_data)
            if len(orientation_out) == 0 or len(wall_materials) == 0 or len(door_materials) == 0 or len(window_materials) == 0:
                submit ='X'
            return render_template("index.html",location=location,out1=orientation_out, out2=wind_direction, wall_materials = wall_materials, door_materials=door_materials, window_materials=window_materials, submit= submit)
    else :
        return render_template("index.html")
    

@app.route('/foundation', methods=['GET', 'POST'])
def foundation():
    obj=soil_data.query.filter_by().all()
    if request.method == 'POST':
        location = request.form['location']
        num_stories = int(request.form['story'])
        building_type = request.form['type']
        floor_area = int(request.form['area'])

        if location == 'Other':
            bearing_capacity = request.form['bearing']
        else:    
            # Retrieve soil properties
            soil = soil_data.query.filter_by(location=location)
            bearing_capacity= soil[0].bearing_capacity
        

        # Calculate loads
        dead_load, live_load, total_load = calculate_loads(floor_area, num_stories, building_type)

        foundation = found_data.query.filter_by(usage=building_type)
        # Find suitable foundations
        primary_foundation = None
        detailed_reason = None
        other_options = []

        for foundation in foundation:
            if (foundation.bearing_capacity_l <= bearing_capacity <= foundation.bearing_capacity_h ):
                if not primary_foundation:
                    primary_foundation = foundation.foundation
                    detailed_reason = foundation.reason

                else:
                    other_options.append(foundation.foundation)

        return render_template('foundation.html', location=location, obj = obj, dead_load = dead_load, live_load = live_load, 
                               total_load = total_load, primary_foundation = primary_foundation, detailed_reason = detailed_reason,
                               other_options=other_options)
    else:
        return render_template('foundation.html', obj = obj)

def calculate_loads(floor_area, num_stories, building_type):
    if building_type == "Residential":
        dead_load_per_unit = 5  # kN/m²
        live_load_per_unit = 2  # kN/m²
    elif building_type == "Multi-story":
        dead_load_per_unit = 6  # kN/m²
        live_load_per_unit = 3  # kN/m²
    else:
        raise ValueError("Invalid building type")
    
    dead_load = floor_area * num_stories * dead_load_per_unit
    live_load = floor_area * num_stories * live_load_per_unit
    total_load = dead_load + live_load
    
    return dead_load, live_load, total_load

@app.route('/createfoundation', methods=['GET', 'POST'])
def createfoundation():
    if request.method == 'POST':
        foundation = request.form['foundation']
        usage = request.form['usage']
        bearing_capacity_l = request.form['bearing_capacity_l']
        bearing_capacity_h = request.form['bearing_capacity_h']
        reason = request.form['reason']

        my_data1 = found_data(foundation = foundation,usage = usage,bearing_capacity_l = bearing_capacity_l,bearing_capacity_h = bearing_capacity_h, reason = reason)
        db.session.add(my_data1)
        db.session.commit()

        # delete = soil_data.query.filter_by(location = location).all()
        # db.session.query(found_data).delete()
        # db.session.commit()
        
        obj=found_data.query.filter_by().all()
        return render_template('createfoundation.html', out1 = 'Success',out2 = obj)
    else:
        obj=found_data.query.filter_by().all()
        return render_template('createfoundation.html',out2 = obj)

# @app.route('/update_location', methods=['POST'])
# def update_location():
#     data = request.get_json()
#     selected_location = data.get('location')
    
#     # You can process the location here (e.g., fetch details from DB)
    
#     return jsonify({'message': f'Location updated to {selected_location}'})

def material_select(temp,cloud_cover,humidity,materials):
    # Weights for each factor (adjusted based on weather)
    # if temp > 30:  # Hot weather → Increase insulation priority
    #     w1, w2, w3, w4 = 0.5, 0.3, 0.1, 0.1
    # elif temp < 15:  # Cold weather → Consider thermal mass more
    #     w1, w2, w3, w4 = 0.3, 0.4, 0.2, 0.1
    # else:  # Moderate weather
    #     w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1
    if temp > 95:
        w1, w2, w3, w4 = 0.8, 0.05, 0.05, 0.1  # Insulation is extremely important
    elif temp > 80:
        w1, w2, w3, w4 = 0.6, 0.15, 0.15, 0.1
    else:
         w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1  # Heat retention is more important

# Adjust absorptance weight based on sunlight exposure (cloud cover)
    # if cloud_cover > 70:
    #     w4 = 0.05  # Less sunlight, absorptance is less important
    # elif cloud_cover < 30:
    #     w4 = 0.2  # More sunlight, absorptance matters more    
    if cloud_cover > 80:
        w4 -= 0.2  # Increase weight on absorptance (less heat absorption)
    elif cloud_cover < 20:
        w4 += 0.3  # Reduce its effect since sun exposure is high

    if humidity > 70:  # Humid places need water-resistant materials
        w3 += 0.2

    tm_min = min(m["TM_min"] for index,m in materials.iterrows())
    tm_max = max(m["TM_max"] for index,m in materials.iterrows())

     # Normalize function
    def normalize(value, min_val, max_val):
        if max_val == min_val:  
            return 0.5  # Prevent division by zero, assign neutral score
        return (value - min_val) / (max_val - min_val)

    # Compute scores
    for index, material in materials.iterrows():
        # u_min = int(material["U_min"])
        U_avg = (material["U_min"] + material["U_max"]) / 2
        R_avg = (material["R_min"] + material["R_max"]) / 2
        TM_avg = (material["TM_min"]) + int(material["TM_max"]) / 2
        A_avg = (material["A_min"]) + int(material["A_max"]) / 2
                
        # Normalize thermal mass
        TM_norm = normalize(TM_avg, tm_min, tm_max)

        # Calculate score
        score = (w1 * (1 / U_avg)) + (w2 * R_avg) + (w3 * TM_norm) + (w4 * (1 - abs(A_avg - 0.65)))
                
        material["Score"] = round(score, 3)
        materials.at[index, "Score"] = round(score, 3)

    # Sort by best score
    df = pd.DataFrame(materials)
    df = df.sort_values(by="Score", ascending=False)
    best_materials = df["Material"].head(6).tolist()
    return best_materials