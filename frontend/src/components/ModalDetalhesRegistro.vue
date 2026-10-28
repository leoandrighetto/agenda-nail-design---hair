<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600px"
    persistent
    :z-index="2500"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card rounded="lg" class="d-flex flex-column modal-detalhes-card">
      <v-card-title :class="['pa-4 text-white d-flex align-center justify-space-between', headerBgClass]">
        <div class="d-flex align-center ga-2">
          <v-icon>{{ icon || 'mdi-information-outline' }}</v-icon>
          <span class="text-h6 font-weight-bold">{{ title }}</span>
        </div>
        <v-btn icon="mdi-close" variant="text" color="white" size="small" @click="fechar"></v-btn>
      </v-card-title>

      <v-card-text class="pa-5 flex-grow-1 overflow-y-auto">
        <slot></slot>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4 bg-surface justify-end">
        <slot name="actions">
          <v-btn color="grey-darken-1" variant="text" @click="fechar">Fechar</v-btn>
        </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
/**
 * Componente reutilizável de modal/card informativo de detalhes.
 * Permite apresentar informações completas de um registro com layout fixo e padronizado.
 */
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Detalhes',
  },
  icon: {
    type: String,
    default: 'mdi-information-outline',
  },
  color: {
    type: String,
    default: 'primary',
  },
})

const emit = defineEmits(['update:modelValue', 'close'])

const headerBgClass = computed(() => {
  if (props.color === 'accent') return 'bg-accent'
  if (props.color === 'secondary') return 'bg-secondary'
  if (props.color === 'info') return 'bg-info'
  if (props.color === 'success') return 'bg-success'
  return 'bg-primary'
})

function fechar() {
  emit('update:modelValue', false)
  emit('close')
}
</script>

<style scoped>
.modal-detalhes-card {
  max-height: 85vh;
}
</style>

