import { error } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import { ArticleResponse } from "$lib/utils";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, fetch }) => {
    let { article_id } = params;

    const res = await fetch(resolve(`/api/article/${article_id}`));

    if (!res.ok) {
        error(res.status, "fetch to api failed");
    }

    let json: unknown;
    try {
        json = await res.json();
    } catch {
        error(502, "api returned non-JSON response");
    }

    const parsed = ArticleResponse.safeParse(json);
    if (!parsed.success) {
        console.error(parsed.error);
        error(502, "bad response from api");
    }

    return { article_data: parsed.data };
};
