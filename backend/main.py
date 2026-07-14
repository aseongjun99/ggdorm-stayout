from datetime import date, timedelta

from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fake_useragent import UserAgent
import httpx

app = FastAPI()
ua = UserAgent()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로그인
@app.post("/login-test")
async def login_test(
    loginId: str = Form(...),
    loginPwd: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...)
):
    url = "https://www.ggdorm.or.kr/user/login"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua.chrome
    }
        
    data = {
        "retUrl": "/ko/index/mypage/stayout/",
        "loginId": loginId,
        "loginPwd": loginPwd
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(url, headers=headers, data=data, timeout=5)
        jsession_id = client.cookies.get("JSESSIONID")
        soup = BeautifulSoup(response.text, "html.parser")

        registration_no = soup.find(
            "input",
            {"name": "registrationNo"}
        )["value"]
        
        print(await fetch_user_info(jsession_id, registration_no, start_date, end_date))

        return jsession_id, registration_no
    
# 외박 신청을 위한 사용자 정보 확인
async def fetch_user_info(jsession_id, registration_no, start_date, end_date):
    url = "https://www.ggdorm.or.kr/ko/index/mypage/stayout/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua.chrome
    }

    cookies = {
        "JSESSIONID" : jsession_id
    }

    data = {
        "registrationNo" : registration_no,
        "mode": "write"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=url, 
                headers=headers,
                cookies=cookies,
                data=data
            )
            
            html_text = response.text
            soup = BeautifulSoup(html_text, 'html.parser')

            extracted_data = {
                "registrationNo": (
                    soup.find("input", {"name": "registrationNo"}).get("value", "")
                    if soup.find("input", {"name": "registrationNo"})
                    else ""
                ),
                "studentId": (
                    soup.find("input", {"name": "stno"}).get("value", "")
                    if soup.find("input", {"name": "stno"})
                    else ""
                ),
                "studentName": (
                    soup.find("input", {"name": "namekor"}).get("value", "")
                    if soup.find("input", {"name": "namekor"})
                    else ""
                ),
                "gender": (
                    soup.find("input", {"name": "sex"}).get("value", "")
                    if soup.find("input", {"name": "sex"})
                    else ""
                ),
                "roomInfo": (
                    soup.find("input", {"name": "roominfo"}).get("value", "")
                    if soup.find("input", {"name": "roominfo"})
                    else ""
                ),
                "phone": (
                    soup.find("input", {"name": "cellno"}).get("value", "")
                    if soup.find("input", {"name": "cellno"})
                    else ""
                ),
            }
            await submit(extracted_data, start_date, end_date, jsession_id)
            
            return {
                "status_code": response.status_code,
                "message": "기숙사 정보 추출 성공",
                "data": extracted_data
            }
                    
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=500, detail=f"기숙사 서버 통신 오류: {exc}")
        
# 외박 신청
async def submit(extracted_data, start_date, end_date, jsession_id):
    target_url = "https://www.ggdorm.or.kr/ko/index/mypage/stayout/"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua.chrome
    }

    cookies = {
        "JSESSIONID" : jsession_id
    }

    print("submit")
    print(extracted_data)

    payload = {
        "startYmd": start_date,
        "endYmd": end_date,  
        "reason": "본가",
        "mode": "regist",
        "type": "write",
        "campus": "1",
        "registrationNo": extracted_data["registrationNo"],
        "seq": "",
        "stno": extracted_data["studentId"],
        "namekor": extracted_data["studentName"],  # 실제 성명 기입
        "sex": extracted_data["gender"],
        "roominfo": extracted_data["roomInfo"],
        "cellno": extracted_data["phone"],
        "startHh": "00",
        "endHh": "00"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                target_url, 
                headers=headers, 
                cookies=cookies,
                data=payload,
                timeout=10.0
            )
            print("@@@@@@@@@@@@@@@@@@@@@@@@@")
            
            print({
                "status_code": response.status_code,
                "message": "외박 신청 요청 완료",
                "html_preview": response.text
            }
            )
            
        except httpx.HTTPError as exc:
            print(exec)
            raise HTTPException(status_code=500, detail=f"기숙사 서버 통신 오류: {exc}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)