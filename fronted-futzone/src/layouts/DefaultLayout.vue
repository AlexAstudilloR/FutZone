<template>
  <div class="flex">

    <button
      @click="isOpen = !isOpen"
      :class="[
        'md:hidden fixed top-6 z-50 text-white transition-all duration-300',
        isOpen
          ? 'left-40'
          : 'left-4 bg-[#19296D] rounded-full flex items-center justify-center',
      ]"
      :style="isOpen ? '' : 'width: 40px; height: 40px;'"
    >
      <font-awesome-icon
        :icon="isOpen ? 'chevron-left' : 'bars'"
        class="text-lg"
      />
    </button>


    <Sidebar :isOpen="isOpen" />


    <div class="flex-1 min-h-screen p-4 md:ml-48">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from "../components/ui/Sidebar.vue";

const isOpen = ref(false);
</script>
