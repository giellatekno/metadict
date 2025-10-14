<script lang="ts">
    import { t } from "svelte-intl-precompile";
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
    let rendered = $derived(data.rendered);
    let neighbors = $derived(data.neighbors);
    let dictionary = $derived(data.dictionary);
</script>

<div class="grid grid-cols-5 gap-10 w-full">
    <div class="card col-span-3 py-2 px-2 w-full h-fit">
        {#if neighbors && neighbors.length > 1}
            {#each neighbors as neighbor}
                {#if neighbor === rendered}
                    <div
                        class="px-2 py-3 text-xl border-y-2 border-primary-500"
                    >
                        {@html neighbor}
                    </div>
                {:else}
                    <div class="py-1 text-sm">
                        {@html neighbor}
                    </div>
                {/if}
            {/each}
        {:else if neighbors && neighbors.length === 1}
            <div class="card">
                {@html rendered}
            </div>
        {/if}
    </div>

    {#if dictionary}
        <div class="card col-span-2 p-5 h-fit space-y-2">
            <h3 class="h3 font-medium">{dictionary[0]}</h3>
            {#if dictionary[1]}
                <div>
                    <h4 class="h4">{$t("authors")}:</h4>
                    <p>{dictionary[1]}</p>
                </div>
            {/if}
            {#if dictionary[2]}
                <div>
                    <h4 class="h4">{$t("year-published")}:</h4>
                    <p>{dictionary[2]}</p>
                </div>
            {/if}
            {#if dictionary[3]}
                <div>
                    <h4 class="h4">ISBN:</h4>
                    <p>{dictionary[3]}</p>
                </div>
            {/if}
            {#if !(dictionary[1] || dictionary[2] || dictionary[3])}
                <p>{$t("no-additional-info")}</p>
            {/if}
        </div>
    {/if}
</div>
