<template>
  <div class="p-6 space-y-8">
    <!-- Perfil del admin -->
    <section
      class="bg-white shadow rounded-lg p-6 flex items-center gap-6 justify-between"
    >
      <div class="flex items-center gap-6">
        <div class="w-24 h-24 rounded-full overflow-hidden">
          <img
            src="/profile.jpeg"
            alt="Foto de perfil"
            class="w-full h-full object-cover rounded-full"
          />
        </div>
        <div class="flex flex-col">
          <h2 class="text-xl font-bold">{{ profile.full_name }}</h2>
          <p class="text-gray-600"><b>+593</b> {{ profile.cell_phone }}</p>
        </div>
      </div>

      <div class="flex gap-2">
        <!-- Ver QR -->
        <BaseButton variant="secondary" @click="showQrModal = true">
          Ver QR de pago
        </BaseButton>

        <!-- Subir QR -->
        <BaseButton variant="primary" @click="uploadQrModal = true">
          Subir QR de pago
        </BaseButton>
      </div>
    </section>

    <!-- Gestión de usuarios -->
    <section>
      <div class="flex gap-2 items-center mb-4 justify-between">
        <div class="flex gap-2 items-center">
          <h3 class="text-lg font-semibold">Gestión de Usuarios</h3>
          <font-awesome-icon icon="users" />
        </div>
        <BaseButton variant="primary" @click="openModal">
          + Crear usuario
        </BaseButton>
      </div>

      <div v-if="profileStore.loading" class="text-gray-500">
        Cargando usuarios...
      </div>
      <div v-else-if="!safeProfiles.length" class="text-gray-500">
        No hay usuarios aún.
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="user in safeProfiles"
          :key="user.id"
          class="bg-white shadow rounded-md p-4 flex items-center justify-between"
        >
          <div>
            <p class="font-semibold text-gray-800">{{ user.full_name }}</p>
            <p class="text-sm text-gray-600">
              📞 {{ user.cell_phone || "Sin número" }}
            </p>
          </div>
          <span
            class="text-sm px-2 py-1 rounded font-medium"
            :class="user.is_admin ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
          >
            {{ user.is_admin ? "Admin" : "Usuario" }}
          </span>
        </div>
      </div>
    </section>

    <!-- Modal para crear usuario -->
    <GenericModal
      :isOpen="isModalOpen"
      title="Nuevo Usuario"
      :fields="modalFields"
      submitLabel="Crear"
      :initialData="{}"
      :errors="formErrors"
      @submit="handleCreate"
      @cancel="isModalOpen = false"
    />

    <!-- Modal para subir QR -->
    <PaymentModal :isOpen="uploadQrModal" @close="handleUploadQrClose" />

    <!-- Modal para ver QR -->
    <PaymentQR :show="showQrModal" @close="showQrModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useProfileStore } from "../../stores/profileStore";
import { getMyProfile } from "../../services/authService";

import BaseButton from "../../components/ui/BaseButton.vue";
import GenericModal from "../../components/ui/GenericModal.vue";
import PaymentModal from "../../components/admin/PaymentModal.vue"; // 👈 ya estaba
import PaymentQR from "../../components/admin/PaymentQR.vue"; // 👈 nuevo

const profile = ref({});
const isModalOpen = ref(false);
const formErrors = ref({});
const uploadQrModal = ref(false); // para PaymentModal (subir)
const showQrModal = ref(false);   // para PaymentQR (ver)

const profileStore = useProfileStore();

const modalFields = [
  {
    label: "Nombre completo",
    model: "full_name",
    type: "text",
    placeholder: "Ej. Juan Pérez",
    required: true,
  },
  {
    label: "Celular",
    model: "cell_phone",
    type: "text",
    placeholder: "09xxxxxxxx",
    required: false,
  },
  {
    label: "Correo electrónico",
    model: "email",
    type: "email",
    placeholder: "usuario@email.com",
    required: true,
  },
  {
    label: "Contraseña",
    model: "password",
    type: "password",
    placeholder: "Mínimo 6 caracteres",
    required: true,
  },
  {
    label: "Tipo de cuenta",
    model: "is_admin",
    type: "select",
    required: true,
    options: [
      { value: true, label: "Administrador" },
      { value: false, label: "Usuario" },
    ],
  },
];

const fetchProfile = async () => {
  const { data } = await getMyProfile();
  profile.value = data;
};

const safeProfiles = computed(() => {
  const list = profileStore.profiles;
  if (list?.results && Array.isArray(list.results)) {
    return list.results.filter((u) => u && u.id);
  }
  if (Array.isArray(list)) {
    return list.filter((u) => u && u.id);
  }
  return [];
});

const openModal = () => {
  isModalOpen.value = true;
  formErrors.value = {};
};

const handleCreate = async (data) => {
  formErrors.value = {};
  try {
    await profileStore.createUserAndProfile(data);
    isModalOpen.value = false;
  } catch (err) {
    formErrors.value = err;
  }
};

const handleUploadQrClose = async () => {
  uploadQrModal.value = false;
  await fetchProfile(); // actualiza datos si se sube un nuevo QR
};

onMounted(async () => {
  await fetchProfile();
  await profileStore.fetchProfiles();
});
</script>
