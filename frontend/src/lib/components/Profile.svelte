<script lang="ts">
    import { resolve } from "$app/paths";
    import { m } from "$lib/paraglide/messages";
    import type { UserType } from "$lib/schemas";
    import { Popover, Portal } from "@skeletonlabs/skeleton-svelte";
    import { Avatar } from "@skeletonlabs/skeleton-svelte";
    import { BadgeCheck } from "@lucide/svelte";

    interface Props {
        user: UserType;
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
    <Popover.Trigger class="mx-3 inline-flex items-center hover:underline">
        <Avatar class="size-8 sm:size-10">
            <Avatar.Image src={user.gh_avatar_url} />
            <Avatar.Fallback>{avatar_fallbackname}</Avatar.Fallback>
        </Avatar>
        <span class="hidden text-sm sm:flex sm:w-30 xl:text-base">
            {user.gh_fullname || user.gh_login_name}
        </span>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card preset-filled-primary-50-950 w-fit border p-4 shadow-xl"
            >
                <Popover.Description>
                    <div class="flex flex-col justify-center gap-2 text-center">
                        <div class="font-bold sm:hidden">
                            {user.gh_fullname || user.gh_login_name}
                        </div>
                        <hr class="hr sm:hidden" />
                        {#if user.restricted_dicts}
                            <div class="flex flex-row justify-start gap-2">
                                <span>{m.gt_employee()}</span>
                                <BadgeCheck />
                            </div>
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
                <Popover.Arrow
                    class="[--arrow-background:var(--color-primary-50-950)] [--arrow-size:--spacing(2)]"
                >
                    <Popover.ArrowTip />
                </Popover.Arrow>
            </Popover.Content>
        </Popover.Positioner>
    </Portal>
</Popover>
