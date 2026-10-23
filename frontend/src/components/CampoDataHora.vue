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
import { ref, computed, watch } from 'vue'
import {
  mascaraData,
  mascaraHora,
  dataBrParaIso,
  horaValida,
  formatarDataBr,
} from '@/utils/shared/formatters'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  // valor externo: ISO (YYYY-MM-DD) para data ou HH:MM para horário
  modelValue: { type: String, default: '' },
  tipo: { type: String, default: 'date', validator: (v) => ['date', 'time'].includes(v) },
  rules: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:modelValue'])

const ehData = computed(() => props.tipo === 'date')
const nativoRef = ref(null)
const texto = ref('')

// converte o valor externo para o texto exibido no campo
function paraTexto(valor) {
  if (!valor) return ''
  return ehData.value ? formatarDataBr(valor) : valor
}

// converte o texto digitado para o valor externo; retorna null se incompleto/inválido
function paraValor(textoDigitado) {
  if (ehData.value) return dataBrParaIso(textoDigitado)
  return horaValida(textoDigitado) ? textoDigitado : null
}

// regra de formato somada às regras recebidas do pai
const regras = computed(() => [
  ...props.rules,
  (v) =>
    !v ||
    paraValor(v) !== null ||
    (ehData.value ? 'Data inválida (DD/MM/AAAA)' : 'Horário inválido (HH:MM)'),
])

// sincroniza o texto quando o valor muda por fora (novo formulário, edição, recálculo)
watch(
  () => props.modelValue,
  (valor) => {
    if (paraValor(texto.value) !== valor) texto.value = paraTexto(valor)
  },
  { immediate: true },
)

// aplica a máscara e só propaga o valor quando estiver completo e válido
function aoDigitar(valor) {
  const mascarado = ehData.value ? mascaraData(valor) : mascaraHora(valor)
  texto.value = mascarado
  if (!mascarado) {
    emit('update:modelValue', '')
    return
  }
  const convertido = paraValor(mascarado)
  if (convertido !== null && convertido !== props.modelValue) {
    emit('update:modelValue', convertido)
  }
}

// abre o seletor nativo (calendário/relógio) do navegador
function abrirSeletor() {
  const nativo = nativoRef.value
  if (!nativo) return
  try {
    nativo.showPicker()
  } catch {
    nativo.focus()
    nativo.click()
  }
}

// recebe o valor escolhido no seletor nativo
function aoEscolherNoSeletor(evento) {
  const valor = evento.target.value
  if (!valor) return
  texto.value = paraTexto(valor)
  if (valor !== props.modelValue) emit('update:modelValue', valor)
}
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

