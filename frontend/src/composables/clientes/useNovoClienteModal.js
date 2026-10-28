/**
 * Composable responsável pelo estado, validações e persistência do modal rápido de novo cliente.
 */
import { ref, watch } from 'vue'
import { criarCliente } from '@/services/clientes/clientesService'
import { formatPhone, formatCPF } from '@/utils/shared/formatters'

export function useNovoClienteModal(props, emit) {
  const formRef = ref(null)
  const formValido = ref(false)
  const salvando = ref(false)

  const padraoDados = () => ({
    nome: '',
    telefone: '',
    cpf: '',
    email: '',
    endereco: '',
  })

  const dados = ref(padraoDados())

  // regras de validação dos campos de cliente
  const regrasNome = [
    (v) => !!(v && String(v).trim()) || 'Nome é obrigatório',
    (v) =>
      /^[a-zA-ZÀ-ÿ\s'-]+$/.test(String(v || '').trim()) ||
      'Nome deve conter apenas letras e espaços',
  ]

  const regrasTelefone = [
    (v) => !!(v && String(v).trim()) || 'Telefone é obrigatório',
    (v) => {
      const digitos = String(v || '').replace(/\D/g, '')
      return (
        digitos.length === 10 ||
        digitos.length === 11 ||
        'Telefone deve ter 10 ou 11 dígitos'
      )
    },
  ]

  const regrasCpf = [
    (v) => !v || String(v).replace(/\D/g, '').length === 11 || 'CPF deve ter 11 dígitos',
  ]

  const regrasEmail = [
    (v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v).trim()) || 'E-mail inválido',
  ]

  // aplica máscaras de telefone e CPF ao digitar
  function aoAlterarTelefone(val) {
    dados.value.telefone = formatPhone(val)
  }

  function aoAlterarCpf(val) {
    dados.value.cpf = formatCPF(val)
  }

  // limpa os dados e a validação sempre que o modal é aberto
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

  // valida o formulário, sanitiza os campos e cria o cliente via service
  async function salvar() {
    if (!formRef.value) return
    const { valid } = await formRef.value.validate()
    if (!valid) return

    salvando.value = true
    try {
      const payload = {
        nome: dados.value.nome.trim(),
        telefone: dados.value.telefone ? String(dados.value.telefone).replace(/\D/g, '') : '',
        cpf: dados.value.cpf ? String(dados.value.cpf).replace(/\D/g, '') : null,
        email: dados.value.email ? dados.value.email.trim() : null,
        endereco: dados.value.endereco ? dados.value.endereco.trim() : '',
      }

      const resposta = await criarCliente(payload)
      emit('salvo', { id: resposta.id, nome: payload.nome, telefone: dados.value.telefone })
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
    regrasTelefone,
    regrasCpf,
    regrasEmail,
    aoAlterarTelefone,
    aoAlterarCpf,
    fechar,
    salvar,
  }
}
