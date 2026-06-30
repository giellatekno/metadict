<script lang="ts">
    import { m } from "$lib/paraglide/messages";
    import type { MessageFunction } from "@inlang/paraglide-js";
    import { XIcon } from "@lucide/svelte";
    import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
    import type { Snippet } from "svelte";

    interface Props {
        buttonContent: Snippet;
        dialogTitle: MessageFunction;
        dialogContent: Snippet;
    }
    let { buttonContent, dialogTitle, dialogContent }: Props = $props();

    const animation =
        "transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0";
</script>

<div class="flex w-fit flex-col">
    <Dialog>
        <Dialog.Trigger
            class="preset-filled-surface-200-800 hover:preset-filled-surface-100-900 border-surface-200-800 flex items-center justify-between gap-4 rounded-lg border px-4 py-1 text-sm xl:text-base"
        >
            {@render buttonContent()}
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
                            {dialogTitle()}
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
                        {@render dialogContent()}
                    </Dialog.Description>
                </Dialog.Content>
            </Dialog.Positioner>
        </Portal>
    </Dialog>
</div>
