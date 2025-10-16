<script lang="ts">
    import { locale } from "$lib/locale.js";
    import { Popover, Portal } from "@skeletonlabs/skeleton-svelte";
    import { langname } from "$lib/langname";
    import { LanguagesIcon } from "lucide-svelte";
    import { t } from "svelte-intl-precompile";

    const locales = ["nob", "eng", "sme"];
</script>

<Popover>
    <Popover.Trigger class="btn preset-filled-primary-500">
        <LanguagesIcon />
        <span>{langname($locale, $locale)}</span>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card p-4 w-fit shadow-xl preset-filled-surface-100-900 border border-surface-200-800"
            >
                <Popover.Description>
                    <ul class="w-full">
                        {#each locales as iso}
                            <li>
                                <button
                                    class="btn hover:preset-tonal"
                                    onclick={() => ($locale = iso)}
                                >
                                    {langname(iso, iso)}
                                </button>
                            </li>
                        {/each}
                    </ul>
                </Popover.Description>
                <!-- <Popover.Arrow -->
                <!--     style="--arrow-size: calc(var(--spacing) * 2); --arrow-background: var(--color-surface-100-900); --arrow-border: var()" -->
                <!-- > -->
                <!--     <Popover.ArrowTip /> -->
                <!-- </Popover.Arrow> -->
            </Popover.Content>
        </Popover.Positioner>
    </Portal>
</Popover>
