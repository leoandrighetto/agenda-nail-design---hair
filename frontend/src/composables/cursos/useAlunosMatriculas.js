/**
 * Composable responsável pela gestão de alunos (Pessoa com eh_aluno=True),
 * matrículas em cursos, evolução de horas cumpridas e integração com clientes existentes.
 */
import { ref, computed } from 'vue'
import {
  listarAlunos,
  criarAluno,
  atualizarAluno,
  excluirAluno,
} from '@/services/cursos/alunosService'
import {
  listarMatriculas,
  criarMatricula,
  atualizarMatricula,
  excluirMatricula,
} from '@/services/cursos/matriculasService'
import { listarClientes } from '@/services/clientes/clientesService'
import { formatPhone, formatCPF } from '@/utils/shared/formatters'

export function useAlunosMatriculas(showMessage, cursosRef, aoAtualizarDadosGerais = null, resetAddressSearch = null) {
  const loadingAlunosMatriculas = ref(false)
  const savingAlunoMatricula = ref(false)
  const atualizandoHorasId = ref(null)

  const alunos = ref([])
  const matriculas = ref([])
  const clientesCadastrados = ref([])

  // controle de visualização interna na aba de alunos & matrículas e filtros
  const subVisaoAlunos = ref('matriculas')
  const buscaMatricula = ref('')
  const filtroStatusMatricula = ref('TODOS')
  const buscaAluno = ref('')

  // estados dos modais de aluno e de matrícula
  const alunoDialog = ref(false)
  const alunoValid = ref(false)
  const alunoFormRef = ref(null)
  const clienteImportadoId = ref(null)

  const matriculaDialog = ref(false)
  const matriculaValid = ref(false)
  const matriculaFormRef = ref(null)

  const hojeIso = new Date().toISOString().split('T')[0]

  const defaultAluno = {
    id: null,
    pessoa_id: null,
    nome: '',
    telefone: '',
    cpf: '',
    email: '',
    endereco: '',
    matricula: '',
    eh_cliente: false,
  }
  const alunoForm = ref({ ...defaultAluno })

  const defaultMatricula = {
    id: null,
    aluno_id: null,
    curso_id: null,
    valor_acordado: null,
    horas_realizadas: 0,
    status: 'EM_ANDAMENTO',
    data_matricula: hojeIso,
    data_conclusao: '',
    observacoes: '',
  }
  const matriculaForm = ref({ ...defaultMatricula })

  const alunoFormTitle = computed(() =>
    alunoForm.value.id ? 'Editar Aluno' : 'Novo Aluno'
  )
  const matriculaFormTitle = computed(() =>
    matriculaForm.value.id ? 'Editar Matrícula' : 'Nova Matrícula'
  )

  // regras de validação para cadastro de aluno e matrícula
  const nomeRules = [
    (v) => !!(v && String(v).trim()) || 'Nome é obrigatório',
    (v) =>
      /^[a-zA-ZÀ-ÿ\s'-]+$/.test(String(v || '').trim()) ||
      'Nome deve conter apenas letras e espaços',
  ]
  const telefoneRules = [
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
  const cpfRules = [
    (v) => !v || String(v).replace(/\D/g, '').length === 11 || 'CPF deve ter 11 dígitos',
  ]
  const emailRules = [
    (v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v).trim()) || 'E-mail inválido',
  ]
  const obrigatorioRule = [(v) => (v !== null && v !== undefined && v !== '') || 'Campo obrigatório']
  const valorAcordadoRules = [
    (v) => (v !== null && v !== '' && Number(v) >= 0) || 'Informe o valor acordado',
  ]

  // clientes que ainda não possuem o papel de aluno ativo, disponíveis para importação rápida
  const clientesDisponiveisParaImportar = computed(() => {
    const idsAlunos = new Set(alunos.value.map((a) => a.id))
    return clientesCadastrados.value.filter((c) => !c.eh_aluno && !idsAlunos.has(c.id))
  })

  // listas filtradas de matrículas e alunos
  const matriculasFiltradas = computed(() => {
    const termo = String(buscaMatricula.value || '').trim().toLowerCase()
    return matriculas.value.filter((m) => {
      if (filtroStatusMatricula.value !== 'TODOS' && m.status !== filtroStatusMatricula.value) {
        return false
      }
      if (!termo) return true
      return (
        String(m.aluno_nome || '').toLowerCase().includes(termo) ||
        String(m.aluno_matricula || '').toLowerCase().includes(termo) ||
        String(m.curso_nome || '').toLowerCase().includes(termo)
      )
    })
  })

  const alunosFiltrados = computed(() => {
    const termo = String(buscaAluno.value || '').trim().toLowerCase()
    if (!termo) return alunos.value
    return alunos.value.filter(
      (a) =>
        String(a.nome || '').toLowerCase().includes(termo) ||
        String(a.matricula || '').toLowerCase().includes(termo) ||
        String(a.telefone || '').toLowerCase().includes(termo) ||
        String(a.email || '').toLowerCase().includes(termo)
    )
  })

  // indicadores computados (KPIs de matrículas)
  const matriculasEmAndamentoCount = computed(() => {
    return matriculas.value.filter((m) => m.status === 'EM_ANDAMENTO').length
  })

  const matriculasConcluidasCount = computed(() => {
    return matriculas.value.filter((m) => m.status === 'CONCLUIDO').length
  })

  // máscaras durante digitação nos campos do aluno
  function aoAlterarTelefoneAluno(val) {
    alunoForm.value.telefone = formatPhone(val)
  }

  function aoAlterarCpfAluno(val) {
    alunoForm.value.cpf = formatCPF(val)
  }

  // preenche os dados do formulário de novo aluno a partir de um cliente já existente
  function aoSelecionarClienteExistente(clienteId) {
    clienteImportadoId.value = clienteId
    if (!clienteId) {
      alunoForm.value = { ...defaultAluno }
      return
    }
    const cliente = clientesCadastrados.value.find((c) => c.id === clienteId)
    if (cliente) {
      alunoForm.value = {
        ...defaultAluno,
        pessoa_id: cliente.id,
        nome: cliente.nome || '',
        telefone: formatPhone(cliente.telefone),
        cpf: formatCPF(cliente.cpf),
        email: cliente.email || '',
        endereco: cliente.endereco || '',
        matricula: cliente.matricula || '',
        eh_cliente: true,
      }
    }
  }

  // preenche automaticamente o valor acordado ao escolher um curso no modal de matrícula
  function aoSelecionarCursoMatricula(cursoId) {
    const listaCursos = cursosRef?.value || []
    const curso = listaCursos.find((c) => c.id === cursoId)
    if (curso && !matriculaForm.value.id) {
      matriculaForm.value.valor_acordado = curso.valor_total
    }
  }

  // carrega alunos, matrículas e clientes em paralelo
  async function fetchAlunosEMatriculas() {
    loadingAlunosMatriculas.value = true
    try {
      const [listaAlu, listaMat, listaCli] = await Promise.all([
        listarAlunos(),
        listarMatriculas(),
        listarClientes(),
      ])
      alunos.value = listaAlu.map((a) => ({
        ...a,
        telefone: formatPhone(a.telefone),
        cpf: formatCPF(a.cpf),
      }))
      matriculas.value = listaMat
      clientesCadastrados.value = listaCli
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao carregar alunos e matrículas', 'error')
      }
    } finally {
      loadingAlunosMatriculas.value = false
    }
  }

  // abertura e fechamento do modal de aluno
  function openAlunoDialog(item = null) {
    clienteImportadoId.value = null
    if (resetAddressSearch) resetAddressSearch()
    if (item) {
      alunoForm.value = {
        id: item.id,
        pessoa_id: item.id,
        nome: item.nome || '',
        telefone: formatPhone(item.telefone),
        cpf: formatCPF(item.cpf),
        email: item.email || '',
        endereco: item.endereco || '',
        matricula: item.matricula || '',
        eh_cliente: Boolean(item.eh_cliente),
      }
    } else {
      alunoForm.value = { ...defaultAluno }
    }
    alunoDialog.value = true
  }

  function closeAlunoDialog() {
    alunoDialog.value = false
    clienteImportadoId.value = null
    if (resetAddressSearch) resetAddressSearch()
  }

  // abertura e fechamento do modal de matrícula
  function openMatriculaDialog(item = null, preSelecionar = {}) {
    if (item) {
      matriculaForm.value = {
        id: item.id,
        aluno_id: item.aluno_id,
        curso_id: item.curso_id,
        valor_acordado: item.valor_acordado,
        horas_realizadas: item.horas_realizadas ?? 0,
        status: item.status || 'EM_ANDAMENTO',
        data_matricula: item.data_matricula || hojeIso,
        data_conclusao: item.data_conclusao || '',
        observacoes: item.observacoes || '',
      }
    } else {
      const cursoPre = (cursosRef?.value || []).find((c) => c.id === preSelecionar.curso_id)
      matriculaForm.value = {
        ...defaultMatricula,
        aluno_id: preSelecionar.aluno_id || null,
        curso_id: preSelecionar.curso_id || null,
        valor_acordado: cursoPre ? cursoPre.valor_total : null,
      }
    }
    matriculaDialog.value = true
  }

  function closeMatriculaDialog() {
    matriculaDialog.value = false
  }

  // valida e salva ou atualiza um aluno
  async function saveAluno() {
    if (alunoFormRef.value) {
      const { valid } = await alunoFormRef.value.validate()
      if (!valid) return false
    }

    savingAlunoMatricula.value = true
    const isEdit = Boolean(alunoForm.value.id)
    const addressVal = alunoForm.value.endereco
    const enderecoExtraido =
      typeof addressVal === 'object' && addressVal !== null
        ? addressVal.formatted_address || addressVal.display_name || ''
        : addressVal || ''

    const payload = {
      pessoa_id: alunoForm.value.pessoa_id || undefined,
      nome: String(alunoForm.value.nome || '').trim(),
      telefone: String(alunoForm.value.telefone || '').replace(/\D/g, ''),
      cpf: alunoForm.value.cpf ? String(alunoForm.value.cpf).replace(/\D/g, '') : null,
      email: alunoForm.value.email ? String(alunoForm.value.email).trim() : null,
      endereco: String(enderecoExtraido).trim() || null,
      matricula: String(alunoForm.value.matricula || '').trim() || undefined,
      eh_cliente: Boolean(alunoForm.value.eh_cliente),
      eh_aluno: true,
    }

    try {
      let resposta = null
      if (isEdit) {
        resposta = await atualizarAluno(alunoForm.value.id, payload)
      } else {
        resposta = await criarAluno(payload)
      }

      if (showMessage) {
        const msgCodigo = !isEdit && resposta?.matricula ? ` (Matrícula: ${resposta.matricula})` : ''
        showMessage(`Aluno ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!${msgCodigo}`)
      }
      await fetchAlunosEMatriculas()
      if (aoAtualizarDadosGerais) await aoAtualizarDadosGerais()

      // se o modal de matrícula estiver aberto, seleciona automaticamente o aluno recém-cadastrado
      if (matriculaDialog.value && !isEdit && resposta?.id) {
        matriculaForm.value.aluno_id = resposta.id
      }

      closeAlunoDialog()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar aluno', 'error')
      }
      return false
    } finally {
      savingAlunoMatricula.value = false
    }
  }

  // valida e salva ou atualiza uma matrícula de aluno em curso
  async function saveMatricula() {
    if (matriculaFormRef.value) {
      const { valid } = await matriculaFormRef.value.validate()
      if (!valid) return false
    }

    savingAlunoMatricula.value = true
    const isEdit = Boolean(matriculaForm.value.id)
    const payload = {
      aluno_id: matriculaForm.value.aluno_id,
      curso_id: matriculaForm.value.curso_id,
      valor_acordado: Number(matriculaForm.value.valor_acordado),
      horas_realizadas: Number(matriculaForm.value.horas_realizadas || 0),
      status: matriculaForm.value.status,
      data_matricula: matriculaForm.value.data_matricula || null,
      data_conclusao: matriculaForm.value.data_conclusao || null,
      observacoes: String(matriculaForm.value.observacoes || '').trim() || null,
    }

    try {
      if (isEdit) {
        await atualizarMatricula(matriculaForm.value.id, payload)
      } else {
        await criarMatricula(payload)
      }
      if (showMessage) {
        showMessage(`Matrícula ${isEdit ? 'atualizada' : 'registrada'} com sucesso!`)
      }
      await fetchAlunosEMatriculas()
      if (aoAtualizarDadosGerais) await aoAtualizarDadosGerais()
      matriculaDialog.value = false
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao salvar matrícula', 'error')
      }
      return false
    } finally {
      savingAlunoMatricula.value = false
    }
  }

  // incrementa ou decrementa rapidamente as horas cumpridas de uma matrícula direto na tabela
  async function ajustarHorasMatricula(mat, delta) {
    const novasHoras = Math.max(0, Number(mat.horas_realizadas || 0) + delta)
    if (novasHoras === mat.horas_realizadas) return

    atualizandoHorasId.value = mat.id
    try {
      await atualizarMatricula(mat.id, { horas_realizadas: novasHoras })
      await fetchAlunosEMatriculas()
      if (aoAtualizarDadosGerais) await aoAtualizarDadosGerais()
      if (showMessage && mat.carga_horaria_total > 0 && novasHoras >= mat.carga_horaria_total && mat.status === 'EM_ANDAMENTO') {
        showMessage(`Parabéns! ${mat.aluno_nome} concluiu a carga horária do curso!`)
      }
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao atualizar horas da matrícula', 'error')
      }
    } finally {
      atualizandoHorasId.value = null
    }
  }

  // exclui uma matrícula ou desativa um aluno pelo identificador
  async function removerAlunoOuMatricula(tipo, id) {
    savingAlunoMatricula.value = true
    try {
      if (tipo === 'aluno') {
        await excluirAluno(id)
      } else if (tipo === 'matricula') {
        await excluirMatricula(id)
      }
      await fetchAlunosEMatriculas()
      if (aoAtualizarDadosGerais) await aoAtualizarDadosGerais()
      return true
    } catch (error) {
      if (showMessage) {
        showMessage(error.message || 'Erro ao excluir registro', 'error')
      }
      return false
    } finally {
      savingAlunoMatricula.value = false
    }
  }

  return {
    loadingAlunosMatriculas,
    savingAlunoMatricula,
    atualizandoHorasId,
    alunos,
    matriculas,
    clientesDisponiveisParaImportar,
    subVisaoAlunos,
    buscaMatricula,
    filtroStatusMatricula,
    buscaAluno,
    matriculasFiltradas,
    alunosFiltrados,
    matriculasEmAndamentoCount,
    matriculasConcluidasCount,
    alunoDialog,
    alunoValid,
    alunoFormRef,
    alunoForm,
    alunoFormTitle,
    clienteImportadoId,
    matriculaDialog,
    matriculaValid,
    matriculaFormRef,
    matriculaForm,
    matriculaFormTitle,
    nomeRules,
    telefoneRules,
    cpfRules,
    emailRules,
    obrigatorioRule,
    valorAcordadoRules,
    aoAlterarTelefoneAluno,
    aoAlterarCpfAluno,
    aoSelecionarClienteExistente,
    aoSelecionarCursoMatricula,
    fetchAlunosEMatriculas,
    openAlunoDialog,
    closeAlunoDialog,
    openMatriculaDialog,
    closeMatriculaDialog,
    saveAluno,
    saveMatricula,
    ajustarHorasMatricula,
    removerAlunoOuMatricula,
  }
}

