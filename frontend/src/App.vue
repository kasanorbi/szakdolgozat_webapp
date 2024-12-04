<template>
    <div>
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
            rel="stylesheet">
        <div class="flex items-center justify-center">
            <div class="navbar bg-primary text-primary-content max-w-screen-xl rounded-full mt-[3vh]">
                <div class="flex-1">
                    <a class="btn rounded-full" href="/">
                        <span class="material-symbols-outlined">
                            home
                        </span>
                    </a>
                </div>
                <div class="flex-none gap-3">
                    <a class="btn text-xl rounded-full" href="/bills">
                        Számlák
                    </a>
                    <a class="btn text-xl rounded-full" href="/storage">
                        Készlet
                    </a>
                    <a class="btn text-xl rounded-full" href="/customers">
                        Új számla
                    </a>
                </div>
            </div>
        </div>
        <RouterView />
    </div>
</template>
<script setup>
import { RouterView } from 'vue-router';
</script>
