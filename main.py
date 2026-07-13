from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fake_useragent import UserAgent
import httpx

app = FastAPI()
ua = UserAgent()

# 로그인

@app.post("/login-test")
async def login_test(
    loginId: str = Form(...),
    loginPwd: str = Form(...)
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
        
        print(await fetch_user_info(jsession_id, registration_no))

        return jsession_id, registration_no
    
# 외박 신청을 위한 사용자 정보 확인
async def fetch_user_info(jsession_id, registration_no):
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
            
            return {
                "status_code": response.status_code,
                "message": "기숙사 정보 추출 성공",
                "data": extracted_data
            }
                    
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=500, detail=f"기숙사 서버 통신 오류: {exc}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)