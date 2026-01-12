<script lang="ts">
    import { resolve } from "$app/paths";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import type { PageProps } from "./$types";
    import { m } from "$lib/paraglide/messages";
    import { page as pagestate } from "$app/state";
    import { ArrowLeftIcon, ArrowRightIcon } from "lucide-svelte";

    let { data }: PageProps = $props();

    const PAGE_SIZE = 10;

    let page = $state(1);

    const start = $derived((page - 1) * PAGE_SIZE);
    const end = $derived(start + PAGE_SIZE);
    const lemmas = $derived(data.lemmas.slice(start, end));
</script>

<h5 class="h5 my-2 text-surface-950-50">
    {m.search_result({ count: data.lemmas.length })}
</h5>
<div class="min-w-124 w-1/4 flex flex-col gap-2">
    <div
        class="card py-2 w-full bg-surface-100-900 border border-surface-200-800"
    >
        <div class="flex flex-col gap-2">
            {#each lemmas as lemma}
                <a
                    class="btn mx-2 hover:preset-tonal justify-start"
                    href={resolve(`/lookup/${pagestate.params.lang}/${lemma}`)}
                >
                    {lemma}
                </a>
                {#if !(lemma === lemmas[lemmas.length - 1])}
                    <hr class="hr border-surface-200-800" />
                {/if}
            {/each}
        </div>
    </div>

    {#if data.lemmas.length > 10}
        <div class="flex justify-center">
            <Pagination
                class="preset-filled-surface-100-900"
                count={data.lemmas.length}
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
