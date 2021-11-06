
recommendation_with_update_using_flask
│   README.md
│   recommendation_api.py
│   userpreference_update.py
│   read_from_cf_json.py
│   calculate_similarity.py
│   main.py
│ 
└───amountOfIngre
│   │   5388__.json
│   │   5389__.json
│   │   5390__.json
│   │   ...
│   
└───CF
│   │   cf.json
│   
└───recipe_vector
│   │   5388.json
│   │   5389.json
│   │   5390.json
│   │   ...
│
└───TopNaccuracy
    │   TopNaccuracy.json


# main.py
- recommendation_api.py, userpreference_update.py를 독립적인 url주소로 실행
- ex) http://localhost:5000/recommend

# recommendation_api.py
- input:{
    id: int
    like:{
        history:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        like:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        scrap:[
            {
                id:int,
                place:int,
                rating:int
            }
        ]
    }
}

- output:[int]
- 사용자가 만들 수 있는 레시피번호(input.id)와 취향을 나타내는 정보(input.like.like)를 바탕으로 사용자의 취향을 벡터로 정의하고 cosine similarity로 레시피들을 유사도 기준으로 sort

# userpreference_update.py
- input: {
    id: int
    like:{
        history:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        like:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        scrap:[
            {
                id:int,
                place:int,
                rating:int
            }
        ]
    }
}

- output: {
    id: int
    like:{
        history:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        like:[
            {
                id:int,
                place:int,
                rating:int
            }
        ],
        scrap:[
            {
                id:int,
                place:int,
                rating:int
            }
        ]
    }
}