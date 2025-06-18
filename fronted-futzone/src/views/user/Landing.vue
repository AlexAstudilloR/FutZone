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


      <div class="z-10 max-w-2xl">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 leading-tight">
          Bienvenido a <span class="text-blue-200">FutZone</span>
        </h1>
        <p class="text-lg md:text-xl text-white/80 mb-8">
          Donde el fútbol se encuentra con la tecnología. Vive la mejor
          experiencia de reserva de canchas.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            class="bg-white text-[#19296D] px-6 py-2 rounded hover:bg-gray-200 transition font-semibold"
            @click="router.push('/login')"
          >
            Empezar ahora
          </button>
          <button
            class="border border-white px-6 py-2 rounded hover:bg-white hover:text-[#19296D] transition font-semibold"
          >
            Contáctanos
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


      <h2
        class="text-3xl font-semibold mb-10 text-center text-[#19296D] z-10 relative will-change-transform underline underline-offset-4"
      >
        Sobre Nosotros
      </h2>

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
      <h2 class="text-3xl font-semibold mb-10 text-center">
        Características destacadas
      </h2>
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
    </section>


    <section
      id="colaboradores"
      class="py-16 px-6 bg-white max-w-5xl mx-auto"
      data-aos="fade-up"
    >
      <h2 class="text-3xl font-semibold mb-10 text-center">
        Colaboradores del Software
      </h2>
      <div class="flex flex-wrap justify-center gap-8">
        <AvatarCard
          v-for="colaborador in colaboradores"
          :key="colaborador"
          :name="colaborador"
          avatar="/profile.jpeg"
        />
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
  "Eicker Alejandro Villamar Romero",
  "Alex Enrique Astudillo Rodríguez",
  "Moncho Ezequiel Astudillo Rodríguez",
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
