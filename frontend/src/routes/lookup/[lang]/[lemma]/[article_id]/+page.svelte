<script lang="ts">
    import { m } from "$lib/paraglide/messages";
    import {
        BookTextIcon,
        CalendarDaysIcon,
        HashIcon,
        ScanTextIcon,
        UserIcon,
        type Icon as IconType,
    } from "@lucide/svelte";
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
    let article = $derived(data.article_data.article);
    let dictionary_info = $derived(data.article_data.dictionary_info);
    let neighbors = $derived(data.article_data.neighbors);
</script>

<div class="grid grid-cols-1 gap-6 xl:grid-cols-4">
    <div
        class="card bg-tertiary-50-950 w-full overflow-y-auto border p-4 shadow-lg xl:col-span-3"
    >
        {#if neighbors && neighbors.length > 1}
            {#each neighbors as neighbor, i}
                {#if i !== 0}
                    <hr class="hr border-primary-500" />
                {/if}
                {#if neighbor.article_number === article.article_number}
                    <div
                        id="article"
                        class="border-primary-500 border-y-3 py-4 pl-2 sm:text-lg xl:text-2xl"
                    >
                        {@html neighbor.rendered}
                    </div>
                {:else}
                    <div class="py-2 text-xs opacity-90 xl:text-sm">
                        {@html neighbor.rendered}
                    </div>
                {/if}
            {/each}
        {:else if neighbors && neighbors.length === 1}
            <div>
                {@html article.rendered}
            </div>
        {/if}
    </div>

    {#if dictionary_info}
        <div
            class="card bg-tertiary-50-950 grid h-fit w-full grid-cols-2 gap-4 border p-4 shadow-lg xl:grid-cols-1"
        >
            {@render dictionary_info_group(
                m.dictionary_title(),
                dictionary_info.name,
                BookTextIcon,
            )}
            {#if dictionary_info.author}
                {@render dictionary_info_group(
                    m.dictionary_authors(),
                    dictionary_info.author,
                    UserIcon,
                )}
            {/if}
            {#if dictionary_info.date_published}
                {@render dictionary_info_group(
                    m.dictionary_year_published(),
                    dictionary_info.date_published,
                    CalendarDaysIcon,
                )}
            {/if}
            {#if dictionary_info.isbn}
                {@render dictionary_info_group("ISBN", dictionary_info.isbn, HashIcon)}
            {/if}
            {#if dictionary_info.is_ocr_read}
                {@render dictionary_info_group(
                    "OCR",
                    m.dictionary_ocr_read(),
                    ScanTextIcon,
                )}
            {/if}
            {#if !(dictionary_info.author || dictionary_info.date_published || dictionary_info.isbn || dictionary_info.is_ocr_read)}
                <p>{m.dictionary_no_additional_info()}</p>
            {/if}
        </div>
    {/if}
</div>

{#snippet dictionary_info_group(header: string, content: string, Icon: typeof IconType)}
    <div class="flex flex-col">
        <h6 class="h6 flex flex-row items-center gap-1">
            <Icon class="size-5" />
            {header}:
        </h6>
        <p class="pl-6 opacity-80">{content}</p>
    </div>
{/snippet}
