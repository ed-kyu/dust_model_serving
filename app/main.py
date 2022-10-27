from fastapi import FastAPI, HTTPException
import uvicorn
from app.inferences import inference
import yaml
import os
from datetime import datetime, timedelta
from pathlib import Path

app = FastAPI()

@app.get("/")
def hello():
    return {
        "Hello":"World"
    }

@app.get("/predict")
def read_region(city: str = "마포구"):
    region_dict = {
        '송파구': 2, '종로구': 4, '서초구': 0, '은평구': 1, 
    '동작구': 4, '동대문구': 1, '노원구': 3, '관악구': 4, '도봉구': 4, '영등포구': 4, 
    '중랑구': 4, '강북구': 4, '중구': 2, '금천구': 2, '성동구': 3, '성북구': 4, 
    '강동구': 0, '광진구': 2, '강남구': 3, '서대문구': 2, '용산구': 1, '마포구': 2, 
    '양천구': 2, '구로구': 0, '강서구': 3
    }
    region_num_to_str = {
        0: '서북권', 1: '도심권', 2: '서남권', 3: '동남권', 4: '동북권'
    }
    city_dict = {'송파구': 0, '종로구': 1, '서초구': 2, '은평구': 3, 
    '동작구': 4, '동대문구': 5, '노원구': 6, '관악구': 7, '도봉구': 8, '영등포구': 9, 
    '중랑구': 10, '강북구': 11, '중구': 12, '금천구': 13, '성동구': 14, '성북구': 15, 
    '강동구': 16, '광진구': 17, '강남구': 18, '서대문구': 19, '용산구': 20, '마포구': 21, 
    '양천구': 22, '구로구': 23, '강서구': 24}

    file_path = Path(__file__).resolve().parent
    with open(os.path.join(file_path.parent, 'config.yaml'), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    last_day = config['CRAWLING_LAST_DAY']
    last_day = datetime.strptime(last_day, '%Y-%m-%d')

    if city in region_dict:   
        result = inference(city_dict[city])
        result_json = {
            "region": region_num_to_str[region_dict[city]], 
            "city": city,
            "prediction": []
            }
        for val in result:
            last_day += timedelta(days=1)
            result_json['prediction'].append({'day': str(last_day)[:10],'PM10': round(val.item(), 3)})
        return result_json

    else:
        raise HTTPException(status_code=404, detail="Region not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)