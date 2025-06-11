<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/authStore";
import BaseInput from '../../components/ui/BaseInput.vue'

const router = useRouter();
const authStore = useAuthStore();

const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const cell_phone = ref("");

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Las contraseñas no coinciden");
    return;
  }

  const payload = {
    full_name: fullName.value,
    email: email.value,
    password: password.value,
    cell_phone: cell_phone.value,
  };

  const { success, error } = await authStore.register(payload);

  if (success) {
    alert("Usuario registrado exitosamente");
    router.push("/login");
  } else {
    alert(`Error: ${JSON.stringify(error)}`);
  }
};
</script>

<template>
  <div class="w-full max-w-md px-6  space-y-3">
    <div class="text-center ">
      <img src="/logo.png" alt="Logo" class="w-20 mx-auto" />
      <h1 class="text-l md:text-2xl font-bold text-[#19296D]">
        Registre su usuario
      </h1>
    </div>

    <BaseInput
      v-model="fullName"
      type="text"
      label="Nombre completo"
      placeholder="Ej. Nombre Apellido"
      icon="fa-user"
    />
    <BaseInput
      v-model="email"
      type="email"
      label="Correo"
      placeholder="mail@example.com"
      icon="fa-envelope"
    />
    <BaseInput
      v-model="password"
      type="password"
      label="Contraseña"
      placeholder="********"
      icon="fa-lock"
    />
    <BaseInput
      v-model="confirmPassword"
      type="password"
      label="Repita su contraseña"
      placeholder="********"
      icon="fa-lock"
    />
    <BaseInput
      v-model="cell_phone"
      type="tel"
      label="Número de teléfono"
      placeholder="0999999999"
      icon="fa-phone"
    />

    <button
      @click="handleRegister"
      class="w-full bg-[#19296D] text-white py-2 rounded hover:bg-blue-900 transition"
    >
      Registrarse
    </button>

    <p class="text-center text-sm text-gray-500">
      ¿Ya tienes cuenta?
      <router-link
        to="/login"
        class="text-[#19296D] font-medium hover:underline"
      >
        Inicia sesión
      </router-link>
    </p>
  </div>
</template>
