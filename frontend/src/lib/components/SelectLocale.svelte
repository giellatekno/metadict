<script lang="ts">
    import { locale } from "$lib/locale.js";
    import { Popover, Portal } from "@skeletonlabs/skeleton-svelte";
    import { langname } from "$lib/langname";
    import { LanguagesIcon } from "lucide-svelte";

    const locales = ["nob", "eng", "sme"];
</script>

<Popover>
    <Popover.Trigger class="btn preset-filled-primary-400-600">
        <LanguagesIcon />
        <span>{langname($locale, $locale)}</span>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card p-4 w-fit shadow-xl preset-filled-tertiary-100-900 border border-tertiary-200-800"
            >
                <Popover.Description>
                    <ul class="w-full">
                        {#each locales as iso}
                            <li>
                                <button
                                    class="btn hover:preset-filled-tertiary-400-600 w-full justify-start"
                                    onclick={() => ($locale = iso)}
                                >
                                    {langname(iso, iso)}
                                </button>
                            </li>
                        {/each}
                    </ul>
                </Popover.Description>
            </Popover.Content>
        </Popover.Positioner>
    </Portal>
</Popover>
