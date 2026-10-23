/**
 * Composable para orquestração da seleção múltipla de procedimentos em modal com busca e checkboxes.
 */
import { ref, computed } from 'vue'

export function useSelecaoProcedimentosModal(store, form, aoSelecionarServico) {
  const modalSelecaoProcedimentos = ref(false)
  const procedimentosTempIds = ref([])
  const termoBuscaProcedimentos = ref('')
  const tentouSalvarSemProcedimento = ref(false)

  // procedimentos filtrados dinamicamente pela barra de pesquisa do modal
  const procedimentosFiltradosModal = computed(() => {
    if (!termoBuscaProcedimentos.value) return store.servicos
    const termo = termoBuscaProcedimentos.value.toLowerCase().trim()
    return store.servicos.filter((s) => s.nome && s.nome.toLowerCase().includes(termo))
  })

  // abre o modal de procedimentos copiando o estado atual já selecionado
  function abrirModalSelecaoProcedimentos() {
    procedimentosTempIds.value = [...(form.value.servicos_ids || [])]
    termoBuscaProcedimentos.value = ''
    modalSelecaoProcedimentos.value = true
  }

  // alterna a marcação do checkbox de um procedimento na lista temporária
  function alternarProcedimentoTemp(id) {
    const index = procedimentosTempIds.value.indexOf(id)
    if (index > -1) {
      procedimentosTempIds.value.splice(index, 1)
    } else {
      procedimentosTempIds.value.push(id)
    }
  }

  // desmarca todos os procedimentos da lista temporária do modal
  function desmarcarTodosProcedimentosTemp() {
    procedimentosTempIds.value = []
  }

  // confirma a seleção e transfere para o formulário
  function confirmarSelecaoProcedimentos() {
    form.value.servicos_ids = [...procedimentosTempIds.value]
    if (aoSelecionarServico) aoSelecionarServico()
    tentouSalvarSemProcedimento.value = false
    modalSelecaoProcedimentos.value = false
  }

  // cancela a seleção descartando alterações temporárias
  function cancelarSelecaoProcedimentos() {
    modalSelecaoProcedimentos.value = false
  }

  // remove um procedimento diretamente ao clicar no botão fechar do chip
  function removerProcedimento(id) {
    const index = form.value.servicos_ids.indexOf(id)
    if (index > -1) {
      form.value.servicos_ids.splice(index, 1)
      if (aoSelecionarServico) aoSelecionarServico()
    }
  }

  // sincroniza procedimento recém-criado na lista temporária se o modal estiver aberto
  function registrarProcedimentoCriado(novoId) {
    if (modalSelecaoProcedimentos.value) {
      if (!procedimentosTempIds.value.includes(novoId)) {
        procedimentosTempIds.value.push(novoId)
      }
    }
  }

  return {
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
  }
}

