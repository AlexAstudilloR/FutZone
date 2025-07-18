<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-lg relative">
      <button
        @click="closeModal"
        class="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-xl"
      >
        &times;
      </button>

      <h2 class="text-xl font-semibold text-center mb-4">
        Este es tu método de pago actual
      </h2>

      <div v-if="loading" class="text-center">
        <span>Cargando QR...</span>
      </div>

      <div v-else-if="paymentQR" class="flex justify-center">
        <img
          :src="paymentQR"
          alt="Código QR"
          class="w-48 h-48 object-contain border rounded"
        />
      </div>

      <div v-else class="text-center text-red-500">
        <p>No se encontró un método de pago.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useAuthStore } from "../../stores/authStore";

const props = defineProps({
  show: Boolean,
});
const emit = defineEmits(["close"]);

const authStore = useAuthStore();
const paymentQR = ref(null);
const loading = ref(false);

const fetchPaymentQR = async () => {
  loading.value = true;
  const { success, data } = await authStore.getPaymentMethod();
  if (success && data?.payment_qr) {
    paymentQR.value = data.payment_qr;
  } else {
    paymentQR.value = null;
  }
  loading.value = false;
};

const closeModal = () => {
  emit("close");
};

// Cada vez que el modal se abre, se trae el QR de nuevo
watch(
  () => props.show,
  (val) => {
    if (val) fetchPaymentQR();
  }
);
</script>
