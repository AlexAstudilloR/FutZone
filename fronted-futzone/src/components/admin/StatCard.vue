<template>
  <div :class="['rounded-lg p-4 shadow flex flex-col gap-2', bgColor]">
    <div class="flex items-center justify-center gap-2">
      <font-awesome-icon :icon="['fas', icon]" :class="[textColor, 'text-md ']" />
      <span class="text-md font-medium text-gray-700">{{ title }}</span>
    </div>
    <p :class="['text-2xl text-center font-bold', textColor]">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String,       
  bgColor: String,    
  textColor: String    
});
</script>