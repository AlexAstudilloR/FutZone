<template>
  <section class="p-4 bg-white shadow rounded-lg mb-8">

    <!-- Encabezado -->
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold">{{ title }}</h2>
      <BaseButton @click="openModal" :icon="['fas','plus']">
        {{ `Agregar ${singular}` }}
      </BaseButton>
    </div>

    <!-- Tabla -->
    <DataTable
      :columns="columns"
      :items="items"
      :loading="loading"
    >
      <template #actions="{ item }">
        <div class="flex gap-2 justify-center">
          <BaseButton
            label="Editar"
            :icon="['fas','pen-to-square']"
            size="sm"
            variant="light"
            textColor="inherit"
            extraClass="border border-blue-600 text-blue-600 px-3 py-1 hover:bg-blue-50"
            @click.prevent="onEdit(item)"
          />
          <BaseButton
            label="Eliminar"
            :icon="['fas','trash']"
            size="sm"
            variant="light"
            textColor="inherit"
            extraClass="border border-red-600 text-red-600 px-3 py-1 hover:bg-red-50"
            @click.prevent="onDelete(item)"
          />
        </div>
      </template>
    </DataTable>

    <GenericModal
      :isOpen="isModalOpen"
      :title="isEditing 
        ? `Editar ${singular}` 
        : `Nuevo ${singular}`"
      :fields="modalFields"
      :initialData="form"
      :submitLabel="isEditing 
        ? 'Guardar cambios' 
        : 'Crear'"
      :onSubmit="handleModalSubmit"
      @cancel="resetForm"
    />
  </section>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import BaseButton from '../ui/BaseButton.vue'
import DataTable  from '../ui/DataTable.vue'
import GenericModal from '../ui/GenericModal.vue'
import Swal from 'sweetalert2'

const props = defineProps({
  title:      { type: String, required: true },
  singular:   { type: String, required: true },
  items:      { type: Array,  required: true },
  fields:     { type: Array,  required: true },
  columns:    { type: Array,  required: true },
  fetchFn:    { type: Function, required: true },
  createFn:   { type: Function, required: true },
  updateFn:   { type: Function, required: true },
  deleteFn:   { type: Function, required: true },
})

const isModalOpen = ref(false)
const isEditing   = ref(false)
const loading     = ref(false)
const form        = ref({})

const modalFields = computed(() =>
  props.fields.map(f => ({
    model:       f.prop,
    label:       f.label,
    type:        f.options ? 'select' : (f.type || 'text'),
    options:     f.options || null,
    placeholder: f.placeholder || '',
  }))
)

function resetForm() {
  isModalOpen.value = false
  isEditing.value   = false
  form.value = props.fields.reduce((acc, f) => {
    acc[f.prop] = f.type === 'checkbox' ? false : ''
    return acc
  }, {})
}

onMounted(async () => {
  loading.value = true
  await props.fetchFn()
  loading.value = false
})

watch(() => props.items, () => {
  if (isModalOpen.value) resetForm()
})

function openModal() {
  resetForm()
  isModalOpen.value = true
}

function onEdit(item) {
  form.value = { ...item }
  isEditing.value = true
  isModalOpen.value = true
}

async function onDelete(item) {
  const { isConfirmed } = await Swal.fire({
    title: `¿Eliminar ${props.singular}?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
    buttonsStyling: false,
    customClass: {
      popup: 'rounded-lg p-6',
      confirmButton: 'border border-red-600 text-red-600 bg-white px-4 py-2 rounded hover:bg-red-600 hover:text-white transition-colors duration-200 mr-2',
      cancelButton:  'border border-blue-600 text-blue-600 bg-white px-4 py-2 rounded hover:bg-blue-600 hover:text-white transition-colors duration-200'
    }
  })
  if (isConfirmed) {
    await props.deleteFn(item.id)
    await props.fetchFn()
  }
}

async function handleModalSubmit(data) {
  if (isEditing.value) {
    await props.updateFn(data.id, data)
  } else {
    await props.createFn(data)
  }
  await props.fetchFn()
  resetForm()
}
</script>
