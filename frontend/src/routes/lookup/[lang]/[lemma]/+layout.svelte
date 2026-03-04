<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { PageData } from "./$types";
    import { type Snippet } from "svelte";
    import { ExternalLink } from "lucide-svelte";
    import { Accordion } from "@skeletonlabs/skeleton-svelte";
    import LookupAccordionItem from "$lib/components/LookupAccordionItem.svelte";
    import { externalDicts } from "$lib/external_dicts";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ?? "");
    let lemma = $derived(page.params.lemma ?? "");

    // Create a list of the historical dicts
    let hist_dicts = $derived(data.entries.filter((item) => item.is_historic));

    // Filter out the historical dicts
    let dicts = $derived(
        data.entries.filter((item) => {
            return !hist_dicts.includes(item);
        }),
    );

    // Find all unique translation languages and
    // sort list to show: xxx-sme, xxx-nob, xxx-fin, xxx-other-langs
    const priority: Record<string, number> = { sme: 1, sma: 2, nob: 3, fin: 4 };
    let sorted_tr_langs = $derived(
        Array.from(new Set(dicts.map((item) => item.lang2))).toSorted(
            (a, b) => {
                const scoreA = priority[a] ?? 3;
                const scoreB = priority[b] ?? 3;
                return scoreA - scoreB;
            },
        ),
    );

    let accordionValues = $derived([
        ...sorted_tr_langs,
        "historical",
        "external",
    ]);
    let highlightedId = $state("");
</script>

<main class="grid w-full grid-cols-4 gap-20">
    <div class="flex flex-col">
        <div
            class="card bg-tertiary-50-950 flex h-fit w-full flex-col gap-4 border p-4 shadow-lg"
        >
            <Accordion
                multiple
                value={accordionValues}
                onValueChange={(details) => (accordionValues = details.value)}
            >
                {#each sorted_tr_langs as tr_lang (tr_lang)}
                    {@const title =
                        langname(lang, getLocale()) +
                        " → " +
                        langname(tr_lang, getLocale())}
                    <LookupAccordionItem value={tr_lang} {title}>
                        {#each dicts as dict}
                            {#if tr_lang === dict.lang2}
                                {@render link_button(
                                    dict.article_id.toString(),
                                    resolve(
                                        `/lookup/${lang}/${lemma}/${dict.article_id}`,
                                    ),
                                    dict.dictionary_name,
                                )}
                            {/if}
                        {/each}
                    </LookupAccordionItem>
                {/each}

                {#if hist_dicts.length > 0}
                    <LookupAccordionItem
                        value="historical"
                        title={m.historical_dictionaries()}
                    >
                        {#each hist_dicts as dict}
                            {@render link_button(
                                dict.article_id.toString(),
                                resolve(
                                    `/lookup/${lang}/${lemma}/${dict.article_id}`,
                                ),
                                dict.dictionary_name,
                            )}
                        {/each}
                    </LookupAccordionItem>
                {/if}
                {#if externalDicts[lang] && externalDicts[lang].length > 0}
                    <LookupAccordionItem
                        value="external"
                        title={m.external_dictionaries()}
                    >
                        {#each externalDicts[lang] as { name, link }, i}
                            {@const formatted_link = link.replaceAll(
                                "{%string%}",
                                lemma,
                            )}
                            {@render link_button(
                                `external-${lang}-${i}`,
                                formatted_link,
                                name,
                                true,
                            )}
                        {/each}
                    </LookupAccordionItem>
                {/if}
            </Accordion>
        </div>
    </div>

    <div class="row-span-3 md:col-span-3">
        {@render children?.()}
    </div>
</main>

{#snippet link_button(
    id: string,
    href: string,
    label: string,
    external = false,
)}
    <a
        {id}
        class="btn my-1 w-full justify-start transition-colors {id ===
        highlightedId
            ? 'preset-filled-primary-500'
            : 'preset-filled-primary-200-800'}"
        {href}
        target={external ? "_blank" : ""}
        onclick={() => {
            if (!external) highlightedId = id;
        }}
    >
        <span class="truncate">{label}</span>
        {#if external}
            <ExternalLink class="size-5" />
        {/if}
    </a>
{/snippet}
