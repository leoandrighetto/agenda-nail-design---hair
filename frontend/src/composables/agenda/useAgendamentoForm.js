/**
 * Composable para manipulação do formulário de agendamento, controle de modais,
 * criação rápida de clientes/procedimentos, detecção de conflitos e persistência.
 */
import { ref, computed, nextTick } from 'vue'
import { somarMinutosNaHora } from '@/utils/shared/formatters'
import { useSelecaoProcedimentosModal } from '@/composables/agenda/useSelecaoProcedimentosModal'

export function useAgendamentoForm(store, hojeIso, mostrarMensagem) {
  const salvando = ref(false)
  const excluindo = ref(false)
  const atualizandoStatus = ref(null)

  // estados de visibilidade dos modais e referências de validação
  const detalheDialog = ref(false)
  const agendamentoSelecionado = ref(null)

  const agendamentoDialog = ref(false)
  const formValido = ref(false)
  const formRef = ref(null)

  const deleteDialog = ref(false)
  const agendamentoParaExcluir = ref(null)

  // controle dos modais rápidos de criação e estados de carregamento dos selects
  const modalNovoCliente = ref(false)
  const modalNovoProcedimento = ref(false)
  const carregandoClientes = ref(false)
  const carregandoProcedimentos = ref(false)

  const padraoForm = () => ({
    id: null,
    cliente_id: null,
    servicos_ids: [],
    data: hojeIso,
    hora_inicio: '09:00',
    hora_fim: '10:00',
    status: 'Confirmado',
  })

  const form = ref(padraoForm())

  const rules = {
    required: (v) => (v !== null && v !== undefined && v !== '') || 'Campo obrigatório',
    requiredArray: (v) =>
      (Array.isArray(v) && v.length > 0) || 'Selecione ao menos um procedimento',
  }

  // lista de serviços selecionados atualmente no formulário de criação/edição
  const servicosSelecionadosForm = computed(() => {
    if (
      !form.value.servicos_ids ||
      !Array.isArray(form.value.servicos_ids) ||
      form.value.servicos_ids.length === 0
    ) {
      return []
    }
    return store.servicos.filter((s) => form.value.servicos_ids.includes(s.id))
  })

  // primeiro serviço selecionado (mantido para compatibilidade)
  const servicoSelecionadoForm = computed(() => {
    return servicosSelecionadosForm.value[0] || null
  })

  // lista de serviços selecionados no formulário que possuem recursos em falta no estoque
  const servicosComRecursosEmFalta = computed(() => {
    return servicosSelecionadosForm.value.filter((s) => !s.recursos_disponiveis)
  })

  // soma da duração em minutos de todos os procedimentos selecionados
  const duracaoTotalMinutos = computed(() => {
    if (!servicosSelecionadosForm.value.length) return 30
    return servicosSelecionadosForm.value.reduce(
      (total, s) => total + (Number(s.duracao_minutos) || 30),
      0
    )
  })

  // soma dos valores de todos os procedimentos selecionados
  const valorTotalEstimado = computed(() => {
    return servicosSelecionadosForm.value.reduce(
      (total, s) => total + (Number(s.preco) || 0),
      0
    )
  })

  // verifica se já existe outro agendamento ativo no mesmo intervalo de horário
  const conflitoHorario = computed(() => {
    if (!form.value.data || !form.value.hora_inicio || !form.value.hora_fim) return null

    return store.agendamentos.find((ag) => {
      if (ag.id === form.value.id) return false
      if (ag.status === 'Cancelado') return false
      if (ag.data !== form.value.data) return false

      const inicioNovo = form.value.hora_inicio
      const fimNovo = form.value.hora_fim
      const inicioExistente = ag.hora
      const fimExistente = ag.hora_fim || somarMinutosNaHora(ag.hora, 30)

      return inicioNovo < fimExistente && fimNovo > inicioExistente
    })
  })

  // objetos auxiliares para exibição detalhada no modal de visualização
  const clienteDetalhe = computed(() => {
    if (!agendamentoSelecionado.value) return null
    return store.clientes.find((c) => c.id === agendamentoSelecionado.value.cliente_id) || null
  })

  const servicoDetalhe = computed(() => {
    const ag = agendamentoSelecionado.value
    if (!ag) return null

    // coleta todos os serviços vinculados ao agendamento (múltiplos ou único) a partir do catálogo da store
    const idsVinculados =
      Array.isArray(ag.servicos) && ag.servicos.length > 0
        ? ag.servicos.map((s) => s.id)
        : ag.servico_id
          ? [ag.servico_id]
          : []

    const servicosCatalogo = idsVinculados
      .map((id) => store.servicos.find((s) => s.id === id) || ag.servicos?.find((s) => s.id === id))
      .filter(Boolean)

    if (servicosCatalogo.length === 0) return null
    if (servicosCatalogo.length === 1) return servicosCatalogo[0]

    // consolida disponibilidade e listas de recursos quando há múltiplos procedimentos no agendamento
    const todosDisponiveis = servicosCatalogo.every((s) => s.recursos_disponiveis !== false)
    const materiaisAgregados = servicosCatalogo.flatMap((s) => s.materiais || [])
    const equipamentosAgregados = servicosCatalogo.flatMap((s) => s.equipamentos || [])

    return {
      ...servicosCatalogo[0],
      recursos_disponiveis: todosDisponiveis,
      materiais: materiaisAgregados,
      equipamentos: equipamentosAgregados,
    }
  })

  // recalcula o horário de término com base na soma da duração de todos os serviços selecionados
  function recalcularHoraFim() {
    if (!form.value.hora_inicio) return
    form.value.hora_fim = somarMinutosNaHora(form.value.hora_inicio, duracaoTotalMinutos.value)
  }

  function aoSelecionarServico() {
    recalcularHoraFim()
  }

  // integra a seleção múltipla de procedimentos em modal
  const {
    modalSelecaoProcedimentos,
    procedimentosTempIds,
    termoBuscaProcedimentos,
    tentouSalvarSemProcedimento,
    procedimentosFiltradosModal,
    abrirModalSelecaoProcedimentos,
    alternarProcedimentoTemp,
    desmarcarTodosProcedimentosTemp,
    confirmarSelecaoProcedimentos,
    cancelarSelecaoProcedimentos,
    removerProcedimento,
    registrarProcedimentoCriado,
  } = useSelecaoProcedimentosModal(store, form, aoSelecionarServico)

  // prepara o formulário para um novo agendamento, opcionalmente recebendo a data clicada
  function iniciarNovoForm(dataPreSelecionada = null) {
    form.value = padraoForm()
    if (typeof dataPreSelecionada === 'string' && dataPreSelecionada) {
      form.value.data = dataPreSelecionada
    }
    recalcularHoraFim()
  }

  // preenche o formulário com os dados de um agendamento existente para edição
  function preencherFormEdicao(evento) {
    let ids = []
    if (evento.servicos && Array.isArray(evento.servicos) && evento.servicos.length > 0) {
      ids = evento.servicos.map((s) => s.id)
    } else if (evento.servicos_ids && Array.isArray(evento.servicos_ids)) {
      ids = evento.servicos_ids
    } else if (evento.servico_id) {
      ids = [evento.servico_id]
    }

    form.value = {
      id: evento.id,
      cliente_id: evento.cliente_id,
      servicos_ids: ids,
      data: evento.data,
      hora_inicio: evento.hora,
      hora_fim: evento.hora_fim || somarMinutosNaHora(evento.hora, 30),
      status: evento.status || 'Pendente',
    }

    if (!evento.hora_fim) {
      recalcularHoraFim()
    }
  }

  // abertura e transição entre os modais da agenda
  function abrirNovoAgendamento(dataPreSelecionada = null) {
    tentouSalvarSemProcedimento.value = false
    iniciarNovoForm(dataPreSelecionada)
    agendamentoDialog.value = true
  }

  function abrirDetalhesAgendamento(evento) {
    agendamentoSelecionado.value = evento
    detalheDialog.value = true
  }

  function abrirEdicaoAgendamento(evento) {
    detalheDialog.value = false
    preencherFormEdicao(evento)
    agendamentoDialog.value = true
  }

  function confirmarExclusao(evento) {
    agendamentoParaExcluir.value = evento
    detalheDialog.value = false
    deleteDialog.value = true
  }

  // recarrega clientes e seleciona automaticamente o cliente recém-cadastrado no modal rápido
  async function aoSalvarNovoCliente(clienteCriado) {
    carregandoClientes.value = true
    try {
      await store.fetchClientes()
      if (clienteCriado?.id) {
        form.value.cliente_id = clienteCriado.id
      }
      if (mostrarMensagem) {
        mostrarMensagem(`Cliente "${clienteCriado.nome}" cadastrado com sucesso!`)
      }
    } catch (err) {
      if (mostrarMensagem) {
        mostrarMensagem(err.message || 'Erro ao atualizar lista de clientes', 'error')
      }
    } finally {
      carregandoClientes.value = false
    }
  }

  // recarrega procedimentos e adiciona automaticamente o procedimento recém-cadastrado ao formulário
  async function aoSalvarNovoProcedimento(procedimentoCriado) {
    carregandoProcedimentos.value = true
    try {
      await store.fetchServicos()
      if (procedimentoCriado?.id) {
        registrarProcedimentoCriado(procedimentoCriado.id)
        if (!Array.isArray(form.value.servicos_ids)) {
          form.value.servicos_ids = []
        }
        if (!form.value.servicos_ids.includes(procedimentoCriado.id)) {
          form.value.servicos_ids.push(procedimentoCriado.id)
        }
        await nextTick()
        aoSelecionarServico()
      }
      if (mostrarMensagem) {
        mostrarMensagem(`Procedimento "${procedimentoCriado.nome}" cadastrado com sucesso!`)
      }
    } catch (err) {
      if (mostrarMensagem) {
        mostrarMensagem(err.message || 'Erro ao atualizar catálogo de procedimentos', 'error')
      }
    } finally {
      carregandoProcedimentos.value = false
    }
  }

  // valida e salva novo agendamento ou atualiza existente através da store
  async function salvarAgendamento() {
    if (!form.value.servicos_ids || !form.value.servicos_ids.length) {
      tentouSalvarSemProcedimento.value = true
      if (mostrarMensagem) {
        mostrarMensagem('Selecione ao menos um procedimento para o agendamento.', 'error')
      }
      return false
    }
    if (!formValido.value) return false

    salvando.value = true
    try {
      const payload = {
        cliente_id: form.value.cliente_id,
        servicos_ids: form.value.servicos_ids,
        servico_id: form.value.servicos_ids[0] || null,
        data_hora_inicio: `${form.value.data}T${form.value.hora_inicio}:00`,
        status: form.value.status,
        valor_total: valorTotalEstimado.value,
      }

      if (form.value.hora_fim) {
        payload.data_hora_fim = `${form.value.data}T${form.value.hora_fim}:00`
      }

      if (form.value.id) {
        await store.atualizarAgendamento(form.value.id, payload)
        if (mostrarMensagem) mostrarMensagem('Agendamento atualizado com sucesso!')
      } else {
        await store.criarAgendamento(payload)
        if (mostrarMensagem) mostrarMensagem('Agendamento registrado com sucesso!')
      }

      agendamentoDialog.value = false
      tentouSalvarSemProcedimento.value = false
      return true
    } catch (err) {
      if (mostrarMensagem) mostrarMensagem(err.message || 'Erro ao salvar agendamento', 'error')
      return false
    } finally {
      salvando.value = false
    }
  }

  // altera rapidamente o status de um agendamento e atualiza o registro em foco no modal
  async function alterarStatusRapido(novoStatus) {
    const agendamentoAtual = agendamentoSelecionado.value
    if (!agendamentoAtual || agendamentoAtual.status === novoStatus) return null
    atualizandoStatus.value = novoStatus

    try {
      await store.atualizarAgendamento(agendamentoAtual.id, {
        status: novoStatus,
      })
      const atualizado = store.agendamentos.find((a) => a.id === agendamentoAtual.id) || null
      if (atualizado) {
        agendamentoSelecionado.value = atualizado
      }
      if (mostrarMensagem) mostrarMensagem(`Status alterado para "${novoStatus}"!`)
      return atualizado
    } catch (err) {
      if (mostrarMensagem) mostrarMensagem(err.message || 'Erro ao alterar status', 'error')
      return null
    } finally {
      atualizandoStatus.value = null
    }
  }

  // exclui o agendamento selecionado através da store e fecha o modal de confirmação
  async function executarExclusao() {
    if (!agendamentoParaExcluir.value?.id) return false
    excluindo.value = true

    try {
      await store.deletarAgendamento(agendamentoParaExcluir.value.id)
      if (mostrarMensagem) mostrarMensagem('Agendamento excluído com sucesso!')
      deleteDialog.value = false
      agendamentoParaExcluir.value = null
      return true
    } catch (err) {
      if (mostrarMensagem) mostrarMensagem(err.message || 'Erro ao excluir agendamento', 'error')
      return false
    } finally {
      excluindo.value = false
    }
  }

  return {
    form,
    salvando,
    excluindo,
    atualizandoStatus,
    detalheDialog,
    agendamentoSelecionado,
    agendamentoDialog,
    formValido,
    formRef,
    deleteDialog,
    agendamentoParaExcluir,
    modalNovoCliente,
    modalNovoProcedimento,
    carregandoClientes,
    carregandoProcedimentos,
    modalSelecaoProcedimentos,
    procedimentosTempIds,
    termoBuscaProcedimentos,
    tentouSalvarSemProcedimento,
    procedimentosFiltradosModal,
    rules,
    servicoSelecionadoForm,
    servicosSelecionadosForm,
    servicosComRecursosEmFalta,
    duracaoTotalMinutos,
    valorTotalEstimado,
    conflitoHorario,
    clienteDetalhe,
    servicoDetalhe,
    recalcularHoraFim,
    aoSelecionarServico,
    iniciarNovoForm,
    preencherFormEdicao,
    abrirNovoAgendamento,
    abrirDetalhesAgendamento,
    abrirEdicaoAgendamento,
    confirmarExclusao,
    abrirModalSelecaoProcedimentos,
    alternarProcedimentoTemp,
    desmarcarTodosProcedimentosTemp,
    confirmarSelecaoProcedimentos,
    cancelarSelecaoProcedimentos,
    removerProcedimento,
    aoSalvarNovoCliente,
    aoSalvarNovoProcedimento,
    salvarAgendamento,
    alterarStatusRapido,
    executarExclusao,
  }
}
