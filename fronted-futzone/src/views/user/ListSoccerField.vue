<script setup>
import { ref, onMounted } from "vue";
import { useFieldStore } from "../../stores/fieldStore";
import SoccerFieldCard from "../../components/SoccerField/FieldCard.vue";
import GenericModal from "../../components/ui/GenericModal.vue";
import AppointmentForm from "../../components/appointments/AppointmentForm.vue";
import TimeSlots from "../../components/ui/TimeSlots.vue";
import { useAppointmentStore } from "../../stores/appointmentStore";
import {toast} from "vue3-toastify"
const fieldStore = useFieldStore();
const appointmentStore = useAppointmentStore();

const showReservationModal = ref(false);
const selectedField = ref(null);
const selectedSlot = ref({ start: "", end: "" });
const selectedDate = ref(new Date().toISOString().split("T")[0]);

const appointmentFormRef = ref(null);

function handleReservar(fieldData) {
  selectedField.value = fieldData;
  selectedSlot.value = { start: "", end: "" };
  showReservationModal.value = true;
}

function handleSlotSelected(slot) {
  selectedSlot.value = { ...slot };
}

async function handleReservationSubmit() {
  if (!appointmentFormRef.value) return;

  const formData = appointmentFormRef.value.getFormData();
  try {
    await appointmentStore.createAppointment(formData);
    showReservationModal.value = false;
    toast.success("Reserva creada con exito, puedes verla en Mi perfil")
  } catch (err) {
    toast.error("Error al crear la reserva:", err);
  }
}

onMounted(() => {
  fieldStore.fetchFields();
});
</script>

<template>
  <div class="p-4">
    <div class="mb-6 text-center">
      <h1 class="text-2xl font-bold text-[#19296D]">Canchas disponibles</h1>
      <p class="text-gray-600 mt-2 text-xl">
        Tu equipo, tu cancha, tu momento. ¡Haz tu reserva ahora!
      </p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <SoccerFieldCard
        v-for="field in fieldStore.fields"
        :key="field.id"
        :id="field.id"
        :nombre="field.name"
        :tipo="field.field_type"
        :precio="field.price"
        :imagen="field.image"
        @reservar="handleReservar"
      />
    </div>

    <GenericModal
      :isOpen="showReservationModal"
      title="Reservar cancha"
      :fields="[]"
      :submitLabel="'Reservar'"
      @cancel="showReservationModal = false"
      @submit="handleReservationSubmit"
    >
      <template #form>
        <AppointmentForm
          ref="appointmentFormRef"
          v-if="selectedField"
          :preselectedField="selectedField"
          :preselectedSlot="selectedSlot"
          @close="showReservationModal = false"
          @update-date="selectedDate = $event"
        />
      </template>

      <template #timeslots>
        <div v-if="selectedField" class="w-full md:w-full">
          <TimeSlots
            :field-id="selectedField.id"
            :date="selectedDate"
            @slotSelected="handleSlotSelected"
          />
        </div>
      </template>
    </GenericModal>
  </div>
</template>