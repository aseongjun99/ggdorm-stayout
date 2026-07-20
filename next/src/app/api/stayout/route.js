import { NextResponse } from "next/server";

import {
    login,
    fetchUserInfo,
    submitStayout,
} from "@/lib/dorm";

export async function POST(request) {
    try {
        const {
            loginId,
            loginPwd,
            start_date,
            end_date,
        } = await request.json();

        const loginResult = await login(
            loginId,
            loginPwd
        );

        const user = await fetchUserInfo(
            loginResult.jsessionid,
            loginResult.registrationNo
        );

        await submitStayout(
            loginResult.jsessionid,
            user,
            start_date,
            end_date
        );

        console.log(loginResult.jsessionid);
        console.log(user);
        console.log(start_date);
        console.log(end_date);

        return NextResponse.json({
            success: true,
            message: "외박 신청이 완료되었습니다.",
        });
    } catch (error) {
        return NextResponse.json(
            {
                success: false,
                message: error.message,
            },
            {
                status: 500,
            }
        );
    }
}