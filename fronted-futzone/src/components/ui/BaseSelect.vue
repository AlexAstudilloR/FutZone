<template>
  <div class="flex flex-col">
    <label v-if="label" class="block text-sm font-medium mb-1 text-gray-700">{{ label }}</label>
    <select
      v-model="internalValue"
      :disabled="disabled"
      :class="[
        'block w-full border rounded-md shadow-sm focus:ring focus:ring-opacity-50',
        sizeClass,
        disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
        extraClass
      ]"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option
        v-for="opt in options"
        :key="opt.value"
        :value="opt.value"
      >
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { computed, toRefs, ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  extraClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])
const { modelValue, size } = toRefs(props)

const internalValue = ref(modelValue.value)

watch(modelValue, val => {
  internalValue.value = val
})

watch(internalValue, val => {
  emit('update:modelValue', val)
})

const sizeClasses = {
  sm: 'px-2 py-1 text-sm',
  md: 'px-3 py-2 text-base',
  lg: 'px-4 py-3 text-lg'
}

const sizeClass = computed(() => sizeClasses[size.value] || sizeClasses.md)
</script>
