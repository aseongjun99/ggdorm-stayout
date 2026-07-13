from bs4 import BeautifulSoup
from fastapi import FastAPI, Form
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

        jsessionid = client.cookies.get("JSESSIONID")

        html_text = response.text 
        print(response.status_code, response.text)
        print(html_text)


        soup = BeautifulSoup(html_text, "html.parser")

        print(soup.prettify())


        registration_no = soup.find(
            "input",
            {"name": "registrationNo"}
        )["value"]
        
        return jsessionid, registration_no

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)