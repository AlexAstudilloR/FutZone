<script setup>
import { ref, computed } from 'vue'
defineOptions({ name: 'BaseInput' })

const props = defineProps({
  modelValue: String,
  type: {
    type: String,
    default: 'text',
  },
  label: String,
  placeholder: String,
  icon: {
    type: [String, Array, Object],
    default: null,
  },
  error: {
    type: String,
    default: '',
  },
  min: String,
  max: String,
  step: String,
  required: Boolean,
  disabled: Boolean,
})

const emit = defineEmits(['update:modelValue', 'input'])

const inputType = ref(props.type)
const togglePassword = () => {
  inputType.value = inputType.value === 'password' ? 'text' : 'password'
}

const hasIcon = computed(() => !!props.icon)
const hasToggle = computed(() => props.type === 'password')

const inputClasses = computed(() => [
  'w-full py-2 border rounded outline-none text-sm transition',
  hasIcon.value ? 'pl-10' : 'pl-3',
  hasToggle.value ? 'pr-10' : 'pr-3',
  props.error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-[#19296D]',
])
</script>

<template>
  <div class="space-y-1">
    <label v-if="label" class="block text-sm font-medium text-gray-700">
      {{ label }}
    </label>

    <p v-if="error" class="text-red-500 text-xs -mt-1">{{ error }}</p>

    <div class="relative">
      <div
        v-if="hasIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-500"
      >
        <font-awesome-icon :icon="icon" />
      </div>

      <input
        :type="inputType"
        :placeholder="placeholder"
        :value="modelValue"
        :min="min"
        :max="max"
        :step="step"
        :required="required"
        :disabled="disabled"
        @input="$emit('update:modelValue', $event.target.value); $emit('input')"
        :class="inputClasses"
      />

      <button
        v-if="hasToggle"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500"
        @click="togglePassword"
      >
        <font-awesome-icon :icon="inputType === 'password' ? 'fa-eye' : 'fa-eye-slash'" />
      </button>
    </div>
  </div>
</template>
