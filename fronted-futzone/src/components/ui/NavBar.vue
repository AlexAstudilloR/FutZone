<template>
  <div :class="wrapperClass">
    <button
      v-for="tab in tabs"
      :key="tab.value"
      @click="$emit('update:modelValue', tab.value)"
      :class="[
        baseTabClass,
        modelValue === tab.value ? activeTabClass : inactiveTabClass
      ]"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: String, 
  tabs: {
    type: Array,
    required: true,
    default: () => [],
  },

  wrapperClass: {
    type: String,
    default: 'flex justify-center bg-[#14215D] rounded-lg  p-1 space-x-4',
  },
  baseTabClass: {
    type: String,
    default: 'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
  },
  activeTabClass: {
    type: String,
    default: 'text-white  underline underline-offset-8',
  },
  inactiveTabClass: {
    type: String,
    default: 'text-white/70 hover:text-white  hover:underline underline-offset-8 transition',
  },
})
</script>