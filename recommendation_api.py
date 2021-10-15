import json
import ast
import numpy as np
from scipy import spatial
from calculate_similarity_vectors import calculate_similarity_vectors

def generateUserPreferenceVector(InputPythonJson):
    likeList = InputPythonJson['like']['like']
    likeList = [x["id"] for x in likeList]
    likeList = list(filter(lambda x : x!= None,likeList))
    likeList = list(map(lambda x : str(x),likeList))
    #######
    base_vectors = []
    size = len(likeList)
    for i in range(size):
        with open(f'./recipe_vector/{likeList[i]}.json',"r") as f:
            vector_json = json.load(f)
            vector_json = json.dumps(vector_json,ensure_ascii = False)
            vector_json = ast.literal_eval(vector_json)
            vector = np.array(vector_json[str(likeList[i])])
            vector_ = {}
            vector_['vector'] = vector
            vector_['rating'] = InputPythonJson['like']['like'][i]['rating']
            base_vectors.append(vector_)
    return base_vectors


def return_max_similarity(base_vectors,recipe_vector):
    max_ = 0
    for i in base_vectors:
        alpha = 0
        if i['rating'] >= 4:
            alpha += 0.15
        if i['rating'] == 5:
            alpha += 0.1
        max_ = max(max_,calculate_similarity_vectors(i['vector'], recipe_vector) + alpha)
    return max_


def get_recommend_by_userVector(InputPythonJson,top=60):
    base_vectors = generateUserPreferenceVector(InputPythonJson)
    possible_recipe_id_list = InputPythonJson['id']
    ########
    sort_list = []
    for recipe_id in possible_recipe_id_list:
        with open(f"./recipe_vector/{recipe_id}.json","r") as f:
            vector_json = json.load(f)
            vector_json = json.dumps(vector_json,ensure_ascii = False)
            vector_json = ast.literal_eval(vector_json)
            vector = np.array(vector_json[str(recipe_id)])
        sort_element = {}
        sort_element['id']=recipe_id
        sort_element['similarity']=return_max_similarity(base_vectors,vector)
        sort_list.append(sort_element)
    sort_list = sorted(sort_list,key=lambda x:x['similarity'],reverse=True)
    return sort_list

