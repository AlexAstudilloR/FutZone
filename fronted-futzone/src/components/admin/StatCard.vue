<template>
  <div
    :class="[
      'rounded-xl p-3 text-center shadow-sm w-full h-full min-h-[90px] max-h-[130px] flex flex-col justify-center',
      bgColor
    ]"
  >
    <div class="space-y-1">
      <h3 class="font-semibold text-sm leading-tight">{{ title }}</h3>
      <p :class="['text-xl font-bold', textColor]">{{ value }}</p>
    </div>
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