<script setup>
import { ref, onMounted } from "vue";
import { useFieldStore } from "../../stores/fieldStore";
import SoccerFieldCard from "../../components/SoccerField/FieldCard.vue";
import GenericModal from "../../components/ui/GenericModal.vue";

const fieldStore = useFieldStore();

onMounted(() => {
  fieldStore.fetchFields();
});


const showModal = ref(false);
const selectedField = ref(null);
const modalErrors = ref({});


const modalFields = [
  {
    model: "date",
    label: "Fecha de reserva",
    type: "date",
    required: true,
  },
  {
    model: "time_start",
    label: "Hora inicio",
    type: "time",
    required: true,
  },
  {
    model: "time_end",
    label: "Hora fin",
    type: "time",
    required: true,
  },
];


function handleReservar(fieldData) {
  selectedField.value = {
    ...fieldData,
    field: fieldData.id,
    date: "",
    time_start: "",
    time_end: "",
  };
  showModal.value = true;
}


async function submitReserva(form) {
  try {
    modalErrors.value = {};
    await appointmentStore.createAppointment({
      date: form.date,
      time_start: form.time_start,
      time_end: form.time_end,
      field: selectedField.value.id,
    });
    showModal.value = false;
    selectedField.value = null;
    alert("Reserva creada correctamente");
  } catch (err) {
    modalErrors.value = err.response?.data || {};
  }
}
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
      :isOpen="showModal"
      title="Reservar Cancha"
      :fields="modalFields"
      :initialData="selectedField"
      :errors="modalErrors"
      submitLabel="Reservar"
      @submit="submitReserva"
      @cancel="() => (showModal = false)"
    />
  </div>
</template>
