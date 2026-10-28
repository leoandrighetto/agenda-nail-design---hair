/**
 * Composable responsável pelo gerenciamento de serviços, materiais, equipamentos,
 * indicadores de estoque, regras de validação e controle dos formulários/modais.
 */
import { ref, computed } from 'vue'
import {
  listarServicos,
  criarServico,
  atualizarServico,
  excluirServico,
} from '@/services/servicos/servicosService'
import {
  listarMateriais,
  criarMaterial,
  atualizarMaterial,
  excluirMaterial,
} from '@/services/estoque/materiaisService'
import {
  listarEquipamentos,
  criarEquipamento,
  atualizarEquipamento,
  excluirEquipamento,
} from '@/services/estoque/equipamentosService'
import { isResourceAvailable } from '@/utils/estoque/estoqueUtils'

export function useServicosEstoque(showMessage) {
  const loading = ref(false)
  const saving = ref(false)

  const servicos = ref([])
  const materiais = ref([])
  const equipamentos = ref([])

  // controle de abas, modais e referências de validação dos formulários
  const activeTab = ref('servicos')

  const servicoDialog = ref(false)
  const servicoValid = ref(false)
  const servicoFormRef = ref(null)

  const materialDialog = ref(false)
  const materialValid = ref(false)
  const materialFormRef = ref(null)

  const equipamentoDialog = ref(false)
  const equipamentoValid = ref(false)
  const equipamentoFormRef = ref(null)

  const deleteDialog = ref(false)
  const deleteTarget = ref({ type: '', id: null, nome: '' })

  const defaultServico = {
    id: null,
    nome: '',
    descricao: '',
    duracao_minutos: 60,
    preco: null,
    materiais_ids: [],
    equipamentos_ids: [],
  }
  const servicoForm = ref({ ...defaultServico })

  const defaultMaterial = {
    id: null,
    nome: '',
    descricao: '',
    quantidade: 1,
    disponivel: true,
  }
  const materialForm = ref({ ...defaultMaterial })

  const defaultEquipamento = {
    id: null,
    nome: '',
    descricao: '',
    quantidade: 1,
    disponivel: true,
  }
  const equipamentoForm = ref({ ...defaultEquipamento })

  // títulos dinâmicos dos modais de criação e edição
  const servicoFormTitle = computed(() =>
    servicoForm.value.id ? 'Editar Serviço' : 'Novo Serviço'
  )
  const materialFormTitle = computed(() =>
    materialForm.value.id ? 'Editar Material' : 'Novo Material'
  )
  const equipamentoFormTitle = computed(() =>
    equipamentoForm.value.id ? 'Editar Equipamento' : 'Novo Equipamento'
  )

  // regras de validação dos formulários de serviços, materiais e equipamentos
  const servicoNomeRules = [(v) => !!v || 'O nome do serviço é obrigatório']
  const servicoDuracaoRules = [(v) => (v && v > 0) || 'Informe a duração']
  const materialNomeRules = [(v) => !!v || 'O nome do material é obrigatório']
  const equipamentoNomeRules = [(v) => !!v || 'O nome do equipamento é obrigatório']

  // indicadores computados (KPIs de disponibilidade)
  const servicosComFalta = computed(() => {
    return servicos.value.filter((s) => !s.recursos_disponiveis).length
  })

  const materiaisEmFalta = computed(() => {
    return materiais.value.filter((m) => !isResourceAvailable(m)).length
  })

  const equipamentosIndisponiveis = computed(() => {
    return equipamentos.value.filter((e) => !isResourceAvailable(e)).length
  })

  // verifica em tempo real no formulário do serviço se algum recurso escolhido está em falta
  const recursosFaltantesNoFormulario = computed(() => {
    const faltantes = []
    for (const id of servicoForm.value.materiais_ids || []) {
      const mat = materiais.value.find((m) => m.id === id)
      if (mat && !isResourceAvailable(mat)) {
        faltantes.push(`${mat.nome} (Material)`)
      }
    }
    for (const id of servicoForm.value.equipamentos_ids || []) {
      const eq = equipamentos.value.find((e) => e.id === id)
      if (eq && !isResourceAvailable(eq)) {
        faltantes.push(`${eq.nome} (Equipamento)`)
      }
    }
    return faltantes
  })

  // sincroniza automaticamente a flag de disponibilidade ao alterar a quantidade nos formulários
  function aoAlterarQuantidadeMaterial(val) {
    materialForm.value.disponivel = Number(val) > 0
  }

  function aoAlterarQuantidadeEquipamento(val) {
    equipamentoForm.value.disponivel = Number(val) > 0
  }

  // carrega serviços, materiais e equipamentos em paralelo via services
  async function fetchAllData() {
    loading.value = true
    try {
      const [listaServ, listaMat, listaEq] = await Promise.all([
        listarServicos(),
        listarMateriais(),
        listarEquipamentos(),
      ])
      servicos.value = listaServ
      materiais.value = listaMat
      equipamentos.value = listaEq
    } catch (error) {
      if (showMessage) {
        showMessage('Erro de conexão com o servidor Flask', 'error')
      }
    } finally {
      loading.value = false
    }
  }

  // prepara o formulário de serviço para criação ou edição
  function prepareServicoForm(item = null) {
    if (item) {
      servicoForm.value = {
        id: item.id,
        nome: item.nome,
        descricao: item.descricao || '',
        duracao_minutos: item.duracao_minutos || 30,
        preco: item.preco,
        materiais_ids: (item.materiais || []).map((m) => m.id),
        equipamentos_ids: (item.equipamentos || []).map((e) => e.id),
      }
    } else {
      servicoForm.value = { ...defaultServico, materiais_ids: [], equipamentos_ids: [] }
    }
  }

  // prepara o formulário de material para criação ou edição
  function prepareMaterialForm(item = null) {
    materialForm.value = item ? { ...item } : { ...defaultMaterial }
  }

  // prepara o formulário de equipamento para criação ou edição
  function prepareEquipamentoForm(item = null) {
    equipamentoForm.value = item ? { ...item } : { ...defaultEquipamento }
  }

  // abre e fecha os modais preparando os formulários correspondentes
  function openServicoDialog(item = null) {
    prepareServicoForm(item)
    servicoDialog.value = true
  }

  function closeServicoDialog() {
    servicoDialog.value = false
  }

  function openMaterialDialog(item = null) {
    prepareMaterialForm(item)
    materialDialog.value = true
  }

  function closeMaterialDialog() {
    materialDialog.value = false
  }

  function openEquipamentoDialog(item = null) {
    prepareEquipamentoForm(item)
    equipamentoDialog.value = true
  }

  function closeEquipamentoDialog() {
    equipamentoDialog.value = false
  }

  // valida e salva ou atualiza um serviço no catálogo
  async function saveServico() {
    if (servicoFormRef.value) {
      const { valid } = await servicoFormRef.value.validate()
      if (!valid) return false
    }

    saving.value = true
    const isEdit = Boolean(servicoForm.value.id)
    const { id, ...dadosServico } = servicoForm.value
    try {
      if (isEdit) {
        await atualizarServico(id, dadosServico)
      } else {
        await criarServico(dadosServico)
      }
      if (showMessage) {
        showMessage(`Serviço ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      }
      await fetchAllData()
      servicoDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar serviço', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  // valida e salva ou atualiza um material e vincula ao serviço caso o modal de serviço esteja aberto
  async function saveMaterial(vincularAoServicoAberto = servicoDialog.value) {
    if (materialFormRef.value) {
      const { valid } = await materialFormRef.value.validate()
      if (!valid) return false
    }

    saving.value = true
    const isEdit = Boolean(materialForm.value.id)
    const { id, ...dadosMaterial } = materialForm.value
    try {
      const data = isEdit
        ? await atualizarMaterial(id, dadosMaterial)
        : await criarMaterial(dadosMaterial)

      if (showMessage) {
        showMessage(`Material ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      }
      await fetchAllData()

      if (vincularAoServicoAberto && !isEdit && data && data.id) {
        servicoForm.value.materiais_ids.push(data.id)
      }
      materialDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar material', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  // valida e salva ou atualiza um equipamento e vincula ao serviço caso o modal de serviço esteja aberto
  async function saveEquipamento(vincularAoServicoAberto = servicoDialog.value) {
    if (equipamentoFormRef.value) {
      const { valid } = await equipamentoFormRef.value.validate()
      if (!valid) return false
    }

    saving.value = true
    const isEdit = Boolean(equipamentoForm.value.id)
    const { id, ...dadosEquipamento } = equipamentoForm.value
    try {
      const data = isEdit
        ? await atualizarEquipamento(id, dadosEquipamento)
        : await criarEquipamento(dadosEquipamento)

      if (showMessage) {
        showMessage(`Equipamento ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      }
      await fetchAllData()

      if (vincularAoServicoAberto && !isEdit && data && data.id) {
        servicoForm.value.equipamentos_ids.push(data.id)
      }
      equipamentoDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar equipamento', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  // ajusta rapidamente a quantidade (+ / -) de um material ou equipamento
  async function adjustQuantity(tipoRecurso, item, delta) {
    const novaQtd = Math.max(0, (item.quantidade || 0) + delta)
    const novoDisponivel = novaQtd > 0 ? item.disponivel : false
    const payload = { quantidade: novaQtd, disponivel: novoDisponivel }

    try {
      if (tipoRecurso === 'materiais') {
        await atualizarMaterial(item.id, payload)
      } else {
        await atualizarEquipamento(item.id, payload)
      }
      await fetchAllData()
    } catch (error) {
      if (showMessage) {
        showMessage('Erro ao atualizar quantidade', 'error')
      }
    }
  }

  // alterna rapidamente a disponibilidade de um material ou equipamento na tabela
  async function toggleAvailability(tipoRecurso, item) {
    const novoStatus = !item.disponivel
    const novaQtd = novoStatus && item.quantidade === 0 ? 1 : item.quantidade
    const payload = { disponivel: novoStatus, quantidade: novaQtd }

    try {
      if (tipoRecurso === 'materiais') {
        await atualizarMaterial(item.id, payload)
      } else {
        await atualizarEquipamento(item.id, payload)
      }
      await fetchAllData()
      if (showMessage) {
        showMessage('Disponibilidade atualizada!')
      }
    } catch (error) {
      if (showMessage) {
        showMessage('Erro ao alternar disponibilidade', 'error')
      }
    }
  }

  // exclui um registro (serviço, material ou equipamento) de forma unificada
  async function deleteRegistro(type, id) {
    saving.value = true
    try {
      if (type === 'servico') {
        await excluirServico(id)
      } else if (type === 'material') {
        await excluirMaterial(id)
      } else if (type === 'equipamento') {
        await excluirEquipamento(id)
      }

      if (showMessage) {
        showMessage('Registro excluído com sucesso!')
      }
      await fetchAllData()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao excluir registro', 'error')
      }
      return false
    } finally {
      saving.value = false
    }
  }

  // abre o modal de confirmação de exclusão para o item selecionado
  function confirmDelete(type, item) {
    deleteTarget.value = { type, id: item.id, nome: item.nome }
    deleteDialog.value = true
  }

  function closeDeleteDialog() {
    deleteDialog.value = false
  }

  // executa a exclusão confirmada no modal e fecha o diálogo em caso de sucesso
  async function executeDelete() {
    const sucesso = await deleteRegistro(deleteTarget.value.type, deleteTarget.value.id)
    if (sucesso) {
      deleteDialog.value = false
    }
    return sucesso
  }

  return {
    loading,
    saving,
    servicos,
    materiais,
    equipamentos,
    activeTab,
    servicoDialog,
    servicoValid,
    servicoFormRef,
    materialDialog,
    materialValid,
    materialFormRef,
    equipamentoDialog,
    equipamentoValid,
    equipamentoFormRef,
    deleteDialog,
    deleteTarget,
    servicoForm,
    materialForm,
    equipamentoForm,
    servicoFormTitle,
    materialFormTitle,
    equipamentoFormTitle,
    servicoNomeRules,
    servicoDuracaoRules,
    materialNomeRules,
    equipamentoNomeRules,
    servicosComFalta,
    materiaisEmFalta,
    equipamentosIndisponiveis,
    recursosFaltantesNoFormulario,
    aoAlterarQuantidadeMaterial,
    aoAlterarQuantidadeEquipamento,
    fetchAllData,
    prepareServicoForm,
    prepareMaterialForm,
    prepareEquipamentoForm,
    openServicoDialog,
    closeServicoDialog,
    openMaterialDialog,
    closeMaterialDialog,
    openEquipamentoDialog,
    closeEquipamentoDialog,
    saveServico,
    saveMaterial,
    saveEquipamento,
    adjustQuantity,
    toggleAvailability,
    deleteRegistro,
    confirmDelete,
    closeDeleteDialog,
    executeDelete,
  }
}
