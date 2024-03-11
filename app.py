
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
import logging
from config import DevelopmentConfig 


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# set database connection 
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

class ChartData(db.Model):
    __tablename__ = 'Chart_Data'
    Id = db.Column(db.Integer, primary_key=True)
    HADM_ID = db.Column(db.Integer)
    CHARTTIME = db.Column(db.TIMESTAMP)
    VALUENUM = db.Column(db.Float)  # Assuming REAL maps to Float
    ERROR = db.Column(db.Integer)
    WARNING = db.Column(db.Integer)
    STOPPED = db.Column(db.Integer)
    Observation_Type_Id = db.Column(db.Integer, db.ForeignKey('Observation_Type.Id'))
    Result_Status_Id = db.Column(db.Integer, db.ForeignKey('Result_Status.Id'))
    Unit_Of_Measure_Id = db.Column(db.Integer, db.ForeignKey('Unit_Of_Measure.Id'))

    observation_type = db.relationship("ObservationType", backref="chart_data")
    result_status = db.relationship("ResultStatus", backref="chart_data" )
    unit_of_measure = db.relationship("UnitOfMeasure", backref="chart_data")

    

class ObservationType(db.Model):
    __tablename__ = 'Observation_Type'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class ResultStatus(db.Model):
    __tablename__ = 'Result_Status'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class UnitOfMeasure(db.Model):
    __tablename__ = 'Unit_Of_Measure'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)



# create end point 
#@app.route('/chart_data', methods=['GET'])    
#@app.route('/chart_data', methods=['POST'])
@app.route('/chart_data', methods=['GET', 'POST'])
def getchartdata():
    Ids_list = []
   
   # ---Both GET and POST  ---#
    if request.method == 'GET':
        Ids = request.args.get('Ids') 
        if not Ids:
            return jsonify({'error':'no Ids provided'}),400
        Ids_list = [int(i) for i in Ids.split(',')]
    
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"error" :"request must be json"}), 400
        data = request.get_json()
        Ids = data.get('Ids',[])
        Ids_list = [int(i) for i in Ids]
    

   # Query the ChartData table for records with IDs that match the provided list, include all related ObservationType
    data = ChartData.query.filter(ChartData.Id.in_(Ids_list)).all()

    end_pt1_result = []
    for item in data:
        #print(item.Observation_Type)
        #observation_type_name = item.Observation_Type.Name if item.Observation_Type else None
        #print(observation_type_name)  # Check if you get the expected names or None

        end_pt1_result.append({
            'Id': item.Id,
            'ChartTime': item.CHARTTIME.isoformat() if item.CHARTTIME else None,  # Ensure datetime is JSON serializable
            'VALUENUM':item.VALUENUM,
            'ERROR':item.ERROR,
            'WARNING':item.WARNING,
            'STOPPED':item.STOPPED,
            'Observation_Type_Name': item.observation_type.Name if item.observation_type else 'None',  # add if item.observation_type
            'Result_Status_Name': item.result_status.Name if item.result_status else 'None',   # if to prevent error: ChartData record has a NULL value for Result_Status_Id
            'Unit_Of_Measure_Name': item.unit_of_measure.Name if item.unit_of_measure else 'None'



        })
    
    return jsonify(end_pt1_result)



@app.route('/data_summary_sql', methods=['GET'])
def data_summary():
    db_path = app.config['DATABASE_PATH']  
    sql = '''
    WITH _valid_tb AS 
    (SELECT
    cd.VALUENUM,
    cd.HADM_ID,
    COALESCE(ot.Name, 'None') AS observation_type, -- deal with null value, make it the same as api ep 1
    COALESCE(um.Name, 'None') AS measure_unit,
    COALESCE(rs.Name, 'None') AS result_status

    FROM 
    Chart_Data cd

    LEFT JOIN Observation_Type ot ON cd.Observation_Type_Id = ot.Id 
    LEFT JOIN Unit_Of_Measure um ON cd.Unit_Of_Measure_Id = um.Id
    LEFT JOIN Result_Status rs ON cd.Result_Status_Id = rs.Id

    WHERE 
    (cd.ERROR != 1 OR cd.ERROR IS NULL) AND 
    (cd.WARNING != 1 OR cd.WARNING IS NULL) AND 
    (rs.Name IS NOT 'Manual' OR rs.Name IS NULL)
    )

    SELECT
    observation_type,
    measure_unit,
    COUNT(DISTINCT HADM_ID) AS num_adm,
    MIN(VALUENUM) AS min_val,
    MAX(VALUENUM) AS max_val
    FROM _valid_tb vt 
    GROUP BY observation_type, measure_unit;
    '''

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    ## Execute sql
    cur.execute(sql)
    ## fetch and print 
    results = cur.fetchall()
    conn.close()

    # convert result to list of dictionary of jsonify
    data_summary = []
    for row in results:
        data_summary.append({
            "observation_type":row[0],
            "measure_unit":row[1],
            "num_adm":row[2],
            "min_val":row[3],
            "max_val":row[4]
        })
    return jsonify(data_summary)



#db_path_url = "sqlite:////home/zzz/develop/Weil/randomized_chart_data.sqlite"
#engine = create_engine(db_path_url)

@app.route('/data_summary_pandas', methods=['GET'])

def data_summary_pandas():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    sql = '''
    SELECT
    cd.VALUENUM,
    cd.HADM_ID,
    cd.ERROR,
    cd.WARNING,
    COALESCE(ot.Name, 'None') AS observation_type, -- deal with null value, make it the same as api ep 1
    COALESCE(um.Name, 'None') AS measure_unit,
    COALESCE(rs.Name, 'None') AS result_status

    FROM 
    Chart_Data cd

    LEFT JOIN Observation_Type ot ON cd.Observation_Type_Id = ot.Id 
    LEFT JOIN Unit_Of_Measure um ON cd.Unit_Of_Measure_Id = um.Id
    LEFT JOIN Result_Status rs ON cd.Result_Status_Id = rs.Id
    '''

    all_data_df = pd.read_sql_query(sql, engine)

    filtered_df = all_data_df[
        (all_data_df['ERROR'] != 1) &
        (all_data_df['WARNING'] != 1)&
        (all_data_df['result_status'] != 'Manual')
    ]

    summary_df = filtered_df.groupby(['observation_type','measure_unit']).agg(
        num_adm = ('HADM_ID','nunique'),
        min_val = ('VALUENUM','min'),
        max_val = ('VALUENUM','max')
    ).reset_index()

    summary_json = summary_df.to_dict(orient='records') # use to_dict instead of to_json will show in pretty 

    return jsonify(summary_json)


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=1319, debug=True)
