import type { RequestHandler } from './$types';
import { redirect } from "@sveltejs/kit";
import { resolve } from "$app/paths";

export const GET: RequestHandler = async ({ cookies }) => {
    cookies.delete("metadict-creds", { path: "/" });
    redirect(303, resolve("/"));
}
