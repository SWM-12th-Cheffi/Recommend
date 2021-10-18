from flask import jsonify, Flask, request
from recommendation_api import calculate_similarity_vectors, generateUserPreferenceVector, return_max_similarity, get_recommend_by_userVector
from userpreference_update import returnVectorJson, UpdateUserPreferrence, trackTopNaccuracy

app = Flask(__name__)



@app.route("/recommend",methods=["POST","GET"]) # 재료 다 고르자마자 실행
def send_recommended_json():
    InputPythonJson = request.get_json()
    return_recipe_id = get_recommend_by_userVector(InputPythonJson)
    res = []
    for recipe_ in return_recipe_id:
        del recipe_['similarity']
    for element_dict in return_recipe_id:
        res.append(element_dict['id'])
    return str(res),200
################ input example


@app.route("/userpreference_update",methods=["POST","GET"]) # 유저가 추천된 레시피 고르고 레이팅을 하던 안하던 레시피에서 나가고 나서 실행 고려중  
def send_userpreference_json():
    InputPythonJson = request.get_json()
    outputJson = UpdateUserPreferrence(InputPythonJson)
    trackTopNaccuracy(InputPythonJson)
    return jsonify({"output_json":outputJson}),200



app.run(host="0.0.0.0",port=5000,debug=True)


###### execute below statement
