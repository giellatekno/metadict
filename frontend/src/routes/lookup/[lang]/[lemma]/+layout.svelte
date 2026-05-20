<script lang="ts">
    import { page } from "$app/state";
    import { langname } from "$lib/langname";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages";
    import { resolve } from "$app/paths";
    import type { LayoutData } from "./$types";
    import { type Snippet } from "svelte";
    import { ExternalLink } from "@lucide/svelte";
    import { externalDicts } from "$lib/external_dicts";
    import { settings } from "$lib/settings.svelte";
    import { goto } from "$app/navigation";
    import { type LookupType } from "$lib/schemas";

    interface Props {
        data: LayoutData;
        children: Snippet;
    }

    let { data, children }: Props = $props();

    let lang = $derived(page.params.lang ?? "");
    let lemma = $derived(page.params.lemma ?? "");

    function getRank(iso: string) {
        const index = settings.selected_target_langs.findIndex(
            (l) => l.iso === iso,
        );
        return index === -1 ? 999 : index;
    }

    function is_enabled(code: string) {
        return (
            settings.selected_target_langs.find((l) => l.iso === code)
                ?.enabled ?? false
        );
    }

    const groupedStandard = $derived.by(() => {
        const groups = new Map<string, LookupType>();
        for (const d of data.entries) {
            if (d.is_historic || !is_enabled(d.lang2)) continue;
            if (!groups.has(d.lang2)) groups.set(d.lang2, []);
            groups.get(d.lang2)!.push(d);
        }
        for (const [_lang2, entries] of groups) {
            entries.sort((a, b) =>
                a.dictionary_name.localeCompare(b.dictionary_name),
            );
        }
        return groups;
    });

    const sections = $derived.by(() => {
        const list: {
            id: string;
            type: "standard" | "hst" | "ext";
            rank: number;
            data?: any;
        }[] = [];

        for (const [lang2, items] of groupedStandard) {
            list.push({
                id: lang2,
                type: "standard",
                rank: getRank(lang2),
                data: items,
            });
        }

        if (data.entries.some((e) => e.is_historic) && is_enabled("hst")) {
            list.push({
                id: "hst",
                type: "hst",
                rank: getRank("hst"),
                data: data.entries.filter((e) => e.is_historic),
            });
        }

        if (is_enabled("ext") && externalDicts[lang]) {
            list.push({ id: "ext", type: "ext", rank: getRank("ext") });
        }

        return list.sort((a, b) => a.rank - b.rank);
    });

    // Allows navigating with arrow keys
    let all_article_ids = $derived(
        sections
            .filter((s) => s.type !== "ext")
            .flatMap((s) => s.data.map((d: any) => d.article_id.toString())),
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
            goto(
                resolve("/lookup/[lang]/[lemma]/[article_id]", {
                    lang,
                    lemma,
                    article_id: cur_article,
                }),
                {
                    keepFocus: true,
                    replaceState: true,
                },
            );
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

<main class="grid w-full grid-cols-1 gap-6 sm:grid-cols-4 sm:gap-20">
    <div class="flex flex-col">
        <div
            class="card preset-filled-tertiary-50-950 flex h-fit w-full flex-col gap-1 p-4 shadow-lg"
        >
            <div class="flex flex-col gap-4">
                <h4 class="h4 font-bold">{langname(lang, getLocale())}</h4>
                {#each sections as section}
                    <div class="mb-4 flex flex-col gap-2">
                        <h5 class="h5 font-bold">
                            {#if section.type === "standard"}
                                → {langname(section.id, getLocale())}
                            {:else if section.type === "hst"}
                                {m.historical_dictionaries()}
                            {:else if section.type === "ext"}
                                {m.external_dictionaries()}
                            {/if}
                        </h5>

                        <hr class="hr" />

                        <div class="flex flex-col">
                            {#if section.type === "ext"}
                                {#each externalDicts[lang] as { name, link }}
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
                            {:else}
                                {#each section.data as dict}
                                    {@render link_button(
                                        dict.article_id.toString(),
                                        resolve(
                                            "/lookup/[lang]/[lemma]/[article_id]",
                                            {
                                                lang,
                                                lemma,
                                                article_id:
                                                    dict.article_id.toString(),
                                            },
                                        ),
                                        dict.dictionary_displayname === ""
                                            ? dict.dictionary_name
                                            : dict.dictionary_displayname,
                                    )}
                                {/each}
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>

    <div class="sm:col-span-3">
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
