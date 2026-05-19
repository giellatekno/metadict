<script lang="ts">
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages.js";
    import { langname } from "$lib/langname";
    import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
    import { settings, type LangConfig } from "$lib/settings.svelte";
    import { SEARCH_OPTIONS, TARGET_OPTIONS } from "$lib/utils";
    import {
        ChevronDownIcon,
        ChevronUpIcon,
        EllipsisIcon,
        RotateCcwIcon,
        XIcon,
    } from "@lucide/svelte";

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

    let activeSearchCount = $derived(
        settings.selected_search_langs.filter((l) => l.enabled).length,
    );
    let activeTargetCount = $derived(
        settings.selected_target_langs.filter((l) => l.enabled).length,
    );

    function move(list: LangConfig[], index: number, direction: -1 | 1) {
        const target = index + direction;
        if (target < 0 || target >= list.length) return;
        const tmp = list[index];
        list[index] = list[target];
        list[target] = tmp;
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
                    class="card bg-tertiary-50-950 border-primary-500 max-h-[90vh] w-full max-w-[95vw] space-y-4 overflow-y-auto border-2 p-6 shadow-xl sm:w-fit {animation}"
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
                            class="align-start grid grid-cols-1 gap-4 text-lg sm:grid-cols-2 sm:gap-12"
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
                                            aria-label={m.options_reset_list()}
                                            class="size-4"
                                        />
                                    </button>
                                </span>
                                <hr class="hr" />
                                <div class="flex flex-col gap-2">
                                    {#each settings.selected_search_langs as langObj, i (langObj.iso)}
                                        {@render lang_row(
                                            langObj,
                                            i,
                                            settings.selected_search_langs,
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
                                        <RotateCcwIcon
                                            aria-label={m.options_reset_list()}
                                            class="size-4"
                                        />
                                    </button>
                                </span>
                                <hr class="hr" />
                                {#each settings.selected_target_langs as langObj, i (langObj.iso)}
                                    {@render lang_row(
                                        langObj,
                                        i,
                                        settings.selected_target_langs,
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

{#snippet lang_row(
    langObj: LangConfig,
    index: number,
    list: LangConfig[],
    totalActive: number,
)}
    <div class="flex items-center justify-between gap-1 rounded p-1">
        <label class="flex cursor-pointer items-center gap-2 select-none">
            <input
                type="checkbox"
                class="checkbox"
                bind:checked={langObj.enabled}
                disabled={langObj.enabled && totalActive <= 1}
                title={langObj.enabled && totalActive <= 1
                    ? m.options_selected_warning()
                    : ""}
            />
            <span class="text-base">
                {#if langObj.iso === "hst"}
                    {m.historical_dictionaries()}
                {:else if langObj.iso === "ext"}
                    {m.external_dictionaries()}
                {:else}
                    {langname(langObj.iso, getLocale())}
                {/if}
            </span>
        </label>
        <div class="flex flex-row">
            <button
                class="hover:preset-tonal rounded p-0.5 disabled:opacity-20"
                disabled={index === 0}
                onclick={() => move(list, index, -1)}
                aria-label={m.options_move_up()}
            >
                <ChevronUpIcon class="size-4" />
            </button>
            <button
                class="hover:preset-tonal rounded p-0.5 disabled:opacity-20"
                disabled={index === list.length - 1}
                onclick={() => move(list, index, 1)}
                aria-label={m.options_move_down()}
            >
                <ChevronDownIcon class="size-4" />
            </button>
        </div>
    </div>
{/snippet}
