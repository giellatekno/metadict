<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { PageData } from "./$types";
    import type { Snippet } from "svelte";
    import { ExternalLink } from "lucide-svelte";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ? page.params.lang : "");
    let lemma = $derived(page.params.lemma ? page.params.lemma : "");
    let n_dicts = $derived(
        new Set(data.entries.map((item: Array<any>) => item[1])).size,
    );

    // Create a list of the historical dicts (e.g. published before 1979 (newest orthography))
    let hist_dicts: Array<any> = $derived.by(() => {
        let arr = [];
        if (data && data.entries.length > 0) {
            arr = data.entries.filter((item: Array<any>) => {
                return item[4] !== "" && Number(item[4].slice(-4)) < 1979;
            });
        }
        return arr;
    });

    // Filter out the historical dicts
    let dicts = $derived(
        data.entries.filter((item: Array<any>) => {
            return !hist_dicts.includes(item);
        }),
    );

    // Find all unique translation languages
    let tr_langs = $derived(
        Array.from(new Set(dicts.map((item: Array<any>) => item[3]))),
    );

    // Sort list to show: xxx-sme, xxx-nob, xxx-other-langs
    let sorted_tr_langs = $derived([
        ...tr_langs.filter((elm) => elm === "sme"),
        ...tr_langs.filter((elm) => elm === "nob"),
        ...tr_langs.filter((elm) => elm !== "sme" && elm !== "nob"),
    ]);

    let result_text = $derived(
        m.lookup_result({ lemma, count: n_dicts })
    );
</script>

<h5 class="h6 my-2 ml-2 text-surface-950-50">{result_text}</h5>

<main class="w-full grid grid-rows-3 md:grid-cols-3 gap-20">
    <div class="flex flex-col">
        <div
            class="flex flex-col w-full h-fit p-2 card bg-surface-100-900 border border-surface-200-800"
        >
            {#each sorted_tr_langs as tr_lang}
                <h6 class="h6">
                    <b>
                        {langname(lang, getLocale())} → {langname(tr_lang, getLocale())}
                    </b>
                </h6>
                <div>
                    {#each dicts as [lemma, dictionary_name, article_id, lang2, _]}
                        {#if tr_lang === lang2}
                            <a
                                class="btn hover:preset-tonal w-full my-1 justify-start"
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
