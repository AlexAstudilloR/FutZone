<script setup>
import { useRouter } from "vue-router"
import { onMounted } from 'vue'

import AOS from "aos"
import "aos/dist/aos.css"

const router = useRouter()

const scrollTo = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: "smooth" })
}

onMounted(() => {
  AOS.init({
    duration: 1000,
    once: false,
    easing: 'ease-in-out',
  })
})
</script>

<template>
  <div class="text-[#19296D] bg-white scroll-smooth">

    <section class="relative bg-[#19296D] text-white text-center pt-32 pb-40 px-6 overflow-hidden">
      <div class="relative z-10" data-aos="fade-up">
        <h1 class="text-4xl font-bold mb-4">Bienvenido a FutZone</h1>
        <p class="text-lg max-w-xl mx-auto mb-6">
          Donde el fútbol se encuentra con la tecnología. Vive la mejor experiencia de reserva de canchas.
        </p>
        <div class="space-x-4">
          <button
            class="bg-white text-[#19296D] px-6 py-2 rounded hover:bg-gray-200 transition"
            @click="router.push('/login')"
          >
            Empezar ahora
          </button>
          <button
            class="border border-white px-6 py-2 rounded hover:bg-white hover:text-[#19296D] transition"
          >
            Contactanos
          </button>
        </div>
      </div>

 
      <svg class="absolute bottom-0 left-0 w-full" viewBox="0 0 1440 320">
        <path
          fill="#ffffff"
          fill-opacity="1"
          d="M0,192L60,202.7C120,213,240,235,360,245.3C480,256,600,256,720,234.7C840,213,960,171,1080,154.7C1200,139,1320,149,1380,154.7L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        ></path>
      </svg>
    </section>


    <section id="quienes-somos" class="py-20 px-6 max-w-4xl mx-auto" data-aos="fade-up">
      <h2 class="text-3xl font-semibold mb-4">¿Quiénes somos?</h2>
      <p class="text-lg text-gray-700">
        FutZone es una plataforma dedicada a facilitar reservas deportivas de manera simple y moderna.
        Conectamos jugadores con canchas disponibles en su ciudad al instante.
      </p>
    </section>

 
    <section id="mision" class="py-20 px-6 bg-gray-100 max-w-4xl mx-auto" data-aos="fade-up">
      <h2 class="text-3xl font-semibold mb-4">Nuestra Misión</h2>
      <p class="text-lg text-gray-700">
        Fomentar el deporte y la vida activa ofreciendo un sistema intuitivo para reservar canchas en tiempo real desde cualquier lugar y dispositivo.
      </p>
    </section>


    <section id="vision" class="py-20 px-6 max-w-4xl mx-auto" data-aos="fade-up">
      <h2 class="text-3xl font-semibold mb-4">Nuestra Visión</h2>
      <p class="text-lg text-gray-700">
        Convertirnos en la plataforma líder de reservas deportivas en Latinoamérica, promoviendo bienestar, comunidad y accesibilidad al deporte.
      </p>
    </section>

  
    <section
      id="caracteristicas"
      class="py-20 px-6 bg-gray-100 max-w-5xl mx-auto"
      data-aos="fade-up"
    >
      <h2 class="text-3xl font-semibold mb-10 text-center">
        Características destacadas
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 text-center text-gray-700">
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition">
          <h3 class="font-bold mb-2">Reserva instantánea</h3>
          <p>Encuentra y reserva tu cancha favorita en solo un clic, sin complicaciones ni llamadas.</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition">
          <h3 class="font-bold mb-2">Notificaciones inteligentes</h3>
          <p>Recibe alertas sobre tus reservas, cambios de horario o promociones directamente a tu móvil.</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition">
          <h3 class="font-bold mb-2">Disponibilidad en tiempo real</h3>
          <p>Consulta fácilmente qué canchas están disponibles y planifica con total confianza.</p>
        </div>
      </div>
    </section>
  </div>
</template>
