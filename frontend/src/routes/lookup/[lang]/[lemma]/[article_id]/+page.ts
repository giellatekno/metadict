import type { Load } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import { resolve } from "$app/paths";
import { ArticleResponse } from "$lib/utils";

export const load: Load = async ({ params, fetch }) => {
    let { article_id } = params;

    const response = await fetch(resolve(`/api/article/${article_id}`));

    if (!response.ok) {
        error(response.status, "fetch to api failed");
    }

    const article_data = ArticleResponse.parse(await response.json());

    return { article_data };
};
