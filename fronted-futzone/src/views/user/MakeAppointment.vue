<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAppointmentStore } from "../../stores/appointmentStore";
import { useFieldStore } from "../../stores/fieldStore";
import BaseInput from "../../components/ui/BaseInput.vue";
import BaseSelect from "../../components/ui/BaseSelect.vue";
import BaseButton from "../../components/ui/BaseButton.vue";
import TimeSlots from "../../components/ui/TimeSlots.vue";
import { toast } from "vue3-toastify";
import GenericModal from "../../components/ui/GenericModal.vue";

const appointmentStore = useAppointmentStore();
const fieldStore = useFieldStore();
const router = useRouter();
const route = useRoute();

const today = new Date().toISOString().split("T")[0];
const minDate = today;

const form = ref({
  date: today,
  field: null,
  time_start: "",
  time_end: "",
});
const isFieldPreselected = computed(() => !!route.query.fieldId);
const errors = ref({});
const showModal = ref(false);
const modalTitle = ref("");
const modalMessage = ref("");
modalTitle.value = "¡Reserva realizada!";
modalMessage.value = `En breve le llegará un mensaje a su WhatsApp con los datos de la reserva.

Si desea revisar su información, puede verla en el apartado de "Mi perfil".`;
onMounted(async () => {
  await fieldStore.fetchFields({ available: true });

  const preselectedFieldId = route.query.fieldId;
  if (preselectedFieldId) {
    const parsedId = parseInt(preselectedFieldId);
    const exists = fieldStore.fields.some((f) => f.id === parsedId);
    if (exists) {
      form.value.field = parsedId;
    }
  }
});

const fieldOptions = computed(() =>
  fieldStore.fields.map((f) => ({ value: f.id, label: f.name }))
);
const selectedFieldName = computed(() => {
  const field = fieldStore.fields.find((f) => f.id === form.value.field);
  return field?.name || "";
});
function setTimeRange({ start, end }) {
  form.value.time_start = start;
  form.value.time_end = end;
}

function goToProfile() {
  showModal.value = false;
  router.push("/profile");
}

async function submit() {
  errors.value = {};

  try {
    const selectedField = fieldStore.fields.find(
      (f) => f.id === form.value.field
    );

    await appointmentStore.createAppointment({
      date: form.value.date,
      field: form.value.field,
      time_start: form.value.time_start,
      time_end: form.value.time_end,
    });

    toast.success("Reserva creada correctamente");

    modalTitle.value = "¡Reserva confirmada!";
    modalMessage.value = `Has reservado la cancha "${selectedField?.name}"\n
    el día ${form.value.date} de ${form.value.time_start} a ${form.value.time_end}.
    Un mensaje a su WhatsApp le llegará con indicaciones para el pago.`;

    showModal.value = true;

    form.value = { date: today, field: null, time_start: "", time_end: "" };
  } catch (err) {
    errors.value = err.response?.data || {};
    if (Object.keys(errors.value).length === 0) {
      toast.error("Ocurrió un error al crear la reserva. Intenta de nuevo.");
    }
  }
}
</script>

<template>
  <div
    class="h-screen flex items-center justify-center bg-gray-50 overflow-hidden"
  >
    <div
      class="w-full max-w-4xl bg-white shadow rounded-lg grid grid-cols-1 md:grid-cols-2 gap-6 p-4 sm:p-6 max-h-[90vh] overflow-y-auto"
    >
      <div>
        <h2 class="text-2xl font-bold mb-4">
          Reservar Cancha
          <p class="text-2xl font-light text-blue-800">
            {{ selectedFieldName }}
          </p>
        </h2>
        <form @submit.prevent="submit" class="space-y-4">
          <!-- Fecha -->
          <div>
            <label class="block text-sm font-medium mb-1">
              Fecha de reserva
            </label>
            <BaseInput
              v-model="form.date"
              type="date"
              :min="minDate"
              :class="{ 'border-red-500': errors.date }"
              required
            />
            <p v-if="errors.date" class="text-red-500 text-sm mt-1">
              {{ errors.date[0] }}
            </p>
          </div>

          <!-- Cancha -->
          <div>
            <BaseSelect
              v-model="form.field"
              :options="fieldOptions"
              label="Cancha"
              placeholder="Selecciona una cancha"
              :disabled="isFieldPreselected"
              :class="{ 'border-red-500': errors.field }"
              required
            />
            <p v-if="errors.field" class="text-red-500 text-sm mt-1">
              {{ errors.field[0] }}
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">Hora inicio</label>
              <BaseInput
                v-model="form.time_start"
                type="time"
                :class="{ 'border-red-500': errors.time_start }"
                required
              />
              <p v-if="errors.time_start" class="text-red-500 text-sm mt-1">
                {{ errors.time_start[0] }}
              </p>
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Hora fin</label>
              <BaseInput
                v-model="form.time_end"
                type="time"
                :class="{ 'border-red-500': errors.time_end }"
                required
              />
              <p v-if="errors.time_end" class="text-red-500 text-sm mt-1">
                {{ errors.time_end[0] }}
              </p>
            </div>
          </div>

          <p v-if="errors.non_field_errors" class="text-red-500 text-sm">
            {{ errors.non_field_errors[0] }}
          </p>

          <div class="text-right">
            <BaseButton type="submit" variant="primary">Reservar</BaseButton>
          </div>
        </form>
      </div>

      <!-- Disponibilidad -->
      <div class="h-full flex items-center justify-center px-4 text-center">
        <transition name="fade">
          <TimeSlots
            v-if="form.field && form.date"
            :field-id="form.field"
            :date="form.date"
            @slotSelected="setTimeRange"
          />
          <div v-else class="text-gray-500 text-sm animate-fade-in">
            Selecciona una
            <span class="font-medium text-gray-700">fecha</span> y una
            <span class="font-medium text-gray-700">cancha</span><br />
            para ver los horarios disponibles.
          </div>
        </transition>
      </div>
    </div>
  </div>
  <GenericModal
    :isOpen="showModal"
    :title="modalTitle"
    :fields="[]"
    :submitLabel="'Ir a mi perfil'"
    :onSubmit="goToProfile"
    @cancel="showModal = false"
  >
    <template #default>
      <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
        {{ modalMessage }}
      </p>
    </template>
  </GenericModal>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
