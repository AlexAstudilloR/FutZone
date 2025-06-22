<script setup>
defineOptions({ name: 'BaseCheckbox' })

const props = defineProps({
  modelValue: Boolean,
  label: String,
  disabled: Boolean,
  error: String
})

const emit = defineEmits(['update:modelValue'])

function toggle() {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
  }
}
</script>

<template>
  <div class="flex items-center space-x-2">
    <input
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      @change="toggle"
      class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
    />
    <label class="text-sm font-medium text-gray-700" @click="toggle">
      {{ label }}
    </label>
    <p v-if="error" class="text-red-500 text-xs ml-2">{{ error }}</p>
  </div>
</template>
