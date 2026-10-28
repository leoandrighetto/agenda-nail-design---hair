/**
 * Composable responsável pelo controle financeiro de cursos e matrículas,
 * incluindo lançamentos de cobranças, filtros e fluxo de baixa rápida de pagamento.
 */
import { ref, computed } from 'vue'
import {
  listarPagamentos,
  criarPagamento,
  atualizarPagamento,
  excluirPagamento,
} from '@/services/cursos/pagamentosService'

export function usePagamentosCurso(showMessage, matriculasRef) {
  const loadingPagamentos = ref(false)
  const savingPagamento = ref(false)

  const pagamentos = ref([])
  const buscaPagamento = ref('')
  const filtroStatusPagamento = ref('TODOS')

  // estados dos modais de lançamento financeiro e de baixa rápida
  const pagamentoDialog = ref(false)
  const pagamentoValid = ref(false)
  const pagamentoFormRef = ref(null)

  const baixaDialog = ref(false)
  const baixaValid = ref(false)
  const baixaFormRef = ref(null)
  const pagamentoEmBaixa = ref(null)

  const hojeIso = new Date().toISOString().split('T')[0]

  const defaultPagamento = {
    id: null,
    matricula_id: null,
    aluno_id: null,
    curso_id: null,
    tipo_cobranca: 'MENSALIDADE',
    status: 'PENDENTE',
    valor_esperado: null,
    valor_pago: null,
    data_vencimento: hojeIso,
    data_pagamento: '',
    forma_pagamento: null,
  }
  const pagamentoForm = ref({ ...defaultPagamento })

  const baixaForm = ref({
    forma_pagamento: 'PIX',
    valor_pago: null,
    data_pagamento: hojeIso,
  })

  const pagamentoFormTitle = computed(() =>
    pagamentoForm.value.id ? 'Editar Cobrança / Pagamento' : 'Nova Cobrança de Curso'
  )

  const obrigatorioRule = [(v) => (v !== null && v !== undefined && v !== '') || 'Campo obrigatório']
  const valorPositivoRule = [
    (v) => (v !== null && v !== '' && Number(v) >= 0) || 'Informe um valor válido',
  ]

  // listagem filtrada de pagamentos considerando atraso automático
  const pagamentosFiltrados = computed(() => {
    const termo = String(buscaPagamento.value || '').trim().toLowerCase()
    return pagamentos.value.filter((p) => {
      const statusEfetivo = p.status === 'PENDENTE' && p.em_atraso ? 'ATRASADO' : p.status
      if (filtroStatusPagamento.value !== 'TODOS' && statusEfetivo !== filtroStatusPagamento.value) {
        return false
      }
      if (!termo) return true
      return (
        String(p.aluno_nome || '').toLowerCase().includes(termo) ||
        String(p.curso_nome || '').toLowerCase().includes(termo) ||
        String(p.tipo_cobranca || '').toLowerCase().includes(termo)
      )
    })
  })

  // indicadores financeiros computados (KPIs)
  const totalRecebidoCursos = computed(() => {
    return pagamentos.value
      .filter((p) => p.status === 'PAGO')
      .reduce((soma, p) => soma + Number(p.valor_pago ?? p.valor_esperado ?? 0), 0)
  })

  const totalPendenteCursos = computed(() => {
    return pagamentos.value
      .filter((p) => p.status === 'PENDENTE' || p.status === 'ATRASADO')
      .reduce((soma, p) => soma + Number(p.valor_esperado || 0), 0)
  })

  const cobrançasEmAtrasoCount = computed(() => {
    return pagamentos.value.filter(
      (p) => p.status === 'ATRASADO' || (p.status === 'PENDENTE' && p.em_atraso)
    ).length
  })

  // preenche aluno, curso e valor esperado ao selecionar uma matrícula existente no formulário
  function aoSelecionarMatriculaNoPagamento(matriculaId) {
    if (!matriculaId) return
    const mat = (matriculasRef?.value || []).find((m) => m.id === matriculaId)
    if (mat) {
      pagamentoForm.value.aluno_id = mat.aluno_id
      pagamentoForm.value.curso_id = mat.curso_id
      if (!pagamentoForm.value.id && !pagamentoForm.value.valor_esperado) {
        pagamentoForm.value.valor_esperado = mat.valor_acordado
      }
    }
  }

  // carrega todos os pagamentos do backend
  async function fetchPagamentos() {
    loadingPagamentos.value = true
    try {
      pagamentos.value = await listarPagamentos()
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao carregar pagamentos de cursos', 'error')
      }
    } finally {
      loadingPagamentos.value = false
    }
  }

  // abre o modal de criação ou edição de pagamento (suporta pré-seleção vinda da aba de matrículas)
  function openPagamentoDialog(item = null, preSelecionar = {}) {
    if (item) {
      pagamentoForm.value = {
        id: item.id,
        matricula_id: item.matricula_id || null,
        aluno_id: item.aluno_id,
        curso_id: item.curso_id,
        tipo_cobranca: item.tipo_cobranca || 'MENSALIDADE',
        status: item.status || 'PENDENTE',
        valor_esperado: item.valor_esperado,
        valor_pago: item.valor_pago,
        data_vencimento: item.data_vencimento || hojeIso,
        data_pagamento: item.data_pagamento || '',
        forma_pagamento: item.forma_pagamento || null,
      }
    } else {
      pagamentoForm.value = {
        ...defaultPagamento,
        matricula_id: preSelecionar.matricula_id || null,
        aluno_id: preSelecionar.aluno_id || null,
        curso_id: preSelecionar.curso_id || null,
        valor_esperado: preSelecionar.valor_esperado ?? null,
      }
    }
    pagamentoDialog.value = true
  }

  function closePagamentoDialog() {
    pagamentoDialog.value = false
  }

  // abre o modal rápido para dar baixa (receber) em uma cobrança pendente ou atrasada
  function openBaixaDialog(pagamento) {
    pagamentoEmBaixa.value = pagamento
    baixaForm.value = {
      forma_pagamento: pagamento.forma_pagamento || 'PIX',
      valor_pago: pagamento.valor_pago ?? pagamento.valor_esperado,
      data_pagamento: pagamento.data_pagamento || hojeIso,
    }
    baixaDialog.value = true
  }

  function closeBaixaDialog() {
    baixaDialog.value = false
    pagamentoEmBaixa.value = null
  }

  // valida e salva ou atualiza um lançamento financeiro completo
  async function savePagamento() {
    if (pagamentoFormRef.value) {
      const { valid } = await pagamentoFormRef.value.validate()
      if (!valid) return false
    }

    savingPagamento.value = true
    const isEdit = Boolean(pagamentoForm.value.id)
    const ehPago = pagamentoForm.value.status === 'PAGO'
    const payload = {
      matricula_id: pagamentoForm.value.matricula_id || null,
      aluno_id: pagamentoForm.value.aluno_id,
      curso_id: pagamentoForm.value.curso_id,
      tipo_cobranca: pagamentoForm.value.tipo_cobranca,
      status: pagamentoForm.value.status,
      valor_esperado: Number(pagamentoForm.value.valor_esperado),
      valor_pago:
        pagamentoForm.value.valor_pago !== null && pagamentoForm.value.valor_pago !== ''
          ? Number(pagamentoForm.value.valor_pago)
          : ehPago
            ? Number(pagamentoForm.value.valor_esperado)
            : null,
      data_vencimento: pagamentoForm.value.data_vencimento,
      data_pagamento: pagamentoForm.value.data_pagamento || (ehPago ? hojeIso : null),
      forma_pagamento: pagamentoForm.value.forma_pagamento || null,
    }

    try {
      if (isEdit) {
        await atualizarPagamento(pagamentoForm.value.id, payload)
      } else {
        await criarPagamento(payload)
      }
      if (showMessage) {
        showMessage(`Cobrança ${isEdit ? 'atualizada' : 'registrada'} com sucesso!`)
      }
      await fetchPagamentos()
      pagamentoDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar cobrança', 'error')
      }
      return false
    } finally {
      savingPagamento.value = false
    }
  }

  // confirma a baixa rápida marcando a cobrança como PAGO
  async function confirmarBaixaPagamento() {
    if (!pagamentoEmBaixa.value) return false
    if (baixaFormRef.value) {
      const { valid } = await baixaFormRef.value.validate()
      if (!valid) return false
    }

    savingPagamento.value = true
    try {
      await atualizarPagamento(pagamentoEmBaixa.value.id, {
        status: 'PAGO',
        forma_pagamento: baixaForm.value.forma_pagamento,
        valor_pago: Number(baixaForm.value.valor_pago),
        data_pagamento: baixaForm.value.data_pagamento || hojeIso,
      })
      if (showMessage) {
        showMessage('Pagamento recebido e baixado com sucesso!')
      }
      await fetchPagamentos()
      closeBaixaDialog()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao registrar baixa do pagamento', 'error')
      }
      return false
    } finally {
      savingPagamento.value = false
    }
  }

  // remove um pagamento pelo identificador
  async function removerPagamento(id) {
    savingPagamento.value = true
    try {
      await excluirPagamento(id)
      await fetchPagamentos()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao excluir pagamento', 'error')
      }
      return false
    } finally {
      savingPagamento.value = false
    }
  }

  return {
    loadingPagamentos,
    savingPagamento,
    pagamentos,
    buscaPagamento,
    filtroStatusPagamento,
    pagamentosFiltrados,
    totalRecebidoCursos,
    totalPendenteCursos,
    cobrançasEmAtrasoCount,
    pagamentoDialog,
    pagamentoValid,
    pagamentoFormRef,
    pagamentoForm,
    pagamentoFormTitle,
    baixaDialog,
    baixaValid,
    baixaFormRef,
    pagamentoEmBaixa,
    baixaForm,
    obrigatorioRule,
    valorPositivoRule,
    aoSelecionarMatriculaNoPagamento,
    fetchPagamentos,
    openPagamentoDialog,
    closePagamentoDialog,
    openBaixaDialog,
    closeBaixaDialog,
    savePagamento,
    confirmarBaixaPagamento,
    removerPagamento,
  }
}

