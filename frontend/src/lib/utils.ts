import { z } from "zod";
import { resolve } from "$app/paths";
import { error } from "@sveltejs/kit";

export const SEARCH_OPTIONS = ["sme", "sma", "smj", "smn", "fin", "nob"];
export const TARGET_OPTIONS = [...SEARCH_OPTIONS, "hst", "ext"];

export const LANG_COLORS: Record<string, string> = {
    smn: "bg-red-600",
    nob: "bg-amber-500",
    sma: "bg-green-600",
    fin: "bg-teal-500",
    sme: "bg-blue-600",
    est: "bg-violet-600",
    smj: "bg-fuchsia-600",
};

export async function api_fetch<T extends z.ZodTypeAny = z.ZodUnknown>(
    path: string,
    fetchFn: typeof fetch,
    schema: T,
): Promise<z.infer<T>> {
    let response;
    try {
        response = await fetchFn(resolve("/api/[...path]", { path }));
    } catch (e) {
        console.error(e);
        error(502, "Failed to communicate with API");
    }

    if (!response.ok) {
        const errorText = await response.text();
        console.error(errorText);
        error(response.status, response.statusText);
    }

    let json;
    try {
        json = await response.json();
    } catch (e) {
        console.error(e);
        error(502, "API returned invalid JSON");
    }

    if (json.error) {
        console.error(json.error);
        error(502, `API error: "${json.error}"`);
    }

    try {
        return schema.parse(json) as z.infer<T>;
    } catch (e) {
        console.error(e);
        error(502, "Unexpected response format from API");
    }
}
