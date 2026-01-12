<script lang="ts">
    import { m } from "$lib/paraglide/messages";
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
    let rendered = $derived(data.rendered);
    let neighbors = $derived(data.neighbors);
    let dictionary = $derived(data.dictionary);
</script>

<div class="grid grid-cols-5 gap-20 w-full">
    <div
        class="card col-span-3 py-2 px-2 w-full h-fit bg-surface-100-900 border border-surface-200-800"
    >
        {#if neighbors && neighbors.length > 1}
            {#each neighbors as neighbor}
                {#if neighbor === rendered}
                    <div
                        class="px-2 py-3 text-xl border-y-2 border-primary-400-600"
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
        <div
            class="card col-span-2 p-5 h-fit space-y-2 bg-surface-100-900 border border-surface-200-800"
        >
            <h3 class="h4 font-medium text-surface-950-50">{dictionary[0]}</h3>
            <hr class="hr" />
            {#if dictionary[1]}
                <div>
                    <h4 class="h4">{m.authors()}:</h4>
                    <p>{dictionary[1]}</p>
                </div>
            {/if}
            {#if dictionary[2]}
                <div>
                    <h4 class="h4">{m.year_published()}:</h4>
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
                <p>{m.no_additional_info()}</p>
            {/if}
        </div>
    {/if}
</div>
