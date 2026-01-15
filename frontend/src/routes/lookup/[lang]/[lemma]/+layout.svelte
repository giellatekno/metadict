<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { PageData } from "./$types";
    import type { Snippet } from "svelte";
    import { ExternalLink } from "lucide-svelte";
    import type { LookupResponse } from "$lib/utils";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ?? "");
    let lemma = $derived(page.params.lemma ?? "");
    let n_dicts = $derived(new Set(data.entries.map((item) => item[1])).size);

    // Create a list of the historical dicts (e.g. published before 1979 (newest orthography))
    let hist_dicts: LookupResponse = $derived(
        data.entries.filter((item) => {
            return item[4] !== "" && Number(item[4].slice(-4)) < 1979;
        }),
    );

    // Filter out the historical dicts
    let dicts = $derived(
        data.entries.filter((item) => {
            return !hist_dicts.includes(item);
        }),
    );

    // Find all unique translation languages and
    // sort list to show: xxx-sme, xxx-nob, xxx-fin, xxx-other-langs
    const priority: Record<string, number> = { sme: 1, nob: 2, fin: 3 };
    let sorted_tr_langs = $derived(
        Array.from(new Set(dicts.map((item) => item[3]))).toSorted((a, b) => {
            const scoreA = priority[a] ?? 3;
            const scoreB = priority[b] ?? 3;
            return scoreA - scoreB;
        }),
    );
</script>

<main class="grid w-full grid-cols-3 gap-20">
    <div class="flex flex-col">
        <h5 class="h6 text-surface-950-50 mb-4">
            {m.lookup_result({ lemma, count: n_dicts })}
        </h5>
        <div
            class="card bg-surface-100-900 border-surface-200-800 flex h-fit w-full flex-col border p-2"
        >
            {#each sorted_tr_langs as tr_lang}
                <h6 class="h6">
                    <b>
                        {langname(lang, getLocale())} → {langname(
                            tr_lang,
                            getLocale(),
                        )}
                    </b>
                </h6>
                <div>
                    {#each dicts as [lemma, dictionary_name, article_id, lang2, _]}
                        {#if tr_lang === lang2}
                            <a
                                class="btn hover:preset-tonal my-1 w-full justify-start"
                                href={resolve(
                                    `/lookup/${lang}/${lemma}/${article_id}`,
                                )}
                            >
                                {dictionary_name.length > 30
                                    ? dictionary_name.slice(0, 30) + "..."
                                    : dictionary_name} ({lemma})
                            </a>
                        {/if}
                    {/each}
                </div>
            {/each}

            {#if hist_dicts.length > 0}
                <h6 class="h6">
                    <b>{m.historical_dictionaries()}</b>
                </h6>
                <nav class="list-nav">
                    {#each hist_dicts as [lemma, dictionary_name, article_id, _lang2, _]}
                        <a
                            class="btn hover:preset-tonal my-1 w-full justify-start"
                            href={resolve(
                                `/lookup/${lang}/${lemma}/${article_id}`,
                            )}
                        >
                            {dictionary_name.length > 30
                                ? dictionary_name.slice(0, 30) + "..."
                                : dictionary_name} ({lemma})
                        </a>
                    {/each}
                </nav>
            {/if}
        </div>
        {#if lang === "nob"}
            <div class="mt-4 flex flex-col gap-2">
                <a
                    class="btn preset-filled-primary-400-600 w-fit"
                    href={`https://ordbokene.no/nob/bm,nn/${lemma}`}
                    target="_blank"
                >
                    <span>{m.search_ordbokene({ lemma })}</span>
                    <ExternalLink />
                </a>
                <a
                    class="btn preset-filled-primary-400-600 w-fit"
                    href={`https://533.davvi.no/ordbok_norsam.php?finn=${lemma}`}
                    target="_blank"
                >
                    <span>{m.search_davvigirji({ lemma })}</span>
                    <ExternalLink />
                </a>
            </div>
        {:else if lang === "sme"}
            <div class="mt-4">
                <a
                    class="btn preset-filled-primary-400-600 w-fit"
                    href={`https://533.davvi.no/ordbok_samnor.php?finn=${lemma}`}
                    target="_blank"
                >
                    <span>{m.search_davvigirji({ lemma })}</span>
                    <ExternalLink />
                </a>
            </div>
        {/if}
    </div>

    <div class="row-span-2 md:col-span-2">
        {@render children?.()}
    </div>
</main>
