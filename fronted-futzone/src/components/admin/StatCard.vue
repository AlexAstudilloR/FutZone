<template>
  <div :class="['rounded-xl p-4 text-center shadow-sm w-full', bgColor]">
    <h3 class="font-semibold text-sm">{{ title }}</h3>
    <p :class="['text-2xl font-bold', textColor]">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  bgColor: String,
  textColor: {
    type: String,
    default: 'text-white',
  },
})
</script>
