<template>

  <NavigationBar/>
  <div class="relative flex size-full min-h-screen flex-col items-center">
    <!-- <div class="h-24"></div> -->
    <RouterView/>
    <h1 class="absolute bottom-0 mb-4 text-center text-sm font-bold text-gray-400">
      Developed by
      <a href="https://github.com/DevJ2K" class="text-blue-500 hover:text-blue-700" target="_blank">DevJ2K</a>
      &
      <a href="https://github.com/lmoheyma" class="text-green-500 hover:text-green-700" target="_blank">lmoheyma</a>
      — Available on
  <a href="https://github.com/DevJ2K/app_gomoku" class="text-purple-500 hover:text-purple-700" target="_blank">GitHub</a>
    </h1>
  </div>
</template>


<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavigationBar from './components/navbar/NavigationBar.vue';
</script>
