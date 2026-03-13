<script lang="ts">
    import { resolve } from "$app/paths";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import type { PageProps } from "./$types";
    import { m } from "$lib/paraglide/messages";
    import { page as pagestate } from "$app/state";
    import { ArrowLeftIcon, ArrowRightIcon } from "lucide-svelte";
    import { LANG_COLORS } from "$lib/utils";

    let { data }: PageProps = $props();

    let pageSize = $state(20);

    let page = $state(1);

    let start = $derived((page - 1) * pageSize);
    let end = $derived(start + pageSize);
    let shownLemmas = $derived(
        data.lemmas ? data.lemmas.slice(start, end) : [],
    );
    let n_results = $derived(data.lemmas ? data.lemmas.length : 0);
</script>

<div class="flex w-1/4 min-w-124 flex-col items-center gap-4">
    {#if n_results > 0}
        <div class="flex w-full items-center justify-between">
            <div class="text-nowrap">
                {m.search_hits({ count: n_results })}
            </div>
            <div class="flex flex-row items-center gap-2">
                <label for="hits-per-page" class="">
                    {m.search_hits_per_page()}
                </label>
                <select
                    name="hits-per-page"
                    class="select w-fit"
                    value={String(pageSize)}
                    onchange={(e) => (pageSize = Number(e.currentTarget.value))}
                >
                    <option value="20">20</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                </select>
            </div>
        </div>
        {#if n_results}
            <div class="flex w-full flex-col gap-2">
                <div class="card bg-tertiary-50-950 w-full shadow-lg">
                    <div class="flex flex-col">
                        {#each shownLemmas as { lang, lemma }, i}
                            {@const rounded_style =
                                i === 0
                                    ? "rounded-t-xl rounded-b-none"
                                    : i === shownLemmas.length - 1
                                      ? "rounded-b-xl rounded-t-none"
                                      : "rounded-none"}
                            {#if i !== 0}
                                <hr class="hr border-surface-200-800" />
                            {/if}
                            <a
                                class="btn hover:preset-tonal justify-between py-3 {rounded_style}"
                                href={resolve(
                                    `/lookup/${pagestate.params.lang}/${lemma}`,
                                )}
                            >
                                {lemma}
                                <span
                                    class="badge preset-filled {LANG_COLORS[
                                        lang
                                    ]}"
                                >
                                    {lang.toUpperCase()}
                                </span>
                            </a>
                        {/each}
                    </div>
                </div>
            </div>
            {#if n_results > 10}
                <Pagination
                    class="preset-filled-tertiary-50-950 flex w-fit min-w-1/2 justify-between"
                    count={n_results}
                    {pageSize}
                    {page}
                    onPageChange={(event) => (page = event.page)}
                >
                    <Pagination.PrevTrigger>
                        <ArrowLeftIcon class="size-4" />
                    </Pagination.PrevTrigger>
                    <Pagination.Context>
                        {#snippet children(pagination)}
                            {#each pagination().pages as page, index (page)}
                                {#if page.type === "page"}
                                    <Pagination.Item {...page}>
                                        {page.value}
                                    </Pagination.Item>
                                {:else}
                                    <Pagination.Ellipsis {index}>
                                        &#8230;
                                    </Pagination.Ellipsis>
                                {/if}
                            {/each}
                        {/snippet}
                    </Pagination.Context>
                    <Pagination.NextTrigger>
                        <ArrowRightIcon class="size-4" />
                    </Pagination.NextTrigger>
                </Pagination>
            {/if}
        {/if}
    {:else}
        <span class="text-lg">{m.search_no_results()}</span>
    {/if}
</div>
