<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { supabase } from "../../lib/supabase";
import { useAuthStore } from "../../stores/authStore";
import BaseInput from "../../components/ui/BaseInput.vue";
import { toast } from "vue3-toastify";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const newPassword = ref("");
const message = ref("");
const isError = ref(false);
const isValidSession = ref(false);

onMounted(async () => {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (session) {
    isValidSession.value = true;
  } else {
    supabase.auth.onAuthStateChange((event, session) => {
      if (event === "PASSWORD_RECOVERY" && session) {
        isValidSession.value = true;
      }
    });
  }
});

const clearMessage = () => {
  message.value = "";
  isError.value = false;
};

// Validaciones de contraseña
const hasMinLength = computed(() => newPassword.value.length >= 6);
const hasUppercase = computed(() => /[A-Z]/.test(newPassword.value));
const hasNumber = computed(() => /\d/.test(newPassword.value));
const hasSpecialChar = computed(() => /[@*_\-!$#]/.test(newPassword.value));
const showRules =computed( ()=> newPassword.value.length >0)
const isPasswordValid = computed(
  () =>
    hasMinLength.value &&
    hasUppercase.value &&
    hasNumber.value &&
    hasSpecialChar.value
);

const handleReset = async () => {
  clearMessage();

  if (!isValidSession.value) {
    message.value =
      "Sesión de recuperación inválida. Solicita un nuevo enlace.";
    isError.value = true;
    return;
  }

  if (!isPasswordValid.value) {
    message.value = "Tu contraseña no cumple con los requisitos mínimos.";
    isError.value = true;
    return;
  }

  try {
    const success = await authStore.updatePassword(newPassword.value);

    if (success) {
      toast.success(
        "Contraseña cambiada correctamente, serás redirigido al login"
      );
      isError.value = false;
      setTimeout(() => router.push({ name: "Login" }), 1500);
    } else {
      message.value = authStore.error || "Error al actualizar la contraseña";
      isError.value = true;
    }
  } catch (error) {
    message.value = "Error inesperado al actualizar la contraseña";
    isError.value = true;
  }
};

const messageClass = computed(() =>
  isError.value
    ? "text-red-500 text-sm text-center"
    : "text-green-500 text-sm text-center"
);
</script>

<template>
  <div class="max-w-md mx-auto p-6 space-y-6">
    <h2 class="text-2xl font-bold text-center">Crear nueva contraseña</h2>

    <div v-if="!isValidSession" class="text-center">
      <p class="text-red-500 text-sm">
        Enlace de recuperación inválido o expirado.
      </p>
      <router-link
        to="/recover-password"
        class="text-blue-500 hover:underline text-sm"
      >
        Solicitar nuevo enlace
      </router-link>
    </div>

    <template v-else>
      <BaseInput
        v-model="newPassword"
        type="password"
        label="Nueva contraseña"
        placeholder="Mínimo 6 caracteres"
        icon="fa-lock"
        @input="clearMessage"
      />

      
     <div v-if="showRules" class="bg-amber-400/5 p-2 rounded-md transition-all duration-200">
  <ul class="text-sm space-y-1 text-gray-700">
    <li :class="hasMinLength ? 'text-green-600' : 'text-red-600'" class="flex items-center gap-2">
      <font-awesome-icon :icon="hasMinLength ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark'" />
      Mínimo 6 caracteres
    </li>
    <li :class="hasUppercase ? 'text-green-600' : 'text-red-600'" class="flex items-center gap-2">
      <font-awesome-icon :icon="hasUppercase ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark'" />
      Al menos una mayúscula
    </li>
    <li :class="hasNumber ? 'text-green-600' : 'text-red-600'" class="flex items-center gap-2">
      <font-awesome-icon :icon="hasNumber ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark'" />
      Al menos un número
    </li>
    <li :class="hasSpecialChar ? 'text-green-600' : 'text-red-600'" class="flex items-center gap-2">
      <font-awesome-icon :icon="hasSpecialChar ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark'" />
      Al menos un carácter especial (@, *, -, etc.)
    </li>
  </ul>
</div>

      <button
        @click="handleReset"
        :disabled="!isPasswordValid"
        class="w-full bg-[#19296D] text-white py-2 rounded hover:bg-blue-800 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        Cambiar contraseña
      </button>
    </template>

    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>
