<script lang="ts">
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages.js";
    import { langname } from "$lib/langname";
    import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
    import { settings, type LangConfig } from "$lib/settings.svelte";
    import { SEARCH_OPTIONS, TARGET_OPTIONS } from "$lib/utils";
    import {
        EllipsisIcon,
        GripVertical,
        RotateCcwIcon,
        XIcon,
    } from "lucide-svelte";

    function reset_list(listId: "search" | "target") {
        if (listId === "search") {
            settings.selected_search_langs = SEARCH_OPTIONS.map((iso) => ({
                iso,
                enabled: true,
            }));
        } else if (listId === "target") {
            settings.selected_target_langs = TARGET_OPTIONS.map((iso) => ({
                iso,
                enabled: true,
            }));
        }
    }

    let dragInfo = $state<{
        index: number | null;
        listId: "search" | "target" | null;
    }>({
        index: null,
        listId: null,
    });

    let activeSearchCount = $derived(
        settings.selected_search_langs.filter((l) => l.enabled).length,
    );
    let activeTargetCount = $derived(
        settings.selected_target_langs.filter((l) => l.enabled).length,
    );

    function handleDragStart(index: number, listId: "search" | "target") {
        dragInfo = { index, listId };
    }

    function handleDragOver(
        e: DragEvent,
        index: number,
        listId: "search" | "target",
        list: LangConfig[],
    ) {
        e.preventDefault();
        if (
            dragInfo.index === null ||
            dragInfo.index === index ||
            dragInfo.listId !== listId
        )
            return;

        const item = list.splice(dragInfo.index, 1)[0];
        list.splice(index, 0, item);
        dragInfo.index = index;
    }

    function handleDragEnd() {
        dragInfo = { index: null, listId: null };
    }

    // animation for search settings dialig
    const animation =
        "transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0";
</script>

<div class="flex w-fit flex-col">
    <Dialog>
        <Dialog.Trigger
            class="preset-filled-surface-200-800 hover:preset-filled-surface-100-900 border-surface-200-800 flex items-center justify-between gap-4 rounded-lg border px-4 py-1"
        >
            <span class="font-bold">
                {m.search_options()}
            </span>
            <EllipsisIcon class="size-5" />
        </Dialog.Trigger>
        <Portal>
            <Dialog.Backdrop class="bg-surface-50-950/50 fixed inset-0 z-50" />
            <Dialog.Positioner
                class="fixed inset-0 z-50 flex items-center justify-center p-4"
            >
                <Dialog.Content
                    class="card bg-tertiary-50-950 border-primary-500 w-fit space-y-4 border-2 p-6 shadow-xl {animation}"
                >
                    <header class="flex items-center justify-between">
                        <Dialog.Title class="h4 font-bold">
                            {m.search_options()}
                        </Dialog.Title>
                        <Dialog.CloseTrigger
                            class="hover:preset-tonal box-content rounded-md p-2"
                            title={m.close()}
                            aria-label={m.close()}
                        >
                            <XIcon class="size-6" />
                        </Dialog.CloseTrigger>
                    </header>
                    <Dialog.Description>
                        <div
                            class="align-start grid grid-cols-2 gap-12 text-lg"
                        >
                            <div class="flex flex-col gap-2">
                                <span
                                    class="flex items-center justify-between font-bold"
                                >
                                    {m.search_languages()}
                                    <button
                                        class="hover:preset-tonal box-content rounded-md p-2"
                                        onclick={() => reset_list("search")}
                                    >
                                        <RotateCcwIcon
                                            aria-label="[l6e] Reset list"
                                            class="size-4"
                                        />
                                    </button>
                                </span>
                                <hr class="hr" />
                                <div class="flex flex-col gap-2">
                                    {#each settings.selected_search_langs as langObj, i (langObj.iso)}
                                        {@render dnd_checkbox(
                                            langObj,
                                            i,
                                            settings.selected_search_langs,
                                            "search",
                                            activeSearchCount,
                                        )}
                                    {/each}
                                </div>
                            </div>
                            <div class="flex flex-col gap-2">
                                <span
                                    class="flex items-center justify-between font-bold"
                                >
                                    {m.target_languages()}
                                    <button
                                        class="hover:preset-tonal box-content rounded-md p-2"
                                        onclick={() => reset_list("target")}
                                    >
                                        <RotateCcwIcon class="size-4" />
                                    </button>
                                </span>
                                <hr class="hr" />
                                {#each settings.selected_target_langs as langObj, i (langObj.iso)}
                                    {@render dnd_checkbox(
                                        langObj,
                                        i,
                                        settings.selected_target_langs,
                                        "target",
                                        activeTargetCount,
                                    )}
                                {/each}
                                <div class="flex flex-col gap-2"></div>
                            </div>
                        </div>
                    </Dialog.Description>
                </Dialog.Content>
            </Dialog.Positioner>
        </Portal>
    </Dialog>
</div>

{#snippet dnd_checkbox(
    langObj: LangConfig,
    index: number,
    list: LangConfig[],
    listId: "search" | "target",
    totalActive: number,
)}
    <button
        ondragover={(e) => handleDragOver(e, index, listId, list)}
        onclick={() => (langObj.enabled = !langObj.enabled)}
        class="hover:bg-surface-100-900 flex items-center justify-between rounded p-1 transition-colors
        {dragInfo.index === index && dragInfo.listId === listId
            ? 'opacity-30'
            : ''}"
    >
        <span class="flex items-center gap-2">
            <input
                type="checkbox"
                class="checkbox"
                bind:checked={langObj.enabled}
                disabled={langObj.enabled && totalActive <= 1}
                title={langObj.enabled && totalActive <= 1
                    ? "[l6e] At least one language must be selected"
                    : ""}
            />
            <span class="text-base select-none">
                {#if langObj.iso === "hst"}
                    {m.historical_dictionaries()}
                {:else if langObj.iso === "ext"}
                    {m.external_dictionaries()}
                {:else}
                    {langname(langObj.iso, getLocale())}
                {/if}
            </span>
        </span>
        <div
            draggable="true"
            role="button"
            tabindex="0"
            aria-label="[l6e] Drag to reorder"
            class="cursor-grab p-1 active:cursor-grabbing"
            ondragstart={() => handleDragStart(index, listId)}
            ondragend={handleDragEnd}
        >
            <GripVertical class="size-4 shrink-0 opacity-40" />
        </div>
    </button>
{/snippet}
