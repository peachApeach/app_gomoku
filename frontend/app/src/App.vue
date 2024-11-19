<template>

  <NavigationBar/>
  <div class="relative flex size-full min-h-screen flex-col items-center font-Poppins">
    <!-- <div class="h-24"></div> -->
    <RouterView/>
  </div>
</template>


<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavigationBar from './components/navbar/NavigationBar.vue';
</script>
