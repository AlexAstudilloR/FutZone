<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-xl font-semibold mb-4">{{ title }}</h2>
      <form @submit.prevent="handleSubmit">
        <div v-for="field in fields" :key="field.model" class="mt-4">
          <BaseInput
            v-if="field.type !== 'select'"
            v-model="form[field.model]"
            :label="field.label"
            :placeholder="field.placeholder"
            :type="field.type"
            :required="field.required"
          />

          <div v-else>
            <label class="block text-sm font-medium mb-1">{{ field.label }}</label>
            <select
              v-model="form[field.model]"
              class="w-full border rounded px-3 py-2"
              :required="field.required"
            >
              <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button
            type="button"
            class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 transition"
            @click="onCancel"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            {{ submitLabel }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import BaseInput from './BaseInput.vue'

const props = defineProps({
  isOpen: Boolean,
  title: {
    type: String,
    required: true
  },
  fields: {
    type: Array,
    default: () => []
  },
  initialData: {
    type: Object,
    default: () => ({})
  },
  submitLabel: {
    type: String,
    default: 'Enviar'
  },
  onSubmit: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['cancel'])

const form = reactive({})

watch(
  () => props.initialData,
  (newVal) => {
    Object.keys(newVal).forEach(key => {
      form[key] = newVal[key]
    })
    // ensure all fields have a default
    props.fields.forEach(f => {
      if (!(f.model in form)) form[f.model] = f.default ?? ''
    })
  },
  { immediate: true }
)

function onCancel() {
  emit('cancel')
}

function handleSubmit() {
  props.onSubmit({ ...form })
}
</script>
