<template>
  <div class="p-4 sm:p-6">
    <h1 class="text-2xl font-bold mb-4">Gestionar Canchas</h1>

    <div
      class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-2"
    >
      <BaseButton
        label="Añadir cancha"
        :icon="['fas', 'plus']"
        size="md"
        variant="primary"
        extraClass="hover:opacity-90 w-full sm:w-auto"
        @click.prevent="showCreate = true"
      />
      <LinkButton
        to="/admin"
        label="Volver a panel"
        :icon="['fas', 'arrow-left']"
        size="md"
        variant="none"
        color="inherit"
        extraClass="border border-[#19296D] text-[#19296D] hover:bg-[#19296D] hover:text-white transition-colors duration-200 w-full sm:w-auto text-center"
      />
    </div>

    <div v-if="loading" class="text-center py-10">Cargando...</div>
    <div v-else>
      <div class="overflow-x-auto">
        <DataTable :items="fields" :columns="columns">
          <template #actions="{ item }">
            <div
              class="flex flex-col sm:flex-row sm:justify-center sm:items-center gap-2"
            >
              <BaseButton
                label="Editar"
                :icon="['fas', 'pen-to-square']"
                size="sm"
                variant="light"
                textColor="blue"
                extraClass="border border-blue-600 px-3 py-1 hover:bg-blue-50 flex-1 sm:flex-none"
                @click.prevent="openEdit(item)"
              />
              <BaseButton
                label="Eliminar"
                :icon="['fas', 'trash']"
                size="sm"
                variant="light"
                textColor="inherit"
                extraClass="border border-red-600 text-red-600 px-3 py-1 hover:bg-red-50 flex-1 sm:flex-none"
                @click.prevent="confirmDelete(item.id)"
              />
            </div>
          </template>
        </DataTable>
      </div>

      <div class="mt-4 flex justify-center">
        <Pagination
          :currentPage="currentPage"
          :totalItems="totalCount"
          @update:page="onPageChange"
        />
      </div>
    </div>

    <GenericModal
      :isOpen="showCreate"
      title="Crear Cancha"
      :fields="fieldConfig"
      :initialData="{}"
      :submitLabel="'Crear'"
      :onSubmit="handleCreate"
      :errors="errors"
      @cancel="closeCreateModal"
    />

    <GenericModal
      :isOpen="showEdit"
      title="Editar Cancha"
      :fields="fieldConfig"
      :initialData="selectedField"
      :submitLabel="'Actualizar'"
      :onSubmit="handleUpdate"
      :errors="errors"
      @cancel="closeEditModal"
    />
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useFieldStore } from "../../stores/fieldStore";
import LinkButton from "../../components/ui/LinkButton.vue";
import Pagination from "../../components/ui/Pagination.vue";
import GenericModal from "../../components/ui/GenericModal.vue";
import DataTable from "../../components/ui/DataTable.vue";
import BaseButton from "../../components/ui/BaseButton.vue";

const store = useFieldStore();
const currentPage = ref(1);
const showCreate = ref(false);
const showEdit = ref(false);
const selectedField = ref({});
const errors = ref({});

const columns = [
  { key: "name", label: "Cancha" },
  { key: "field_type", label: "Tipo" },
  { key: "available", label: "Estado" },
  { key: "price", label: "Precio" },
];

const fieldConfig = [
  {
    model: "name",
    label: "Nombre",
    type: "text",
    placeholder: "Nombre de la cancha",
    required: true,
  },
  {
    model: "field_type",
    label: "Tipo",
    type: "text",
    placeholder: "Futbol 7, Indoor...",
    required: true,
  },
  {
    model: "available",
    label: "Estado",
    type: "select",
    options: [
      { value: true, label: "Disponible" },
      { value: false, label: "Cerrada" },
    ],
    required: true,
  },
  {
    model: "price",
    label: "Precio",
    type: "number",
    placeholder: "0.00",
    required: true,
  },
  {
    model: "image",
    label: "Imagen",
    type: "file",
    required: false,
    accept: "image/png, image/jpeg",
  },
];

const loading = computed(() => store.loading);
const fields = computed(() => store.fields);
const totalCount = computed(() => store.fields.length);
function closeCreateModal() {
  showCreate.value = false;
  errors.value = {};
}

function closeEditModal() {
  showEdit.value = false;
  errors.value = {};
}
async function loadPage(page = 1) {
  currentPage.value = page;
  await store.fetchFields();
}

function onPageChange(page) {
  loadPage(page);
}

function openEdit(field) {
  selectedField.value = { ...field };
  errors.value = {};
  showEdit.value = true;
}

function confirmDelete(id) {
  if (confirm("¿Seguro que quieres eliminar esta cancha?")) {
    store.deleteField(id);
  }
}

async function handleCreate(formValues) {
  console.log("Llamando a store.createField con:", formValues)

  const formData = new FormData();
  for (const key in formValues) {
    if (formValues[key] !== undefined && formValues[key] !== null) {
      formData.append(key, formValues[key]);
    }
  }

  // Debug: ver qué se está enviando
  for (const [key, val] of formData.entries()) {
    console.log(`${key}:`, val);
  }

  const { success, error } = await store.createField(formData);

  if (success) {
    showCreate.value = false;
    errors.value = {};
    loadPage(currentPage.value);
  } else {
    console.log("Error devuelto del store:", error);
    errors.value = { ...error };
  }
}

async function handleUpdate(data) {
  const formData = new FormData();
  for (const key in data) {
    if (data[key] !== undefined && data[key] !== null) {
      formData.append(key, data[key]);
    }
  }

  const { success, error } = await store.updateField(
    selectedField.value.id,
    formData
  );
  if (success) {
    showEdit.value = false;
    errors.value = {};
    loadPage(currentPage.value);
  } else {
    errors.value = { ...error };
  }
}
onMounted(() => loadPage());
</script>
