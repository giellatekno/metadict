import { ArticleResponse } from "$lib/schemas";
import type { PageLoad } from "./$types";
import { api_fetch } from "$lib/utils";

export const load: PageLoad = async ({ params, fetch }) => {
    let { article_id } = params;

    const result = await api_fetch(`article/${article_id}`, fetch, ArticleResponse);
    return { article_data: result };
};
