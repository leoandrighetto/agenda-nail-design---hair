/**
 * Composable responsável pela máscara, validação, conversão de formato e acionamento
 * do seletor nativo para campos de data (DD/MM/AAAA) e horário (HH:MM).
 */
import { ref, computed, watch } from 'vue'
import {
  mascaraData,
  mascaraHora,
  dataBrParaIso,
  horaValida,
  formatarDataBr,
} from '@/utils/shared/formatters'

export function useCampoDataHora(props, emit) {
  const ehData = computed(() => props.tipo === 'date')
  const nativoRef = ref(null)
  const texto = ref('')

  // converte o valor externo (ISO ou HH:MM) para o texto exibido no campo
  function paraTexto(valor) {
    if (!valor) return ''
    return ehData.value ? formatarDataBr(valor) : valor
  }

  // converte o texto digitado para o valor externo; retorna null se incompleto/inválido
  function paraValor(textoDigitado) {
    if (ehData.value) return dataBrParaIso(textoDigitado)
    return horaValida(textoDigitado) ? textoDigitado : null
  }

  // regra de formato somada às regras recebidas do componente pai
  const regras = computed(() => [
    ...props.rules,
    (v) =>
      !v ||
      paraValor(v) !== null ||
      (ehData.value ? 'Data inválida (DD/MM/AAAA)' : 'Horário inválido (HH:MM)'),
  ])

  // sincroniza o texto exibido quando o modelValue muda externamente
  watch(
    () => props.modelValue,
    (valor) => {
      if (paraValor(texto.value) !== valor) texto.value = paraTexto(valor)
    },
    { immediate: true }
  )

  // aplica a máscara durante a digitação e emite apenas quando o valor for válido
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

  // aciona o seletor nativo de data ou hora do navegador
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

  // sincroniza o valor escolhido através do seletor nativo
  function aoEscolherNoSeletor(evento) {
    const valor = evento.target.value
    if (!valor) return
    texto.value = paraTexto(valor)
    if (valor !== props.modelValue) emit('update:modelValue', valor)
  }

  return {
    ehData,
    nativoRef,
    texto,
    regras,
    aoDigitar,
    abrirSeletor,
    aoEscolherNoSeletor,
  }
}

