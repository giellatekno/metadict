<script lang="ts">
    import { m } from "$lib/paraglide/messages";
    import { ScanTextIcon } from "lucide-svelte";
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
    let rendered = $derived(data.rendered);
    let neighbors = $derived(data.neighbors);
    let dictionary = $derived(data.dictionary);
</script>

<div class="grid w-full grid-cols-5 gap-20">
    <div
        class="card bg-tertiary-50-950 col-span-3 h-fit w-full border p-4 shadow-lg"
    >
        {#if neighbors && neighbors.length > 1}
            {#each neighbors as neighbor}
                {#if neighbor === rendered}
                    <div
                        class="border-primary-500 border-y-2 px-2 py-3 text-xl"
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
            <div>
                {@html rendered}
            </div>
        {/if}
    </div>

    {#if dictionary}
        <div
            class="card bg-tertiary-50-950 col-span-2 flex h-fit w-full flex-col gap-2 border p-4 shadow-lg"
        >
            <h3 class="h4 text-surface-950-50 font-bold">{dictionary[0]}</h3>
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
            <!-- OCR  -->
            <!-- <ScanTextIcon /> -->
        </div>
    {/if}
</div>
