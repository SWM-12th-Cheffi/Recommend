import json
import ast
import numpy as np
from calculate_similarity_vectors import calculate_similarity_vectors
from read_from_cf_json import read_from_cf

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
                            "top1":1 if historyList[i]['place']==0 else 0,
                            "top6":1 if historyList[i]['place']<=5 else 0,
                            "top12":1 if historyList[i]['place']<=11 else 0
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
                            "top1":1 if historyList[i]['place']==0 else 0,
                            "top6":1 if historyList[i]['place']<=5 else 0,
                            "top12":1 if historyList[i]['place']<=11 else 0
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
    #
    likeList_id = []
    for i in likeList:
        likeList_id.append(i['id'])
    person_id = None
    if len(likeList_id) >= 10:
        json_ = read_from_cf()
        max_ = json_['max_']
        for k,v in json_.items():
            if v == list(map(lambda x: str(x),likeList_id)):
                person_id = k
    #


    for recipebefore in historyList:
        if "id" not in recipebefore:
            continue
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
    has_to_remove = []
    if length_ > 5:
        for i in range(0,length_-1):
            for j in range(i+1,length_):
                if "id" not in historyList[j]:
                    has_to_remove.append(historyList[j])
                else:
                    ca = np.array(returnVectorJson(historyList[i]['id'])[str(historyList[i]['id'])])
                    cb = np.array(returnVectorJson(historyList[j]['id'])[str(historyList[j]['id'])])
                    if calculate_similarity_vectors(ca,cb) > 0.95:
                        has_to_remove.append(historyList[j])
        #print(has_to_remove)
        if len(has_to_remove) > 0:
            for element in has_to_remove:
                if element in historyList:
                    historyList.remove(element)
    length_ = len(historyList)            
    if length_ > 100:
        for reduce_iter in range(length_ - 100):
            if historyList[reduce_iter] not in scrapList:
                historyList.remove(historyList[reduce_iter])


    #
    json_ =  read_from_cf()
    likeList_id = []
    print(person_id)
    for i in likeList:
        likeList_id.append(i['id'])
    if person_id != None and len(likeList) >= 10:
        json_[person_id] = list(map(lambda x: str(x),likeList_id))
    elif person_id != None and len(likeList) < 10:
        del json_[person_id]
    elif person_id == None and len(likeList) >= 10:
        json_['max_'] += 1
        json_[json_['max_']] = list(map(lambda x: str(x),likeList_id))
        print(json_)
    with open(f'CF/cf.json', 'w', encoding='utf-8') as make_file:
        json.dump(json_, make_file, indent="\t",ensure_ascii = False)
    #

    outputJson = {
        "id":InputPythonJson['id'],
        "like":{
            "history":historyList,
            "like":likeList,
            "scrap":scrapList
        }
    }
    return outputJson

