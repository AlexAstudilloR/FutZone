<template>
  <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="sm:max-w-md w-full bg-white rounded-lg shadow-md p-6 relative">
      <!-- Botón cerrar -->
      <button
        @click="handleCancel"
        class="absolute top-2 right-2 text-gray-600 hover:text-gray-900"
        aria-label="Cerrar modal"
      >
        &times;
      </button>

      <h2 class="text-lg font-semibold text-gray-900 mb-4">
        Añade un QR para recibir el pago de tus reservas
      </h2>

      <p class="text-sm text-gray-600 mb-3">El QR puede ser de:</p>

      <div class="flex justify-center gap-6 mb-4">
        <div class="flex flex-col items-center">
          <img src="/deunalogo.png" alt="Logo DeUna" class="w-16 h-16 object-contain rounded-lg border" />
          <span class="text-xs text-gray-500 mt-1">DeUna</span>
        </div>
        <div class="flex flex-col items-center">
          <img src="/peigologo.avif" alt="Logo Peigo" class="w-16 h-16 object-contain rounded-lg border" />
          <span class="text-xs text-gray-500 mt-1">Peigo</span>
        </div>
      </div>

      <div class="space-y-2 mb-4">
        <label for="qr-upload" class="text-sm font-medium text-gray-700">Imagen QR</label>

        <div v-if="!selectedImage" class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
          <font-awesome-icon icon="arrow-up-from-bracket" class="text-gray-400 text-4xl mb-4" />
          <label
            for="qr-upload"
            class="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm text-gray-700 bg-white hover:bg-gray-50"
          >
            Seleccionar imagen
          </label>
          <input
            id="qr-upload"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageChange"
          />
          <p class="text-xs text-gray-500 mt-2">PNG, JPG, GIF hasta 10MB</p>
        </div>

        <div v-else class="relative border border-gray-300 rounded-lg p-4">
          <button
            @click="handleRemoveImage"
            class="absolute -top-2 -right-2 h-6 w-6 rounded-full bg-white border hover:bg-gray-50 flex items-center justify-center"
          >
            <font-awesome-icon icon="xmark-circle" class="text-sm text-gray-600" />
          </button>
          <img :src="selectedImage" alt="QR Preview" class="w-48 h-48 object-contain mx-auto" />
          <p class="text-sm text-gray-600 text-center mt-2">Vista previa del QR</p>
        </div>
      </div>

      <div class="flex justify-end gap-2">
        <button
          @click="handleCancel"
          class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-100"
        >
          Cancelar
        </button>
        <button
          @click="handleSave"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          :disabled="!selectedFile"
        >
          Guardar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useAuthStore } from "../../stores/authStore";
const authStore = useAuthStore();

const props = defineProps({
  isOpen: Boolean,
});
const emit = defineEmits(["close"]);

const selectedFile = ref(null);
const selectedImage = ref(null);

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    selectedFile.value = null;
    selectedImage.value = null;
    // reset input if needed
    const input = document.getElementById("qr-upload");
    if (input) input.value = "";
  }
});

const handleImageChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    selectedFile.value = file;
    const reader = new FileReader();
    reader.onload = (event) => {
      selectedImage.value = event.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleRemoveImage = () => {
  selectedFile.value = null;
  selectedImage.value = null;
  const input = document.getElementById("qr-upload");
  if (input) input.value = "";
};

const handleCancel = () => {
  handleRemoveImage();
  emit("close");
};

const handleSave = async () => {
  if (!selectedFile.value) return;

  const formData = new FormData();
  formData.append("payment_qr", selectedFile.value);

  const res = await authStore.uploadPaymentQR(formData);

  if (res.success) {
    // Aquí va tu toast o notificación si quieres
    handleCancel();
  } else {
    console.error("Error al subir QR:", res.error);
  }
};
</script>
