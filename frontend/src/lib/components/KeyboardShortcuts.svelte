<script lang="ts">
    import { browser } from "$app/environment";
    import { m } from "$lib/paraglide/messages.js";
    import { KeyboardIcon } from "@lucide/svelte";
    import DialogButton from "./DialogButton.svelte";

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
</script>

<DialogButton dialogTitle={m.kbd_shortcuts}>
    {#snippet buttonContent()}
        <KeyboardIcon class="size-5" />
        <span class="font-bold">{m.kbd_shortcuts()}</span>
    {/snippet}
    {#snippet dialogContent()}
        <div class="grid grid-cols-[auto_1fr] gap-6 text-lg">
            {#each shortcuts as { keys, desc }}
                <div class="flex items-center gap-1">
                    {#each keys as key}
                        {#if key === "ctrl"}
                            <kbd class="kbd preset-filled-surface-200-800 text-lg">
                                {#if isMac}
                                    ⌘
                                {:else}
                                    Ctrl
                                {/if}
                            </kbd>
                            +
                        {:else}
                            <kbd class="kbd preset-filled-surface-200-800 text-lg">
                                {key}
                            </kbd>
                        {/if}
                    {/each}
                </div>
                <span>{desc()}</span>
            {/each}
        </div>
    {/snippet}
</DialogButton>
