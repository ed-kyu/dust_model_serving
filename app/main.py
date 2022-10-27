from fastapi import FastAPI, HTTPException
import uvicorn
from inferences import inference
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

@app.get("/predict/")
async def read_region(region: str = "마포구"):
    region_dict = {'송파구': 0, '종로구': 1, '서초구': 2, '은평구': 3, 
    '동작구': 4, '동대문구': 5, '노원구': 6, '관악구': 7, '도봉구': 8, '영등포구': 9, 
    '중랑구': 10, '강북구': 11, '중구': 12, '금천구': 13, '성동구': 14, '성북구': 15, 
    '강동구': 16, '광진구': 17, '강남구': 18, '서대문구': 19, '용산구': 20, '마포구': 21, 
    '양천구': 22, '구로구': 23, '강서구': 24}

    file_path = Path(__file__).resolve().parent
    with open(os.path.join(file_path.parent, 'config.yaml'), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    last_day = config['CRAWLING_LAST_DAY']
    last_day = datetime.strptime(last_day, '%Y-%m-%d')

    if region in region_dict:   
        result = inference(region_dict[region])
        result_json = {   
            "region": region,
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