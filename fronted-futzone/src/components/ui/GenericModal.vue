<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-xl font-semibold mb-4">{{ title }}</h2>
      <form @submit.prevent="handleSubmit">
        <div v-for="field in fields" :key="field.model" class="mt-4">
          <div v-if="field.type === 'file'">
            <label class="block text-sm font-medium mb-1">{{ field.label }}</label>
            <label class="flex items-center gap-2 px-3 py-2 bg-gray-100 border border-dashed border-gray-400 rounded cursor-pointer hover:bg-gray-200 text-sm w-fit">
              <font-awesome-icon :icon="['fas', 'arrow-up-from-bracket']" />
              <span>Subir una imagen</span>
              <input
                type="file"
                :accept="field.accept || 'image/*'"
                class="hidden"
                @change="(e) => handleFileChange(e, field.model)"
              />
            </label>
            <img
              :src="imagePreviewUrl(field.model)"
              alt="preview"
              class="mt-2 h-16 w-auto object-contain rounded border mx-auto"
            />
            <p v-if="errorFor(field.model)" class="text-red-600 text-sm mt-1">{{ errorFor(field.model) }}</p>
          </div>

          <div v-else-if="field.type === 'select'">
            <label class="block text-sm font-medium mb-1">{{ field.label }}</label>
            <select
              v-model="form[field.model]"
              class="w-full border rounded px-3 py-2"
              :required="field.required"
              @input="clearError(field.model)"
            >
              <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
            <p v-if="errorFor(field.model)" class="text-red-600 text-sm mt-1">{{ errorFor(field.model) }}</p>
          </div>

          <BaseInput
            v-else
            v-model="form[field.model]"
            :label="field.label"
            :placeholder="field.placeholder"
            :type="field.type"
            :required="field.required"
            @input="clearError(field.model)"
          />
          <p v-if="errorFor(field.model)" class="text-red-600 text-sm mt-1">{{ errorFor(field.model) }}</p>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button type="button" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 transition" @click="onCancel">
            Cancelar
          </button>
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
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
  title: String,
  fields: Array,
  initialData: Object,
  submitLabel: String,
  onSubmit: Function,
  errors: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['cancel', 'submit'])

const form = reactive({})
const previews = reactive({})

watch(
  () => props.initialData,
  (newVal) => {
    Object.keys(newVal || {}).forEach((key) => {
      form[key] = newVal[key]
    })

    props.fields.forEach((f) => {
      if (!(f.model in form)) form[f.model] = f.default ?? ''
    })
  },
  { immediate: true }
)

function clearError(field) {
  if (props.errors[field]) {
    props.errors[field] = ''
  }
}

function handleFileChange(e, model) {
  const file = e.target.files[0]
  form[model] = file

  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      previews[model] = reader.result
    }
    reader.readAsDataURL(file)
  } else {
    previews[model] = null
  }

  clearError(model)
}

function imagePreviewUrl(model) {
  return previews[model] || '/noimage.png'
}

function errorFor(field) {
  const err = props.errors?.[field]
  if (Array.isArray(err)) return err.join(', ')
  if (typeof err === 'object') return Object.values(err).flat().join(', ')
  return typeof err === 'string' ? err : null
}

function onCancel() {
  emit('cancel')
}

function handleSubmit() {
  const raw = {}
  for (const key in form) {
    raw[key] = form[key]
  }
  emit('submit', raw)
}
</script>
