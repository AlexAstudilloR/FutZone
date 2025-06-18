<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/authStore";
import { toast } from "vue3-toastify";
import BaseInput from "../../components/ui/BaseInput.vue";

const router = useRouter();
const authStore = useAuthStore();

const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const cell_phone = ref("");

const errors = reactive({
  full_name: "",
  email: "",
  password: "",
  confirmPassword: "",
  cell_phone: "",
});

const handleRegister = async () => {
  Object.keys(errors).forEach((key) => (errors[key] = ""));
  authStore.error = null;

  if (password.value !== confirmPassword.value) {
    errors.confirmPassword = "Las contraseñas no coinciden";
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
    toast.success("Tu cuenta fue creada correctamente");
    router.push("/login");
  } else {
    let handled = false;

    if (typeof error === "string") {
      if (error.includes("nombre")) {
        errors.full_name = error;
        handled = true;
      } else if (error.includes("correo")) {
        errors.email = error;
        handled = true;
      } else if (error.includes("contraseña")) {
        errors.password = error;
        handled = true;
      } else if (
        error.includes("celular") ||
        error.includes("teléfono") ||
        error.includes("número")
      ) {
        errors.cell_phone = error;
        handled = true;
      }
    }

    if (!handled) {
      toast.error(
        typeof error === "string"
          ? error
          : "Revisa los campos e intenta de nuevo"
      );
      authStore.error =
        typeof error === "string" ? error : "Error desconocido al registrar.";
    }
  }
};
</script>

<template>
  <div class="w-full max-w-md px-6 space-y-3">
    <div class="text-center">
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
      :error="errors.full_name"
      @input="errors.full_name = ''"
    />

    <BaseInput
      v-model="email"
      type="email"
      label="Correo"
      placeholder="mail@example.com"
      icon="fa-envelope"
      :error="errors.email"
      @input="errors.email = ''"
    />

    <BaseInput
      v-model="password"
      type="password"
      label="Contraseña"
      placeholder="********"
      icon="fa-lock"
      :error="errors.password"
      @input="errors.password = ''"
    />

    <BaseInput
      v-model="confirmPassword"
      type="password"
      label="Repita su contraseña"
      placeholder="********"
      icon="fa-lock"
      :error="errors.confirmPassword"
      @input="errors.confirmPassword = ''"
    />

    <BaseInput
      v-model="cell_phone"
      type="tel"
      label="Número de teléfono"
      placeholder="0999999999"
      icon="fa-phone"
      :error="errors.cell_phone"
      @input="errors.cell_phone = ''"
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
