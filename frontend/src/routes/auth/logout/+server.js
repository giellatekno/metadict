import { redirect } from "@sveltejs/kit";
import { base } from "$app/paths";

export async function GET({ cookies }) {
    cookies.delete("metadict-creds", { path: "/" });
    redirect(303, `${base}/`);
}
