<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { locale, t } from "svelte-intl-precompile";
    import { resolve } from "$app/paths";
    import { Accordion, AccordionItem } from "@skeletonlabs/skeleton";
    import externalLinkIcon from "$assets/external-link.svg";
    import type { PageData } from "./$types";
    import type { Snippet } from "svelte";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang);
    let lemma = $derived(page.params.lemma);
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
        $t("lookup-result", { values: { lemma: lemma, count: n_dicts } }),
    );
</script>

<h5 class="h5 my-2">{result_text}</h5>

<main class="w-full grid grid-cols-3 gap-5">
    <div class="flex flex-col w-3/4">
        <Accordion class="card">
            {#each sorted_tr_langs as tr_lang}
                <AccordionItem open>
                    {#snippet summary()}
                        <h6 class="h6">
                            <b>
                                {langname(lang, $locale)} → {langname(
                                    tr_lang,
                                    $locale,
                                )}
                            </b>
                        </h6>
                    {/snippet}
                    {#snippet content()}
                        <nav class="list-nav">
                            {#each dicts as [lemma, dictionary_name, article_id, lang2, _]}
                                {#if tr_lang === lang2}
                                    <a
                                        href={resolve(
                                            `/lookup/${lang}/${lemma}/${article_id}`,
                                        )}
                                    >
                                        {dictionary_name.length > 30
                                            ? dictionary_name.slice(0, 30) +
                                              "..."
                                            : dictionary_name} ({lemma})
                                    </a>
                                {/if}
                            {/each}
                        </nav>
                    {/snippet}
                </AccordionItem>
            {/each}

            {#if hist_dicts.length > 0}
                <AccordionItem open>
                    {#snippet summary()}
                        <h6 class="h6">
                            <b>{$t("historical-dictionaries")}</b>
                        </h6>
                    {/snippet}
                    {#snippet content()}
                        <nav class="list-nav">
                            {#each hist_dicts as [lemma, dictionary_name, article_id, _lang2, _]}
                                <a
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
                    {/snippet}
                </AccordionItem>
            {/if}
        </Accordion>
        {#if lang === "nob"}
            <div class="p-4 mt-10">
                <a
                    class="btn variant-filled-primary"
                    href={`https://ordbokene.no/nob/bm,nn/${lemma}`}
                    target="_blank"
                >
                    <span>
                        {$t("search-ordbokene", { values: { lemma: lemma } })}
                    </span>
                    <img
                        src={externalLinkIcon}
                        alt="External link"
                        width="22"
                    />
                </a>
            </div>
        {/if}
    </div>

    <div class="flex col-span-2">
        {@render children?.()}
    </div>
</main>
