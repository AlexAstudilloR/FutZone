<template>
  <div class="text-[#19296D] bg-white scroll-smooth">
    <section
      class="relative min-h-[85vh] flex flex-col justify-center items-center px-6 text-white text-center bg-gradient-to-br from-[#19296D] via-[#1E3A8A] to-[#3B82F6] overflow-hidden"
      data-aos="fade-up"
    >
      <font-awesome-icon
        icon="futbol"
        class="absolute top-12 left-12 text-white/10 text-6xl"
      />
      <font-awesome-icon
        icon="users"
        class="absolute bottom-12 right-12 text-white/10 text-5xl rotate-12"
      />
      <font-awesome-icon
        icon="bolt"
        class="absolute top-1/2 left-[10%] text-white/10 text-5xl -rotate-12"
      />

      <div class="z-10 max-w-4xl">
        <div
          class="inline-flex items-center px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/20"
        >
          <span
            class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"
          ></span>
          Plataforma líder en reservas deportivas
        </div>

        <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          Bienvenido a
          <span
            class="bg-gradient-to-r from-blue-200 to-white bg-clip-text text-transparent"
          >
            FutZone
          </span>
        </h1>

        <p
          class="text-xl md:text-2xl text-white/90 mb-8 max-w-2xl mx-auto leading-relaxed"
        >
          Donde el fútbol se encuentra con la tecnología. Vive la mejor
          experiencia de reserva de canchas en tiempo real.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            class="bg-white text-[#19296D] px-8 py-4 rounded-lg hover:bg-gray-100 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            @click="router.push('/login')"
          >
            🚀 Empezar ahora
          </button>
          <button
            class="border-2 border-white px-8 py-4 rounded-lg hover:bg-white hover:text-[#19296D] transition-all duration-300 font-semibold text-lg backdrop-blur-sm"
          >
            📞 Contáctanos
          </button>
        </div>
      </div>
    </section>
    <section
      class="py-20 px-6 relative overflow-hidden bg-white"
      data-aos="fade-up"
    >
      <div
        class="absolute inset-0 z-0 pointer-events-none bg-[radial-gradient(circle,_rgba(25,41,109,0.05)_1px,transparent_1px)] bg-[length:40px_40px]"
      ></div>

      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold mb-6 text-[#19296D]">
          Conoce FutZone
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Descubre quiénes somos, nuestra misión y visión para revolucionar las
          reservas deportivas
        </p>
      </div>

      <div
        class="relative h-[500px] w-full flex items-center justify-center z-10"
      >
        <div
          class="absolute w-[600px] h-[600px] bg-blue-200 opacity-20 rounded-full blur-3xl left-1/2 -translate-x-1/2 top-[20%] pointer-events-none z-0"
        ></div>

        <div class="relative w-[500px] h-[500px]" style="perspective: 1000px">
          <div
            class="relative w-full h-full transition-transform duration-700 ease-out"
            style="transform-style: preserve-3d"
            :style="{
              transform: `rotateY(${
                -selectedCard * (360 / institucional.length)
              }deg)`,
            }"
          >
            <PokerCard
              v-for="(card, index) in institucional"
              :key="card.id"
              v-bind="card"
              :index="index"
              :selected-id="selectedCard"
              :is-rotating="rotating"
              :total="institucional.length"
              :radius="220"
              @select="selectCard"
            />
          </div>
        </div>
      </div>

      <div class="flex justify-center mt-8 space-x-4 z-10 relative">
        <button
          v-for="(_, index) in institucional"
          :key="index"
          @click="selectCard(index)"
          :disabled="rotating"
          class="w-3 h-3 rounded-full transition-all duration-300"
          :class="[
            selectedCard === index
              ? 'bg-[#19296D] scale-125'
              : 'bg-gray-400 hover:bg-gray-600',
            rotating ? 'pointer-events-none' : '',
          ]"
        ></button>
      </div>
    </section>

    <section
      id="caracteristicas"
      class="py-20 px-6 bg-gray-100 max-w-5xl mx-auto"
      data-aos="fade-up"
    >
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold mb-6 text-[#19296D]">
          Características Destacadas
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Descubre las funcionalidades que hacen de FutZone la mejor opción para
          tus reservas deportivas
        </p>
      </div>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 text-center text-gray-700"
      >
        <div
          class="bg-white p-6 rounded shadow hover:shadow-lg transition transform hover:-translate-y-1"
          data-aos="zoom-in-up"
        >
          <font-awesome-icon
            :icon="['fas', 'bolt']"
            class="text-3xl text-blue-600 mb-3"
          />
          <h3 class="font-bold text-lg mb-2">Reserva instantánea</h3>
          <p>
            Encuentra y reserva tu cancha favorita en solo un clic, sin
            complicaciones ni llamadas.
          </p>
        </div>

        <div
          class="bg-white p-6 rounded shadow hover:shadow-lg transition transform hover:-translate-y-1"
          data-aos="zoom-in-down"
        >
          <font-awesome-icon
            :icon="['fas', 'bell']"
            class="text-3xl text-blue-600 mb-3"
          />
          <h3 class="font-bold text-lg mb-2">Notificaciones inteligentes</h3>
          <p>
            Recibe alertas sobre tus reservas, cambios de horario o promociones
            directamente a tu móvil.
          </p>
        </div>

        <div
          class="bg-white p-6 rounded shadow hover:shadow-lg transition transform hover:-translate-y-1"
          data-aos="zoom-in"
        >
          <font-awesome-icon
            :icon="['fas', 'clock']"
            class="text-3xl text-blue-600 mb-3"
          />
          <h3 class="font-bold text-lg mb-2">Disponibilidad en tiempo real</h3>
          <p>
            Consulta fácilmente qué canchas están disponibles y planifica con
            total confianza.
          </p>
        </div>
      </div>
       <div class="text-center mt-16">
          <button 
            class="bg-gradient-to-r from-[#19296D] to-[#3B82F6] text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
            @click="router.push('/register')"
          >
            Prueba todas las características 🚀
          </button>
        </div>
    </section>

    <section
      id="colaboradores"
      class="py-24 px-6 bg-gradient-to-b from-gray-50 to-white"
      data-aos="fade-up"
    >
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-6 text-[#19296D]">
            Nuestro Equipo
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Conoce a los desarrolladores apasionados que hacen posible FutZone
          </p>
        </div>

        <div class="flex flex-wrap justify-center gap-8">
          <AvatarCard
            v-for="(colaborador, index) in colaboradores"
            :key="index"
            :name="colaborador.name"
            :role="colaborador.role"
            :description="colaborador.description"
            :skills="colaborador.skills"
            :verified="colaborador.verified"
            :data-aos-delay="index * 100"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import AOS from "aos";
import "aos/dist/aos.css";

import PokerCard from "../../components/ui/PokerCard.vue";
import AvatarCard from "../../components/ui/AvatarCard.vue";

const router = useRouter();

const colaboradores = [
  {
    name: "Eicker Alejandro Villamar Romero",
    role: "Frontend Developer",
    description:
      "Apasionado por las interfaces limpias y la experiencia de usuario moderna.",
    skills: ["Vue3", "Tailwind", "Pinia", "Vite"],
    verified: true,
  },
  {
    name: "Alex Enrique Astudillo Rodríguez",
    role: "Backend Developer",
    description:
      "Especializado en APIs robustas con Django y autenticación segura con Supabase.",
    skills: ["Django", "DRF", "Supabase", "PostgreSQL"],
    verified: true,
  },
];

const institucional = [
  {
    id: 1,
    title: "¿Quiénes somos?",
    subtitle: "Nuestra identidad",
    description:
      "FutZone es una plataforma dedicada a facilitar reservas deportivas de manera simple y moderna. Conectamos jugadores con canchas disponibles en su ciudad al instante.",
    icon: "users",
    gradient: "from-[#1e3a8a] to-[#3b82f6]",
  },
  {
    id: 2,
    title: "Nuestra Misión",
    subtitle: "Propósito",
    description:
      "Fomentar el deporte y la vida activa ofreciendo un sistema intuitivo para reservar canchas en tiempo real desde cualquier lugar y dispositivo.",
    icon: "compass",
    gradient: "from-[#3b82f6] to-[#60a5fa]",
  },
  {
    id: 3,
    title: "Nuestra Visión",
    subtitle: "Futuro",
    description:
      "Convertirnos en la plataforma líder de reservas deportivas en Latinoamérica, promoviendo bienestar, comunidad y accesibilidad al deporte.",
    icon: "eye",
    gradient: "from-[#6366f1] to-[#818cf8]",
  },
];

const selectedCard = ref(0);
const rotating = ref(false);

function selectCard(index) {
  if (!rotating.value && index !== selectedCard.value) {
    rotating.value = true;
    selectedCard.value = index;
    setTimeout(() => {
      rotating.value = false;
    }, 800);
  }
}

onMounted(() => {
  AOS.init({
    duration: 1000,
    once: false,
    easing: "ease-in-out",
  });
});
</script>
