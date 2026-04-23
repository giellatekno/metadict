<script lang="ts">
    import { browser } from "$app/environment";
    import { m } from "$lib/paraglide/messages.js";
    import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
    import { KeyboardIcon, XIcon } from "lucide-svelte";

    const isMac = $derived.by(() => {
        const ua = browser ? window.navigator.userAgent : "";
        return ua ? ua.includes("Mac") : false;
    });

    const shortcuts = [
        { keys: ["ctrl", "K"], desc: m.kbd_shortcuts_searchfield_focus },
        { keys: ["↵"], desc: m.kbd_shortcuts_searchfield_enter },
        { keys: ["↑", "↓"], desc: m.kbd_shortcuts_searchresults_navigate },
        { keys: ["ctrl", "↵"], desc: m.kbd_shortcuts_searchresults_enter },
    ];

    // animation for search settings dialig
    const animation =
        "transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0";
</script>

<div class="flex w-fit flex-col">
    <Dialog>
        <Dialog.Trigger
            class="preset-filled-surface-200-800 hover:preset-filled-surface-100-900 border-surface-200-800 flex items-center justify-between gap-4 rounded-lg border px-4 py-1"
        >
            <KeyboardIcon class="size-5" />
            <span class="font-bold">{m.kbd_shortcuts()}</span>
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
                            {m.kbd_shortcuts()}
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
                        <div class="grid grid-cols-[auto_1fr] gap-6 text-lg">
                            {#each shortcuts as { keys, desc }}
                                <div class="flex items-center gap-1">
                                    {#each keys as key}
                                        {#if key === "ctrl"}
                                            <kbd
                                                class="kbd preset-filled-surface-200-800 text-lg"
                                            >
                                                {#if isMac}
                                                    ⌘
                                                {:else}
                                                    Ctrl
                                                {/if}
                                            </kbd>
                                            +
                                        {:else}
                                            <kbd
                                                class="kbd preset-filled-surface-200-800 text-lg"
                                            >
                                                {key}
                                            </kbd>
                                        {/if}
                                    {/each}
                                </div>
                                <span>{desc()}</span>
                            {/each}
                        </div>
                    </Dialog.Description>
                </Dialog.Content>
            </Dialog.Positioner>
        </Portal>
    </Dialog>
</div>
