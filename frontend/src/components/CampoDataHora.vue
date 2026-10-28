<template>
  <v-text-field
    v-bind="$attrs"
    :model-value="texto"
    type="text"
    inputmode="numeric"
    autocomplete="off"
    :maxlength="ehData ? 10 : 5"
    :placeholder="ehData ? 'DD/MM/AAAA' : 'HH:MM'"
    :rules="regras"
    @update:model-value="aoDigitar"
  >
    <!-- ícone interativo à esquerda que abre o seletor nativo do navegador -->
    <template v-slot:prepend-inner>
      <div class="campo-data-hora__seletor">
        <v-icon
          :icon="ehData ? 'mdi-calendar' : 'mdi-clock-outline'"
          :title="ehData ? 'Abrir calendário' : 'Abrir seletor de horário'"
          class="cursor-pointer"
          @click="abrirSeletor"
        ></v-icon>
        <input
          ref="nativoRef"
          class="campo-data-hora__nativo"
          :type="tipo"
          :value="modelValue || ''"
          tabindex="-1"
          aria-hidden="true"
          @input="aoEscolherNoSeletor"
        />
      </div>
    </template>
  </v-text-field>
</template>

<script setup>
/**
 * Campo de data (DD/MM/AAAA) ou horário (HH:MM) digitável, com cursor de texto e seletor nativo acionado pelo ícone.
 */
import { useCampoDataHora } from '@/composables/shared/useCampoDataHora'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  // valor externo: ISO (YYYY-MM-DD) para data ou HH:MM para horário
  modelValue: { type: String, default: '' },
  tipo: { type: String, default: 'date', validator: (v) => ['date', 'time'].includes(v) },
  rules: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:modelValue'])

const {
  ehData,
  nativoRef,
  texto,
  regras,
  aoDigitar,
  abrirSeletor,
  aoEscolherNoSeletor,
} = useCampoDataHora(props, emit)
</script>

<style scoped>
.campo-data-hora__seletor {
  position: relative;
  display: inline-flex;
  align-items: center;
}

/* input nativo invisível, posicionado sob o ícone para ancorar o seletor */
.campo-data-hora__nativo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  pointer-events: none;
  border: 0;
  padding: 0;
}
</style>

