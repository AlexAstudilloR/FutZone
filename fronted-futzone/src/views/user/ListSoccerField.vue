<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useFieldStore } from "../../stores/fieldStore";
import SoccerFieldCard from "../../components/SoccerField/FieldCard.vue";

const fieldStore = useFieldStore();
const router = useRouter();

onMounted(() => {
  fieldStore.fetchFields();
});

function handleReservar(fieldData) {
  router.push({ name: "Reservar", query: { fieldId: fieldData.id } });
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
  </div>
</template>

