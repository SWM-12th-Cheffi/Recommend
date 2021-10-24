import json
import ast
import numpy as np
from calculate_similarity_vectors import calculate_similarity_vectors


def trackTopNaccuracy(InputPythonJson):
    print("here")
    likeList = InputPythonJson['like']['like']
    historyList = InputPythonJson['like']['history']
    if len(historyList) > 0:
        with open(f"./TopNaccuracy/TopNaccuracy.json","r") as f:
            top_json = json.load(f)
            top_json = json.dumps(top_json,ensure_ascii = False)
            top_json = ast.literal_eval(top_json)
            if top_json == {}:
                length_ = len(historyList)
                iter_ = 1
                for i in range(length_):
                    print(historyList[i]['rating'])
                    if historyList[i]['rating'] == int(historyList[i]['rating']):
                
                        top_json[str(iter_)] = {
                            "top1":1 if historyList[i]['place']==1 else 0,
                            "top10":1 if historyList[i]['place']<=10 else 0,
                            "top25":1 if historyList[i]['place']<=25 else 0
                        }
                        iter_+=1
            else:
                max_ = 0
                for k in top_json.keys():
                    max_ = max(int(k),max_)
                length_ = len(historyList)
                for i in range(length_):
                    if historyList[i]['rating'] == int(historyList[i]['rating']):
                        top_json[str(max_+1)] = {
                            "top1":1 if historyList[i]['place']==1 else 0,
                            "top10":1 if historyList[i]['place']<=10 else 0,
                            "top25":1 if historyList[i]['place']<=25 else 0
                        }
                        max_ += 1
            with open(f"./TopNaccuracy/TopNaccuracy.json", 'w', encoding='utf-8') as make_file:
                    json.dump(top_json, make_file, indent="\t",ensure_ascii = False)
               


def returnVectorJson(filename):
    with open(f"./recipe_vector/{filename}.json","r") as f:
        vector_json = json.load(f)
        vector_json = json.dumps(vector_json,ensure_ascii = False)
        vector_json = ast.literal_eval(vector_json)
    return vector_json

def UpdateUserPreferrence(InputPythonJson):
    
    likeList = InputPythonJson['like']['like']
    historyList = InputPythonJson['like']['history']
    scrapList = InputPythonJson['like']['scrap']
    for recipebefore in historyList:
        if recipebefore['rating'] == int(recipebefore['rating']):
            recipebefore['rating'] += 0.1
        if recipebefore['rating'] != None and int(recipebefore['rating']) < 3:
            hate_id = recipebefore['id']
            vector_json = returnVectorJson(hate_id)
            hatevector = np.array(vector_json[str(hate_id)])
            for likerecipe in likeList:
                like_id = likerecipe['id']
                vector_json = returnVectorJson(like_id)
                likevector = np.array(vector_json[str(like_id)])
                if calculate_similarity_vectors(likevector,hatevector) > 0.85:
                    if calculate_similarity_vectors(likevector,hatevector) > 0.95 and int(likerecipe['rating'])-int(recipebefore['rating']) >= 2:
                        likerecipe['rating'] = abs(int(likerecipe['rating'])+int(recipebefore['rating']))//2
                    else:
                        likeList.remove(likerecipe)
        if recipebefore['rating'] == None or int(recipebefore['rating']) >= 4:
            recipe_like_id = recipebefore['id']
            replace = False
            for likerecipe in likeList: # already updated history recipe into likeList
                if likerecipe['id'] == recipe_like_id:
                    replace = True
                    likerecipe['rating'] = int(recipebefore['rating'])
            if replace == False: # most recent history recipe -> should be updated into likeList
                done = False
                for likerecipe in likeList:
                    like_id = likerecipe['id']
                    vector_json_already_in_list = returnVectorJson(like_id)
                    vector_json_compare = returnVectorJson(recipe_like_id)
                    vector_already_in_list = np.array(vector_json_already_in_list[str(like_id)])
                    vector_compare = np.array(vector_json_compare[str(recipe_like_id)])
                    if calculate_similarity_vectors(vector_already_in_list,vector_compare) > 0.90 and done == False:
                        done = True
                        likeList.remove(likerecipe)
                        likeList.append(recipebefore)
                if done == False:
                    likeList.append(recipebefore)
    
    length_ = len(historyList)
    if length_ > 5:
        for i in range(0,length_-1):
            for j in range(i+1,length_-1):
                ca = np.array(returnVectorJson(historyList[i]['id'])[str(historyList[i]['id'])])
                cb = np.array(returnVectorJson(historyList[j]['id'])[str(historyList[j]['id'])])
                if calculate_similarity_vectors(ca,cb) > 0.93:
                    historyList.remove(historyList[j])
    length_ = len(historyList)            
    if length_ > 100:
        for reduce_iter in range(length_ - 100):
            if historyList[reduce_iter] not in scrapList:
                historyList.remove(historyList[reduce_iter])


    outputJson = {
        "id":InputPythonJson['id'],
        "like":{
            "history":historyList,
            "like":likeList,
            "scrap":scrapList
        }
    }
    return outputJson

