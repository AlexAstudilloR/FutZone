<script setup>
import { onMounted } from 'vue'
import { useFieldStore } from '../../stores/fieldStore'
import SoccerFieldCard from '../../components/SoccerField/FieldCard.vue'

const fieldStore = useFieldStore()

onMounted(() => {
  fieldStore.fetchFields()
})
</script>

<template>
  <div class="p-4">
    <div class="mb-6 text-center">
      <h1 class="text-2xl font-bold text-[#19296D]">Canchas disponibles</h1>
      <p class="text-gray-600 mt-2">
        Ven y disfruta con amigos y familia en nuestros distintos tipos de cancha
      </p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
      <SoccerFieldCard
        v-for="field in fieldStore.fields"
        :key="field.id"
        :nombre="field.name"
        :tipo="field.field_type"
        :precio="field.price"
      />
    </div>
  </div>
</template>
