<template>
  <div class="overflow-x-auto rounded-lg shadow border border-gray-200">
    <table class="min-w-full divide-y divide-gray-200 text-sm">
      <thead class="bg-gray-100 text-gray-700 font-semibold">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-2 text-left whitespace-nowrap"
          >
            {{ col.label }}
          </th>
          <th v-if="$slots.actions" class="px-4 py-2 text-center">Acciones</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-100">
        <tr
          v-for="item in items"
          :key="item[idKey]"
          class="hover:bg-gray-50"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-2 whitespace-nowrap"
          >
            <slot :name="col.key" :item="item">
              {{ item[col.key] }}
            </slot>
          </td>
          <td v-if="$slots.actions" class="px-4 py-2 whitespace-nowrap">
            <slot name="actions" :item="item"></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    items: { type: Array, required: true },
    columns: { type: Array, required: true },
    idKey: {
      type: String,
      default: 'id'
    }
  }
}
</script>