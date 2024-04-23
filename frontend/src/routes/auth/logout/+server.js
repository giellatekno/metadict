import { redirect } from "@sveltejs/kit";

const API_ENDPOINT = "http://localhost:3000/auth/logout";

export async function GET() {
    redirect(303, API_ENDPOINT);
}
