/**
 * Composable responsável pelo estado reativo, validações e regras de negócio de clientes.
 */
import { ref, computed } from 'vue'
import {
  listarClientes,
  criarCliente,
  atualizarCliente,
  excluirCliente,
} from '@/services/clientes/clientesService'
import { formatPhone, formatCPF } from '@/utils/shared/formatters'

export function useClientes(showMessage) {
  const clientes = ref([])
  const loading = ref(false)
  const saving = ref(false)

  const defaultItem = {
    id: null,
    nome: '',
    telefone: '',
    cpf: '',
    email: '',
    endereco: '',
  }

  const editedItem = ref({ ...defaultItem })

  const formTitle = computed(() => {
    return editedItem.value.id ? 'Editar Cliente' : 'Novo Cliente'
  })

  // regras de validação dos campos do formulário de cliente
  const nameRules = [
    (v) => !!v || 'Nome é obrigatório',
    (v) => /^[a-zA-ZÀ-ÿ\s]+$/.test(v) || 'Nome deve conter apenas letras e espaços',
  ]

  const phoneRules = [
    (v) => !!v || 'Telefone é obrigatório',
    (v) => (v && String(v).replace(/\D/g, '').length === 11) || 'Telefone deve ter 11 dígitos',
  ]

  const cpfRules = [
    (v) => !v || String(v).replace(/\D/g, '').length === 11 || 'CPF deve ter 11 dígitos',
  ]

  const emailRules = [
    (v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'E-mail inválido',
  ]

  // restaura o item em edição para os valores iniciais em branco
  function resetEditedItem() {
    editedItem.value = { ...defaultItem }
  }

  // preenche o item em edição garantindo a aplicação das máscaras visuais
  function setEditedItem(item) {
    editedItem.value = {
      ...item,
      telefone: formatPhone(item.telefone),
      cpf: formatCPF(item.cpf),
    }
  }

  // carrega a lista de clientes aplicando formatação de telefone e CPF
  async function fetchClientes() {
    loading.value = true
    try {
      const data = await listarClientes()
      clientes.value = data.map((c) => ({
        ...c,
        telefone: formatPhone(c.telefone),
        cpf: formatCPF(c.cpf),
      }))
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro de conexão ao servidor Flask', 'error')
      }
    } finally {
      loading.value = false
    }
  }

  // cria ou atualiza um cliente sanitizando máscaras e endereço antes de enviar ao service
  async function saveCliente() {
    saving.value = true
    const isEdit = Boolean(editedItem.value.id)
    const addressVal = editedItem.value.endereco

    const payload = {
      nome: editedItem.value.nome,
      telefone: editedItem.value.telefone ? String(editedItem.value.telefone).replace(/\D/g, '') : '',
      cpf: editedItem.value.cpf ? String(editedItem.value.cpf).replace(/\D/g, '') : null,
      email: editedItem.value.email || null,
      endereco:
        typeof addressVal === 'object' && addressVal !== null
          ? addressVal.formatted_address || addressVal.display_name || ''
          : addressVal || '',
    }

    try {
      if (isEdit) {
        await atualizarCliente(editedItem.value.id, payload)
      } else {
        await criarCliente(payload)
      }

      if (showMessage) {
        showMessage(`Cliente ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso`)
      }
      await fetchClientes()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  // exclui o cliente selecionado e recarrega a listagem
  async function deleteCliente() {
    if (!editedItem.value.id) return false
    saving.value = true
    try {
      await excluirCliente(editedItem.value.id)
      if (showMessage) {
        showMessage('Cliente excluído com sucesso')
      }
      await fetchClientes()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao excluir cliente', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  return {
    clientes,
    loading,
    saving,
    editedItem,
    formTitle,
    nameRules,
    phoneRules,
    cpfRules,
    emailRules,
    resetEditedItem,
    setEditedItem,
    fetchClientes,
    saveCliente,
    deleteCliente,
  }
}

