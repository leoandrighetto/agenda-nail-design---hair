/**
 * Composable para manipulação do formulário de agendamento, detecção de conflitos de horário e ações de persistência.
 */
import { ref, computed } from 'vue'
import { somarMinutosNaHora } from '@/utils/shared/formatters'

export function useAgendamentoForm(store, hojeIso, mostrarMensagem) {
  const salvando = ref(false)
  const excluindo = ref(false)
  const atualizandoStatus = ref(null)

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
    if (!form.value.servicos_ids || !Array.isArray(form.value.servicos_ids) || form.value.servicos_ids.length === 0) {
      return []
    }
    return store.servicos.filter((s) => form.value.servicos_ids.includes(s.id))
  })

  // primeiro serviço selecionado (mantido para compatibilidade)
  const servicoSelecionadoForm = computed(() => {
    return servicosSelecionadosForm.value[0] || null
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
      const fimExistente = ag.hora_fim || ag.hora

      return inicioNovo < fimExistente && fimNovo > inicioExistente
    })
  })

  // recalcula o horário de término com base na soma da duração de todos os serviços selecionados
  function recalcularHoraFim() {
    if (!form.value.hora_inicio) return
    form.value.hora_fim = somarMinutosNaHora(form.value.hora_inicio, duracaoTotalMinutos.value)
  }

  function aoSelecionarServico() {
    recalcularHoraFim()
  }

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

  // salva novo agendamento ou atualiza existente através da store
  async function salvarAgendamento() {
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
      return true
    } catch (err) {
      if (mostrarMensagem) mostrarMensagem(err.message || 'Erro ao salvar agendamento', 'error')
      return false
    } finally {
      salvando.value = false
    }
  }

  // altera rapidamente o status de um agendamento e retorna o registro atualizado
  async function alterarStatusRapido(agendamentoAtual, novoStatus) {
    if (!agendamentoAtual || agendamentoAtual.status === novoStatus) return null
    atualizandoStatus.value = novoStatus

    try {
      await store.atualizarAgendamento(agendamentoAtual.id, {
        status: novoStatus,
      })
      const atualizado = store.agendamentos.find((a) => a.id === agendamentoAtual.id) || null
      if (mostrarMensagem) mostrarMensagem(`Status alterado para "${novoStatus}"!`)
      return atualizado
    } catch (err) {
      if (mostrarMensagem) mostrarMensagem(err.message || 'Erro ao alterar status', 'error')
      return null
    } finally {
      atualizandoStatus.value = null
    }
  }

  // exclui um agendamento pelo identificador através da store
  async function executarExclusao(agendamentoId) {
    if (!agendamentoId) return false
    excluindo.value = true

    try {
      await store.deletarAgendamento(agendamentoId)
      if (mostrarMensagem) mostrarMensagem('Agendamento excluído com sucesso!')
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
    rules,
    servicoSelecionadoForm,
    servicosSelecionadosForm,
    duracaoTotalMinutos,
    valorTotalEstimado,
    conflitoHorario,
    recalcularHoraFim,
    aoSelecionarServico,
    iniciarNovoForm,
    preencherFormEdicao,
    salvarAgendamento,
    alterarStatusRapido,
    executarExclusao,
  }
}
