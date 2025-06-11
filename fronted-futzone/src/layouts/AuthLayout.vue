<template>
  <div class="flex min-h-screen bg-[#f6f9ff]">

    <div
      class="flex flex-col justify-center items-center w-full xl:w-[60%] px-6 py-10 overflow-y-auto"
    >
      <div class="w-full max-w-md">
        <slot />
      </div>
    </div>


    <div class="hidden xl:block xl:w-[40%]">
      <img
        src="/auth-image.svg"
        alt="Fútbol"
        class="w-full h-full max-h-screen object-cover"
      />
    </div>
  </div>
</template>
