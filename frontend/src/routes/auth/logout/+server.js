import { redirect } from "@sveltejs/kit";
import { env } from "$env/dynamic/public";

export async function GET({ cookies }) {
    cookies.delete("metadict-creds", { path: "/" });
    //redirect(303, `${env.PUBLIC_API_ENDPOINT}/auth/logout`);
    redirect(303, "/");
}
