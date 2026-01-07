import type { Load } from "@sveltejs/kit";

export const load: Load = async ({ params, fetch }) => {
    const lemma = encodeURIComponent(params.lemma!);

    const response = await fetch(`/api/lookup/${params.lang}/${lemma}`);
    const entries = await response.json();

    return { entries };
}
