/**
 * Composable responsável pelo estado, validações e persistência do modal rápido de novo procedimento.
 */
import { ref, watch } from 'vue'
import { criarServico } from '@/services/servicos/servicosService'

export function useNovoProcedimentoModal(props, emit) {
  const formRef = ref(null)
  const formValido = ref(false)
  const salvando = ref(false)

  const padraoDados = () => ({
    nome: '',
    duracao_minutos: 30,
    preco: null,
    descricao: '',
  })

  const dados = ref(padraoDados())

  const regrasNome = [(v) => !!v || 'O nome do procedimento é obrigatório']

  const regrasDuracao = [(v) => (v != null && v > 0) || 'Informe a duração em minutos']

  // reinicia os campos e a validação sempre que o modal é aberto
  watch(
    () => props.modelValue,
    (aberto) => {
      if (aberto) {
        dados.value = padraoDados()
        if (formRef.value) formRef.value.resetValidation()
      }
    }
  )

  function fechar() {
    emit('update:modelValue', false)
  }

  // valida o formulário, formata o payload numérico e persiste o novo procedimento via service
  async function salvar() {
    if (!formRef.value) return
    const { valid } = await formRef.value.validate()
    if (!valid) return

    salvando.value = true
    try {
      const payload = {
        nome: dados.value.nome.trim(),
        duracao_minutos: Number(dados.value.duracao_minutos) || 30,
        preco:
          dados.value.preco != null && dados.value.preco !== ''
            ? Number(dados.value.preco)
            : null,
        descricao: dados.value.descricao ? dados.value.descricao.trim() : '',
      }

      const resposta = await criarServico(payload)
      emit('salvo', {
        id: resposta.id,
        nome: payload.nome,
        preco: payload.preco,
        duracao_minutos: payload.duracao_minutos,
      })
      fechar()
    } finally {
      salvando.value = false
    }
  }

  return {
    formRef,
    formValido,
    salvando,
    dados,
    regrasNome,
    regrasDuracao,
    fechar,
    salvar,
  }
}

