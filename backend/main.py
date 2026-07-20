from datetime import date, timedelta

from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fake_useragent import UserAgent
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
ua = UserAgent()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://www.ggdorm.or.kr"

DEFAULT_HEADER = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua.chrome
    }

def get_input_value(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("input", {"name": name})
    return tag.get("value", "") if tag else ""

@app.post("/stayout")
async def stayout(
    loginId: str = Form(...),
    loginPwd: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...)
):
    async with httpx.AsyncClient(
        follow_redirects=True,
        headers=DEFAULT_HEADER,
        timeout=10
    ) as client:

        registration_no = await login(
            client,
            loginId,
            loginPwd
        )

        user_info = await fetch_user_info(
            client,
            registration_no
        )

        await submit_stayout(
            client,
            user_info,
            start_date,
            end_date
        )

        return {
            "success": True,
            "message": "외박 신청이 완료되었습니다."
        }
    
async def login(
    client: httpx.AsyncClient,
    login_id: str,
    login_pwd: str,
) -> str:

    response = await client.post(
        BASE_URL + "/user/login",
        data={
            "retUrl": "/ko/index/mypage/stayout/",
            "loginId": login_id,
            "loginPwd": login_pwd,
        },
    )

    soup = BeautifulSoup(response.text, "html.parser")

    registration_no = get_input_value(
        soup,
        "registrationNo"
    )

    if not registration_no:
        raise HTTPException(
            status_code=401,
            detail="로그인에 실패했습니다."
        )

    return registration_no

async def fetch_user_info(
    client: httpx.AsyncClient,
    registration_no: str,
):

    response = await client.post(
        BASE_URL + "/ko/index/mypage/stayout/",
        data={
            "registrationNo": registration_no,
            "mode": "write"
        }
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {
        "registrationNo": registration_no,
        "studentId": get_input_value(soup, "stno"),
        "studentName": get_input_value(soup, "namekor"),
        "gender": get_input_value(soup, "sex"),
        "roomInfo": get_input_value(soup, "roominfo"),
        "phone": get_input_value(soup, "cellno"),
    }

async def submit_stayout(
    client: httpx.AsyncClient,
    user: dict,
    start_date: date,
    end_date: date,
):

    payload = {
        "startYmd": start_date,
        "endYmd": end_date,
        "reason": "본가",
        "mode": "regist",
        "type": "write",
        "campus": "1",
        "registrationNo": user["registrationNo"],
        "seq": "",
        "stno": user["studentId"],
        "namekor": user["studentName"],
        "sex": user["gender"],
        "roominfo": user["roomInfo"],
        "cellno": user["phone"],
        "startHh": "00",
        "endHh": "00",
    }

    await client.post(
        BASE_URL + "/ko/index/mypage/stayout/",
        data=payload
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)