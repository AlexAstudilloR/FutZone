<template>
  <div class="min-h-screen flex flex-col p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Gestionar Reservas</h1>
      <LinkButton
        to="/admin"
        label="Volver a panel"
        :icon="['fas', 'arrow-left']"
        size="md"
        variant="none"
        color="inherit"
        extraClass="border border-[#19296D] text-[#19296D] hover:bg-[#19296D] hover:text-white transition-colors duration-200"
      />
    </div>

    <StatusTabs v-model="selectedStatus" :tabs="statusTabs" class="mb-6" />

    <div class="flex items-center gap-2 mb-6">
      <label>Ordenar por fecha</label>
      <select
        v-model="sortOrder"
        @change="sortAppointments"
        class="border px-2 py-1 rounded"
      >
        <option value="asc">ascendente</option>
        <option value="desc">descendente</option>
      </select>
    </div>

    <div class="flex-grow">
      <div v-if="store.appointments.length > 0">
        <div v-for="appointment in sortedAppointments" :key="appointment.id">
          <AppointmentCard
            :appointment="appointment"
            @accept="updateStatus(appointment.id, 'accepted')"
            @reject="updateStatus(appointment.id, 'rejected')"
          />
        </div>
      </div>
      <NoData
        v-else-if="!store.loading"
        :message="`No hay reservas ${
          selectedStatus === 'pending'
            ? 'pendientes'
            : selectedStatus === 'accepted'
            ? 'aceptadas'
            : 'rechazadas'}`"
      />
    </div>

    <div class="mt-auto pt-6">
      <Pagination
        v-if="!store.loading && store.totalCount > 0"
        :currentPage="currentPage"
        :totalItems="store.totalCount"
        @update:page="goToPage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from "vue"
import AppointmentCard from "../../components/ui/AppointmentCard.vue"
import Pagination from "../../components/ui/Pagination.vue"
import LinkButton from "../../components/ui/LinkButton.vue"
import StatusTabs from "../../components/ui/NavBar.vue"
import NoData from "../../components/ui/NoData.vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const store = useAppointmentStore()
const currentPage = ref(1)
const sortOrder = ref("asc")
const selectedStatus = ref("pending")

const statusTabs = [
  { label: "Pendientes", value: "pending" },
  { label: "Aceptadas", value: "accepted" },
  { label: "Rechazadas", value: "rejected" },
]

const loadAppointments = async () => {
  const status = selectedStatus.value || "pending"
  await store.fetchAppointments(currentPage.value, status)
  sortAppointments()
}

const goToPage = (page) => {
  currentPage.value = page
}

const updateStatus = async (id, status) => {
  await store.updateStatus(id, status)
  loadAppointments()
}

const sortAppointments = () => {
  store.appointments.sort((a, b) => {
    return sortOrder.value === "asc"
      ? new Date(a.date) - new Date(b.date)
      : new Date(b.date) - new Date(a.date)
  })
}

const sortedAppointments = computed(() => store.appointments)

watchEffect(() => {
  currentPage.value = 1
  loadAppointments()
})
</script>
