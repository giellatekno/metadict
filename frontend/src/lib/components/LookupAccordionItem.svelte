<script>
    import { Accordion } from "@skeletonlabs/skeleton-svelte";
    import { ChevronDownIcon } from "@lucide/svelte";
    import { slide } from "svelte/transition";

    let { value, title, children } = $props();
</script>

<Accordion.Item {value}>
    <h4>
        <Accordion.ItemTrigger
            class="border-primary-500 flex items-center justify-between text-lg font-bold"
        >
            {title}
            <Accordion.ItemIndicator class="group">
                <ChevronDownIcon
                    class="h-5 w-5 transition group-data-[state=open]:rotate-180"
                />
            </Accordion.ItemIndicator>
        </Accordion.ItemTrigger>
        <hr class="hr border-primary-500 mx-auto w-49/50 border-t-2" />
    </h4>
    <Accordion.ItemContent class="pt-0">
        {#snippet element(attributes)}
            {#if !attributes.hidden}
                <div {...attributes} transition:slide={{ duration: 150 }}>
                    {@render children()}
                </div>
            {/if}
        {/snippet}
    </Accordion.ItemContent>
</Accordion.Item>
