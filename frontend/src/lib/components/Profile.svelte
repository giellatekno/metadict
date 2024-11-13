<script lang="ts">
    import { base } from "$app/paths";
    import { t } from "svelte-intl-precompile";
    import type { PopupSettings } from "@skeletonlabs/skeleton";
    import { Avatar, popup } from "@skeletonlabs/skeleton";
    
    export let user: {
        gh_avatar_url: string;
        gh_fullname: string;
        restricted_dicts: boolean;
    };

    const profilePopupClick: PopupSettings = {
        event: "click",
        target: "profilePopupClick",
        placement: "bottom"
    };

</script>

<button class="inline-flex items-center gap-2" use:popup={profilePopupClick}>
        <Avatar src="{user.gh_avatar_url}" rounded="rounded-full" width="w-10"/>
        <div>{user.gh_fullname}</div>
</button>

<div class="card p-4 w-30 variant-filled-tertiary shadow-xl" data-popup="profilePopupClick">
    <div class="flex flex-col gap-2 justify-center text-center">
        {#if user.restricted_dicts}
        <span>{$t("access")}</span>
        {:else}
        <span>{$t("no-access")}</span>
        {/if}
        
        <a href="{base}/auth/logout" class="btn variant-ghost-error ">
            {$t("logout")}
        </a>
    </div>
        
    <div class="arrow variant-filled-tertiary" />
</div>
