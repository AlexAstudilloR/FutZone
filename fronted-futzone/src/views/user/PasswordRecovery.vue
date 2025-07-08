<template>
  <div class="max-w-md mx-auto p-6 space-y-4">
    <h2 class="text-2xl font-bold text-center">Recuperar contraseña</h2>

    <BaseInput
      v-model="email"
      type="email"
      label="Correo electrónico"
      placeholder="tu@correo.com"
      icon="fa-envelope"
      @input="clearMessage"
    />

    <button
      @click="handleRecovery"
      class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
    >
      Enviar enlace de recuperación
    </button>

    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { supabase } from "../../lib/supabase";
import BaseInput from "../../components/ui/BaseInput.vue";

const email = ref("");
const message = ref("");
const isError = ref(false);

const clearMessage = () => {
  message.value = "";
  isError.value = false;
};

const handleRecovery = async () => {
  clearMessage();

  if (!email.value || !email.value.includes("@")) {
    message.value = "Por favor, ingresa un correo válido.";
    isError.value = true;
    return;
  }

  // Llamar a la función RPC que revisa si el correo está registrado
  const { data: exists, error } = await supabase.rpc("email_exists", {
    user_email: email.value,
  });

  if (error) {
    message.value = "Error al verificar el correo.";
    isError.value = true;
    return;
  }

  if (!exists) {
    message.value = "El correo no está registrado.";
    isError.value = true;
    return;
  }

  // Si existe, enviar el enlace de recuperación
  const { error: recoveryError } = await supabase.auth.resetPasswordForEmail(
    email.value,
    {
      redirectTo: `${import.meta.env.VITE_APP_URL}/reset-password`,
    }
  );

  if (recoveryError) {
    message.value = "Hubo un error al enviar el correo.";
    isError.value = true;
    return;
  }

  message.value = "Revisa tu correo para restablecer tu contraseña.";
  isError.value = false;
};

const messageClass = computed(() =>
  isError.value
    ? "text-red-500 text-sm text-center"
    : "text-green-500 text-sm text-center"
);
</script>
