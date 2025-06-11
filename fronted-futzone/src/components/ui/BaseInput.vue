<script setup>
import { ref } from 'vue'
defineOptions({ name: 'BaseInput' })

const props = defineProps({
  modelValue: String,
  type: {
    type: String,
    default: 'text',
  },
  label: String,
  placeholder: String,
  icon: String,
})

const emit = defineEmits(['update:modelValue'])

const inputType = ref(props.type)
const togglePassword = () => {
  inputType.value = inputType.value === 'password' ? 'text' : 'password'
}
</script>

<template>
  <div class="space-y-1">
    <label v-if="label" class="block text-sm font-medium text-gray-700">
      {{ label }}
    </label>

    <div class="relative">
      <!-- Ícono izquierdo -->
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-500">
        <font-awesome-icon :icon="icon" />
      </div>

      <!-- Input -->
      <input
        :type="inputType"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="w-full pl-10 pr-10 py-2 border rounded outline-[#19296D] text-sm"
      />

      <!-- Toggle mostrar contraseña -->
      <button
        v-if="type === 'password'"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500"
        @click="togglePassword"
      >
        <font-awesome-icon :icon="inputType === 'password' ? 'fa-eye' : 'fa-eye-slash'" />
      </button>
    </div>
  </div>
</template>
