/**
 * Composable responsável pelo gerenciamento do catálogo de cursos, modalidades de ensino,
 * vínculo com materiais e equipamentos do estoque, validações e modais.
 */
import { ref, computed } from 'vue'
import {
  listarCursos,
  criarCurso,
  atualizarCurso,
  excluirCurso,
} from '@/services/cursos/cursosService'
import {
  listarModalidades,
  criarModalidade,
  atualizarModalidade,
  excluirModalidade,
} from '@/services/cursos/modalidadesService'
import { listarMateriais } from '@/services/estoque/materiaisService'
import { listarEquipamentos } from '@/services/estoque/equipamentosService'
import { isResourceAvailable } from '@/utils/estoque/estoqueUtils'

export function useCursosModalidades(showMessage) {
  const loadingCursos = ref(false)
  const savingCursoModalidade = ref(false)

  const cursos = ref([])
  const modalidades = ref([])
  const materiais = ref([])
  const equipamentos = ref([])

  // filtros de busca textual nas tabelas
  const buscaCurso = ref('')
  const buscaModalidade = ref('')

  // estados dos modais e referências de validação dos formulários
  const cursoDialog = ref(false)
  const cursoValid = ref(false)
  const cursoFormRef = ref(null)

  const modalidadeDialog = ref(false)
  const modalidadeValid = ref(false)
  const modalidadeFormRef = ref(null)

  const defaultCurso = {
    id: null,
    nome: '',
    numero_aulas: 10,
    duracao_no_dia: '4 horas',
    carga_horaria_total: 40,
    horas_realizadas: 0,
    valor_total: null,
    ativo: true,
    modalidades_ids: [],
  }
  const cursoForm = ref({ ...defaultCurso })

  const defaultModalidade = {
    id: null,
    nome: '',
    duracao: '',
    caracteristicas: '',
    materiais_ids: [],
    equipamentos_ids: [],
  }
  const modalidadeForm = ref({ ...defaultModalidade })

  // títulos dinâmicos dos modais de criação e edição
  const cursoFormTitle = computed(() =>
    cursoForm.value.id ? 'Editar Curso' : 'Novo Curso'
  )
  const modalidadeFormTitle = computed(() =>
    modalidadeForm.value.id ? 'Editar Modalidade' : 'Nova Modalidade'
  )

  // regras de validação dos formulários de curso e modalidade
  const cursoNomeRules = [
    (v) => !!(v && String(v).trim()) || 'O nome do curso é obrigatório',
  ]
  const numeroAulasRules = [
    (v) => (v !== null && v !== '' && Number(v) > 0) || 'Informe o número de aulas',
  ]
  const cargaHorariaRules = [
    (v) => (v !== null && v !== '' && Number(v) > 0) || 'Informe a carga horária total (h)',
  ]
  const valorCursoRules = [
    (v) => (v !== null && v !== '' && Number(v) >= 0) || 'Informe o valor total do curso',
  ]
  const modalidadeNomeRules = [
    (v) => !!(v && String(v).trim()) || 'O nome da modalidade é obrigatório',
  ]

  // listas filtradas por termo de busca
  const cursosFiltrados = computed(() => {
    const termo = String(buscaCurso.value || '').trim().toLowerCase()
    if (!termo) return cursos.value
    return cursos.value.filter((c) => {
      const nomeMatch = String(c.nome || '').toLowerCase().includes(termo)
      const modMatch = (c.modalidades || []).some((m) =>
        String(m.nome || '').toLowerCase().includes(termo)
      )
      return nomeMatch || modMatch
    })
  })

  const modalidadesFiltradas = computed(() => {
    const termo = String(buscaModalidade.value || '').trim().toLowerCase()
    if (!termo) return modalidades.value
    return modalidades.value.filter(
      (m) =>
        String(m.nome || '').toLowerCase().includes(termo) ||
        String(m.caracteristicas || '').toLowerCase().includes(termo)
    )
  })

  // indicadores computados (KPIs de cursos e recursos de ensino)
  const cursosAtivosCount = computed(() => {
    return cursos.value.filter((c) => c.ativo).length
  })

  const modalidadesComFaltaCount = computed(() => {
    return modalidades.value.filter((m) => !m.recursos_disponiveis).length
  })

  // verifica em tempo real no formulário de modalidade se algum recurso selecionado está em falta no estoque
  const recursosFaltantesNaModalidade = computed(() => {
    const faltantes = []
    for (const id of modalidadeForm.value.materiais_ids || []) {
      const mat = materiais.value.find((m) => m.id === id)
      if (mat && !isResourceAvailable(mat)) {
        faltantes.push(`${mat.nome} (Material)`)
      }
    }
    for (const id of modalidadeForm.value.equipamentos_ids || []) {
      const eq = equipamentos.value.find((e) => e.id === id)
      if (eq && !isResourceAvailable(eq)) {
        faltantes.push(`${eq.nome} (Equipamento)`)
      }
    }
    return faltantes
  })

  // carrega cursos, modalidades, materiais e equipamentos em paralelo
  async function fetchCursosEModalidades() {
    loadingCursos.value = true
    try {
      const [listaCursos, listaMods, listaMat, listaEq] = await Promise.all([
        listarCursos(),
        listarModalidades(),
        listarMateriais(),
        listarEquipamentos(),
      ])
      cursos.value = listaCursos
      modalidades.value = listaMods
      materiais.value = listaMat
      equipamentos.value = listaEq
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao carregar dados de cursos e modalidades', 'error')
      }
    } finally {
      loadingCursos.value = false
    }
  }

  // prepara e abre o modal de criação ou edição de curso
  function openCursoDialog(item = null) {
    if (item) {
      cursoForm.value = {
        id: item.id,
        nome: item.nome,
        numero_aulas: item.numero_aulas ?? 10,
        duracao_no_dia: item.duracao_no_dia || '',
        carga_horaria_total: item.carga_horaria_total ?? 40,
        horas_realizadas: item.horas_realizadas ?? 0,
        valor_total: item.valor_total,
        ativo: Boolean(item.ativo),
        modalidades_ids: (item.modalidades || []).map((m) => m.id),
      }
    } else {
      cursoForm.value = { ...defaultCurso, modalidades_ids: [] }
    }
    cursoDialog.value = true
  }

  function closeCursoDialog() {
    cursoDialog.value = false
  }

  // prepara e abre o modal de criação ou edição de modalidade
  function openModalidadeDialog(item = null) {
    if (item) {
      modalidadeForm.value = {
        id: item.id,
        nome: item.nome,
        duracao: item.duracao || '',
        caracteristicas: item.caracteristicas || '',
        materiais_ids: (item.materiais || []).map((m) => m.id),
        equipamentos_ids: (item.equipamentos || []).map((e) => e.id),
      }
    } else {
      modalidadeForm.value = {
        ...defaultModalidade,
        materiais_ids: [],
        equipamentos_ids: [],
      }
    }
    modalidadeDialog.value = true
  }

  function closeModalidadeDialog() {
    modalidadeDialog.value = false
  }

  // valida e salva ou atualiza um curso no catálogo
  async function saveCurso() {
    if (cursoFormRef.value) {
      const { valid } = await cursoFormRef.value.validate()
      if (!valid) return false
    }

    savingCursoModalidade.value = true
    const isEdit = Boolean(cursoForm.value.id)
    const payload = {
      nome: String(cursoForm.value.nome || '').trim(),
      numero_aulas: Number(cursoForm.value.numero_aulas),
      duracao_no_dia: String(cursoForm.value.duracao_no_dia || '').trim() || null,
      carga_horaria_total: Number(cursoForm.value.carga_horaria_total),
      horas_realizadas: Number(cursoForm.value.horas_realizadas || 0),
      valor_total: Number(cursoForm.value.valor_total),
      ativo: Boolean(cursoForm.value.ativo),
      modalidades_ids: cursoForm.value.modalidades_ids || [],
    }

    try {
      if (isEdit) {
        await atualizarCurso(cursoForm.value.id, payload)
      } else {
        await criarCurso(payload)
      }
      if (showMessage) {
        showMessage(`Curso ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      }
      await fetchCursosEModalidades()
      cursoDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar curso', 'error')
      }
      return false
    } finally {
      savingCursoModalidade.value = false
    }
  }

  // alterna rapidamente o status ativo/inativo de um curso na listagem
  async function toggleCursoAtivo(curso) {
    try {
      await atualizarCurso(curso.id, { ativo: !curso.ativo })
      await fetchCursosEModalidades()
      if (showMessage) {
        showMessage(`Curso "${curso.nome}" ${!curso.ativo ? 'ativado' : 'inativado'}!`)
      }
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao alterar status do curso', 'error')
      }
    }
  }

  // valida e salva ou atualiza uma modalidade e a vincula automaticamente se o modal de curso estiver aberto
  async function saveModalidade(vincularAoCursoAberto = cursoDialog.value) {
    if (modalidadeFormRef.value) {
      const { valid } = await modalidadeFormRef.value.validate()
      if (!valid) return false
    }

    savingCursoModalidade.value = true
    const isEdit = Boolean(modalidadeForm.value.id)
    const payload = {
      nome: String(modalidadeForm.value.nome || '').trim(),
      duracao: String(modalidadeForm.value.duracao || '').trim() || null,
      caracteristicas: String(modalidadeForm.value.caracteristicas || '').trim() || null,
      materiais_ids: modalidadeForm.value.materiais_ids || [],
      equipamentos_ids: modalidadeForm.value.equipamentos_ids || [],
    }

    try {
      const data = isEdit
        ? await atualizarModalidade(modalidadeForm.value.id, payload)
        : await criarModalidade(payload)

      if (showMessage) {
        showMessage(`Modalidade ${isEdit ? 'atualizada' : 'cadastrada'} com sucesso!`)
      }
      await fetchCursosEModalidades()

      if (vincularAoCursoAberto && !isEdit && data?.id) {
        if (!cursoForm.value.modalidades_ids.includes(data.id)) {
          cursoForm.value.modalidades_ids.push(data.id)
        }
      }
      modalidadeDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar modalidade', 'error')
      }
      return false
    } finally {
      savingCursoModalidade.value = false
    }
  }

  // exclui um curso ou modalidade pelo identificador
  async function removerCursoOuModalidade(tipo, id) {
    savingCursoModalidade.value = true
    try {
      if (tipo === 'curso') {
        await excluirCurso(id)
      } else if (tipo === 'modalidade') {
        await excluirModalidade(id)
      }
      await fetchCursosEModalidades()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao excluir registro', 'error')
      }
      return false
    } finally {
      savingCursoModalidade.value = false
    }
  }

  return {
    loadingCursos,
    savingCursoModalidade,
    cursos,
    modalidades,
    materiais,
    equipamentos,
    buscaCurso,
    buscaModalidade,
    cursosFiltrados,
    modalidadesFiltradas,
    cursoDialog,
    cursoValid,
    cursoFormRef,
    cursoForm,
    cursoFormTitle,
    modalidadeDialog,
    modalidadeValid,
    modalidadeFormRef,
    modalidadeForm,
    modalidadeFormTitle,
    cursoNomeRules,
    numeroAulasRules,
    cargaHorariaRules,
    valorCursoRules,
    modalidadeNomeRules,
    cursosAtivosCount,
    modalidadesComFaltaCount,
    recursosFaltantesNaModalidade,
    fetchCursosEModalidades,
    openCursoDialog,
    closeCursoDialog,
    openModalidadeDialog,
    closeModalidadeDialog,
    saveCurso,
    toggleCursoAtivo,
    saveModalidade,
    removerCursoOuModalidade,
  }
}

