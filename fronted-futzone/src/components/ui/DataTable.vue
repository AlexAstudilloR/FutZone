<template>
  <table class="w-full border border-[#19296D]">
    <thead class="bg-[#f9fafb]">
      <tr>
        <th
          v-for="col in columns"
          :key="col.key"
          class="p-2 border text-left"
        >
          {{ col.label }}
        </th>
        <th v-if="$slots.actions" class="p-2 border">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="item in items"
        :key="item[idKey]"
        class="hover:bg-gray-50"
      >
        <td
          v-for="col in columns"
          :key="col.key"
          class="p-2 border"
        >
          {{ item[col.key] }}
        </td>
        <td v-if="$slots.actions" class="p-2 border">
          <slot name="actions" :item="item"></slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    items: { type: Array, required: true },
    columns: {
      type: Array,
      required: true,

    },
    idKey: {
      type: String,
      default: 'id'
    }
  }
}
</script>
