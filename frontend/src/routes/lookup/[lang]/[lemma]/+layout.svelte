<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { PageData } from "./$types";
    import { type Snippet } from "svelte";
    import { ExternalLink } from "lucide-svelte";
    import type { LookupType } from "$lib/utils";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ?? "");
    let lemma = $derived(page.params.lemma ?? "");

    const externalDicts: Record<string, { name: string; link: string }[]> = {
        deu: [
            {
                name: "Wiktionary",
                link: "https://de.wiktionary.org/wiki/{%string%}",
            },
        ],
        est: [
            {
                name: "Sõnaveeb",
                link: "https://sonaveeb.ee/search/unif/dlall/dsall/{%string%}/1/est",
            },
            {
                name: "Wiktionary",
                link: "https://et.wiktionary.org/wiki/{%string%}",
            },
        ],
        // eng: [],
        fin: [
            {
                name: "Kielitoimiston sanakirja",
                link: "https://www.kielitoimistonsanakirja.fi/#/{%string%}",
            },
            {
                name: "Wiktionary",
                link: "https://fi.wiktionary.org/wiki/{%string%}",
            },
        ],
        nob: [
            {
                name: "ordbøkene.no",
                link: "https://ordbokene.no/nob/bm,nn/{%string%}",
            },
            {
                name: "Davvi girji",
                link: "https://533.davvi.no/ordbok_norsam.php?finn={%string%}",
            },
        ],
        sma: [],
        sme: [
            {
                name: "Davvi girji",
                link: "https://533.davvi.no/ordbok_samnor.php?finn={%string%}",
            },
        ],
        smj: [],
        smn: [],
        swe: [
            {
                name: "Svenska Akademiens ordböcker",
                link: "https://svenska.se/?q={%string%}",
            },
        ],
    };

    // Create a list of the historical dicts (e.g. published before 1979 (newest orthography))
    let hist_dicts: LookupType = $derived(
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
        <div
            class="card bg-tertiary-50-950 flex h-fit w-full flex-col border p-4 shadow-lg"
        >
            {#each sorted_tr_langs as tr_lang}
                <h6 class="h6 font-bold">
                    {langname(lang, getLocale())} → {langname(
                        tr_lang,
                        getLocale(),
                    )}
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
                <h6 class="h6 font-bold">
                    {m.historical_dictionaries()}
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
            {#if externalDicts[lang] && externalDicts[lang].length > 0}
                <h6 class="h6 font-bold">Eksterne Ordbøker</h6>
                {#each externalDicts[lang] as { name, link }}
                    {@const formatted_link = link.replaceAll(
                        "{%string%}",
                        lemma,
                    )}
                    <a
                        class="btn hover:preset-tonal my-1 w-full justify-start"
                        href={formatted_link}
                        target="_blank"
                    >
                        <span>{name}</span>
                        <ExternalLink />
                    </a>
                {/each}
            {/if}
        </div>
    </div>

    <div class="row-span-2 md:col-span-2">
        {@render children?.()}
    </div>
</main>
