<script lang="ts">
    import { resolve } from "$app/paths";
    import { m } from "$lib/paraglide/messages";
    import type { User } from "$lib/utils";
    import { Popover, Portal } from "@skeletonlabs/skeleton-svelte";
    import { Avatar } from "@skeletonlabs/skeleton-svelte";
    import { BadgeCheck } from "lucide-svelte";

    interface Props {
        user: User;
    }

    let { user }: Props = $props();

    // Turns John Doe into JD
    let fallbackname = $derived(
        (user.gh_fullname || user.gh_login_name)
            .split(" ")
            .map((word) => word.charAt(0))
            .join("")
            .toUpperCase(),
    );
</script>

<Popover>
    <Popover.Trigger class="inline-flex items-center gap-2">
        <Avatar class="size-10">
            <Avatar.Image src={user.gh_avatar_url} />
            <Avatar.Fallback>{fallbackname}</Avatar.Fallback>
        </Avatar>
        <div class="flex w-30">
            {user.gh_fullname || user.gh_login_name}
        </div>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card p-4 w-fit shadow-xl preset-filled-tertiary-100-900 border border-tertiary-200-800"
            >
                <Popover.Description>
                    <div class="flex flex-col gap-2 justify-center text-center">
                        {#if user.restricted_dicts}
                            <div class="flex flex-row gap-2 justify-start">
                                <span>{m.access()}</span>
                                <BadgeCheck />
                            </div>
                            <!-- {:else} -->
                            <!--     <span class="text-error-950-50" -->
                            <!--         >{m.no_access()}</span -->
                            <!--     > -->
                            <hr class="hr" />
                        {/if}
                        <span>
                            <a
                                href={resolve("/auth/logout")}
                                class="btn preset-filled-secondary-400-600 w-full h-fit"
                            >
                                {m.logout()}
                            </a>
                        </span>
                    </div>
                </Popover.Description>
            </Popover.Content>
        </Popover.Positioner>
    </Portal>
</Popover>
