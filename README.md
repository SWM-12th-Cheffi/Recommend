```bash
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

```
# main.py
- recommendation_api.py, userpreference_update.py를 독립적인 url주소로 실행
- ex) http://localhost:5000/recommend

# recommendation_api.py
- input:
```json
{
    id: int,
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
```
- output:[int]

- 사용자가 만들 수 있는 레시피번호(input.id)와 취향을 나타내는 정보(input.like.like)를 바탕으로 사용자의 취향을 벡터로 정의하고 
타 비슷한 취향의 유저와 비교하여 타 유저의 취향까지 고려. cosine similarity로 레시피들을 유사도 기준으로 sort

# CF
- 내부 cf.json에 사용자데이터 저장
- memory base user based collaborative filtering recommendation system 적용목적

# recipe_vector
- 레시피들의 고차원 벡터 파일형태 저장

# TopNaccuracy
- 추천시스템 성능지표인 top-n-accuracy측정을 위한 파일 저장


# userpreference_update.py
- input: 
```json
{
    id: int,
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
```
```json
- output: {
    id: int,
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
```
- input.like.history를 활용하여 input.like.like 갱신
- input.like.history를 활용하여 TopNaccuracy/TopNaccuracy.json 갱신
- input.like.like를 활용하여 CF/cf.json을 갱신


# read_from_cf_json.py
- CF폴더로부터 파일을 읽기 위한 모듈

# calculate_similarity_vectors.py
- cosine 유사도 계산을 위한 모듈