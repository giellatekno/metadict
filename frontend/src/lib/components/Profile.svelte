<script lang="ts">
    import { resolve } from "$app/paths";
    import { t } from "svelte-intl-precompile";
    import { Popover, Portal } from "@skeletonlabs/skeleton-svelte";
    import { Avatar } from "@skeletonlabs/skeleton-svelte";

    interface Props {
        user: {
            gh_avatar_url: string;
            gh_fullname: string;
            restricted_dicts: boolean;
        };
    }

    let { user }: Props = $props();

    // Turns John Doe into JD
    let fallbackname = user.gh_fullname
        .split(" ")
        .map((word) => word.charAt(0))
        .join("")
        .toUpperCase();
</script>

<Popover>
    <Popover.Trigger class="inline-flex items-center gap-2">
        <Avatar class="w-10">
            <Avatar.Image src={user.gh_avatar_url} class="rounded-full" />
            <Avatar.Fallback>{fallbackname}</Avatar.Fallback>
        </Avatar>
        <div>{user.gh_fullname}</div>
    </Popover.Trigger>
    <Portal>
        <Popover.Positioner>
            <Popover.Content
                class="card p-4 w-44 shadow-xl preset-filled-surface-100-900 border border-surface-200-800"
            >
                <Popover.Description>
                    <div class="flex flex-col gap-2 justify-center text-center">
                        {#if user.restricted_dicts}
                            <span class="text-success-800">{$t("access")}</span>
                        {:else}
                            <span class="text-error-800">{$t("no-access")}</span
                            >
                        {/if}
                        <span>
                            <a
                                href={resolve("/auth/logout")}
                                class="btn preset-tonal-error w-fit h-fit"
                            >
                                {$t("logout")}
                            </a>
                        </span>
                    </div>
                </Popover.Description>
                <!-- <Popover.Arrow -->
                <!--     style="--arrow-size: calc(var(--spacing) * 2); --arrow-background: var(--color-surface-100-900);" -->
                <!-- > -->
                <!--     <Popover.ArrowTip /> -->
                <!-- </Popover.Arrow> -->
            </Popover.Content>
        </Popover.Positioner>
    </Portal>
</Popover>
