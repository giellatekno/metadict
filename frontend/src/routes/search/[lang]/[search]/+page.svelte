<script lang="ts">
    import { resolve } from "$app/paths";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import type { PageProps } from "./$types";
    import { m } from "$lib/paraglide/messages";
    import { page as pagestate } from "$app/state";
    import { ArrowLeftIcon, ArrowRightIcon } from "lucide-svelte";

    let { data }: PageProps = $props();

    const PAGE_SIZE = 10;

    let page = $state(1);

    let start = $derived((page - 1) * PAGE_SIZE);
    let end = $derived(start + PAGE_SIZE);
    let lemmas = $derived(data.lemmas ? data.lemmas.slice(start, end) : []);
    let n_results = $derived(data.lemmas ? data.lemmas.length : 0);
</script>

<h5 class="h5 text-surface-950-50 mb-4">
    {m.search_result({ count: n_results })}
</h5>
{#if n_results}
    <div class="flex w-1/4 min-w-124 flex-col gap-2">
        <div
            class="card bg-surface-100-900 border-surface-200-800 w-full border py-2"
        >
            <div class="flex flex-col gap-2">
                {#each lemmas as lemma}
                    <a
                        class="btn hover:preset-tonal mx-2 justify-start"
                        href={resolve(
                            `/lookup/${pagestate.params.lang}/${lemma}`,
                        )}
                    >
                        {lemma}
                    </a>
                    {#if !(lemma === lemmas[lemmas.length - 1])}
                        <hr class="hr border-surface-200-800" />
                    {/if}
                {/each}
            </div>
        </div>

        {#if n_results > 10}
            <div class="flex w-full justify-center">
                <Pagination
                    class="preset-filled-surface-100-900 flex w-full justify-between"
                    count={n_results}
                    pageSize={PAGE_SIZE}
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
            </div>
        {/if}
    </div>
{/if}
