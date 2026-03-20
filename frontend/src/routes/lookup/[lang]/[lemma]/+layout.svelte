<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { PageData } from "./$types";
    import { type Snippet } from "svelte";
    import { ExternalLink } from "lucide-svelte";
    import { externalDicts } from "$lib/external_dicts";
    import { settings, type LangConfig } from "$lib/settings.svelte";
    import { goto } from "$app/navigation";
    import { type LookupType } from "$lib/utils";

    interface Props {
        data: PageData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ?? "");
    let lemma = $derived(page.params.lemma ?? "");

    function is_enabled(list: LangConfig[], code: string) {
        return list.find((l) => l.iso === code)?.enabled ?? false;
    }

    function sort_entries(entries: LookupType) {
        return [...entries].sort((a, b) => {
            // Sort first by lang1
            const rankSourceA = settings.selected_search_langs.findIndex(
                (l) => l.iso === a.lang1,
            );
            const rankSourceB = settings.selected_search_langs.findIndex(
                (l) => l.iso === b.lang1,
            );
            if (rankSourceA !== rankSourceB) {
                return rankSourceA - rankSourceB;
            }

            // If lang1 equal, sort by lang2
            const rankTargetA = settings.selected_target_langs.findIndex(
                (l) => l.iso === a.lang2,
            );
            const rankTargetB = settings.selected_target_langs.findIndex(
                (l) => l.iso === b.lang2,
            );
            if (rankTargetA !== rankTargetB) return rankTargetA - rankTargetB;

            // If lang2 equal, sort alphabetically
            return a.dictionary_name.localeCompare(b.dictionary_name);
        });
    }

    // Create a list of the historical dicts
    let hist_dicts = $derived(data.entries.filter((item) => item.is_historic));

    // Filter out the historical dicts
    let dicts = $derived(
        sort_entries(
            data.entries.filter((item) => {
                return (
                    !hist_dicts.includes(item) &&
                    is_enabled(settings.selected_search_langs, item.lang1) &&
                    is_enabled(settings.selected_target_langs, item.lang2)
                );
            }),
        ),
    );

    const groupedDicts = $derived.by(() => {
        const groups: Record<string, LookupType> = {};

        for (const d of dicts) {
            const key = `${d.lang1}-${d.lang2}`;
            if (!groups[key]) groups[key] = [];
            groups[key].push(d);
        }
        return groups;
    });

    // Get external dicts only for langs that dicts have lemma as lang1
    const src_langs = $derived([...new Set(dicts.map((d) => d.lang1))]);
    const filteredExternal = $derived(
        src_langs
            .filter(
                (lang) =>
                    externalDicts[lang] && externalDicts[lang].length !== 0,
            )
            .map((lang) => [lang, externalDicts[lang]] as const),
    );

    // Allows navigating with arrow keys
    let all_article_ids = $derived(
        [...dicts, ...hist_dicts].map((e) => e.article_id.toString()),
    );

    let cur_article_idx = $state(0);
    let cur_article = $derived(all_article_ids[cur_article_idx]);
    // Update cur_article_idx if url has id
    $effect(() => {
        const id = page.params.article_id;
        if (id) {
            const foundIdx = all_article_ids.indexOf(id);
            if (foundIdx !== -1) cur_article_idx = foundIdx;
        }
    });
    // if cur_article changes, navigate to it
    $effect(() => {
        if (
            cur_article_idx >= 0 &&
            cur_article_idx < all_article_ids.length &&
            cur_article !== ""
        ) {
            goto(resolve(`/lookup/${lang}/${lemma}/${cur_article}`), {
                keepFocus: true,
                replaceState: true,
            });
        }
    });

    function handleKeyDown(e: KeyboardEvent) {
        if (all_article_ids.length === 0) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            cur_article_idx = (cur_article_idx + 1) % all_article_ids.length;
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            cur_article_idx =
                (cur_article_idx - 1 + all_article_ids.length) %
                all_article_ids.length;
        }
    }
</script>

<svelte:window onkeydown={handleKeyDown} />

<main class="grid w-full grid-cols-4 gap-20">
    <div class="flex flex-col">
        <div
            class="card preset-filled-tertiary-50-950 flex h-fit w-full flex-col gap-1 p-4 shadow-lg"
        >
            <div class="flex flex-col gap-4">
                {#each Object.values(groupedDicts) as dictionaries}
                    <div class="mb-4 flex flex-col gap-2">
                        <h4 class="h4">
                            {langname(dictionaries[0].lang1, getLocale())} →
                            {langname(dictionaries[0].lang2, getLocale())}
                        </h4>
                        <hr class="hr" />

                        <div class="flex flex-col">
                            {#each dictionaries as dict}
                                {@render link_button(
                                    dict.article_id.toString(),
                                    resolve(
                                        `/lookup/${lang}/${lemma}/${dict.article_id}`,
                                    ),
                                    dict.dictionary_name,
                                )}
                            {/each}
                        </div>
                    </div>
                {/each}

                {#if hist_dicts.length > 0 && is_enabled(settings.selected_target_langs, "hst")}
                    <div class="flex flex-col gap-2">
                        <h4 class="h4">{m.historical_dictionaries()}</h4>
                        <hr class="hr" />
                        <div class="flex flex-col">
                            {#each hist_dicts as dict}
                                {@render link_button(
                                    dict.article_id.toString(),
                                    resolve(
                                        `/lookup/${lang}/${lemma}/${dict.article_id}`,
                                    ),
                                    dict.dictionary_name,
                                )}
                            {/each}
                        </div>
                    </div>
                {/if}
                {#if is_enabled(settings.selected_target_langs, "ext")}
                    {#each filteredExternal as [lang, dicts]}
                        <div class="flex flex-col gap-2">
                            <h4 class="h4">
                                {m.external_dictionaries()} ({lang})
                            </h4>
                            <hr class="hr" />
                            <div class="flex flex-col">
                                {#each dicts as { name, link }}
                                    {@const formatted_link = link.replaceAll(
                                        "{%string%}",
                                        lemma,
                                    )}
                                    {@render link_button(
                                        null,
                                        formatted_link,
                                        name,
                                        true,
                                    )}
                                {/each}
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>

    <div class="row-span-3 md:col-span-3">
        {@render children?.()}
    </div>
</main>

{#snippet link_button(
    id: null | string,
    href: string,
    label: string,
    external = false,
)}
    <a
        {id}
        class="btn my-1 w-full justify-start transition-colors {id ===
        cur_article
            ? 'preset-filled-primary-500'
            : 'preset-filled-primary-200-800'}"
        {href}
        target={external ? "_blank" : ""}
    >
        <span class="truncate">{label}</span>
        {#if external}
            <ExternalLink class="size-5" />
        {/if}
    </a>
{/snippet}
