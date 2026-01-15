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

    let avatar_fallbackname = $derived(
        capitalize_name(user.gh_fullname || user.gh_login_name),
    );

    // Turns John Doe into JD
    function capitalize_name(name: string): string {
        return name
            .split(" ")
            .map((word) => word.charAt(0))
            .join("")
            .toUpperCase();
    }
</script>

<Popover>
    <Popover.Trigger class="inline-flex items-center gap-2">
        <Avatar class="size-10">
            <Avatar.Image src={user.gh_avatar_url} />
            <Avatar.Fallback>{avatar_fallbackname}</Avatar.Fallback>
        </Avatar>
        <div class="flex w-30">{user.gh_fullname || user.gh_login_name}</div>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card preset-filled-tertiary-100-900 border-tertiary-200-800 w-fit border p-4 shadow-xl"
            >
                <Popover.Description>
                    <div class="flex flex-col justify-center gap-2 text-center">
                        {#if user.restricted_dicts}
                            <div class="flex flex-row justify-start gap-2">
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
                                class="btn preset-filled-secondary-400-600 h-fit w-full"
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
