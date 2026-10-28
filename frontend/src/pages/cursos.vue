<template>
  <v-container fluid class="pa-6">
    <!-- Cabeçalho da Página -->
    <v-row class="mb-4 align-center">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold text-primary">Cursos & Ensinos</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Gerencie o catálogo de cursos, modalidades, matrículas de alunos e o controle financeiro das turmas
        </p>
      </v-col>
      <v-col cols="12" md="6" class="d-flex justify-md-end flex-wrap ga-2">
        <v-btn
          color="secondary"
          variant="tonal"
          prepend-icon="mdi-book-open-page-variant-outline"
          @click="openModalidadeDialog()"
        >
          Nova Modalidade
        </v-btn>
        <v-btn
          color="accent"
          variant="tonal"
          prepend-icon="mdi-account-school-outline"
          @click="openAlunoDialog()"
        >
          Novo Aluno
        </v-btn>
        <v-btn
          color="info"
          variant="tonal"
          prepend-icon="mdi-certificate-outline"
          @click="openMatriculaDialog()"
        >
          Nova Matrícula
        </v-btn>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          size="large"
          elevation="2"
          @click="openCursoDialog()"
        >
          Novo Curso
        </v-btn>
      </v-col>
    </v-row>

    <!-- Cards de Resumo (2 cards por linha, tamanho fixo e espaçamento ajustado) -->
    <v-row class="mb-6" justify="space-between">
      <v-col cols="12" md="6">
        <v-card
          elevation="2"
          rounded="lg"
          class="pa-5 border-s-lg border-primary kpi-card"
        >
          <div class="d-flex align-start justify-space-between h-100">
            <div class="pr-3 flex-grow-1 d-flex flex-column justify-space-between h-100">
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-bold text-uppercase tracking-wide">
                  Cursos Ativos
                </div>
                <div class="text-h4 font-weight-bold text-primary mt-1">
                  {{ cursosAtivosCount }}
                </div>
              </div>
              <div class="text-body-2 text-grey-darken-2 mt-2">
                <v-icon size="16" color="primary" class="mr-1">mdi-school-outline</v-icon>
                <strong>{{ cursos.length }}</strong> curso(s) no catálogo • <strong>{{ modalidades.length }}</strong> modalidade(s) cadastradas
              </div>
            </div>
            <v-avatar color="primary" variant="tonal" size="56" class="flex-shrink-0">
              <v-icon size="30">mdi-school</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card
          elevation="2"
          rounded="lg"
          class="pa-5 border-s-lg border-primary kpi-card"
        >
          <div class="d-flex align-start justify-space-between h-100">
            <div class="pr-3 flex-grow-1 d-flex flex-column justify-space-between h-100">
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-bold text-uppercase tracking-wide">
                  Alunos & Matrículas
                </div>
                <div class="text-h4 font-weight-bold text-accent mt-1">
                  {{ matriculasEmAndamentoCount }}
                </div>
              </div>
              <div class="text-body-2 text-grey-darken-2 mt-2">
                <v-icon size="16" color="accent" class="mr-1">mdi-account-group-outline</v-icon>
                <strong>{{ matriculasEmAndamentoCount }}</strong> em andamento • <strong>{{ matriculasConcluidasCount }}</strong> concluída(s) • <strong>{{ alunos.length }}</strong> aluno(s)
              </div>
            </div>
            <v-avatar color="secondary" variant="tonal" size="56" class="flex-shrink-0">
              <v-icon size="30" color="primary">mdi-certificate-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card
          elevation="2"
          rounded="lg"
          class="pa-5 border-s-lg border-primary kpi-card"
        >
          <div class="d-flex align-start justify-space-between h-100">
            <div class="pr-3 flex-grow-1 d-flex flex-column justify-space-between h-100">
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-bold text-uppercase tracking-wide">
                  Recursos de Ensino
                </div>
                <div class="text-h4 font-weight-bold text-accent mt-1">
                  {{ modalidades.length }}
                </div>
              </div>
              <div
                class="text-body-2 mt-2 font-weight-medium"
                :class="modalidadesComFaltaCount > 0 ? 'text-error' : 'text-success'"
              >
                <v-icon size="16" class="mr-1">
                  {{ modalidadesComFaltaCount > 0 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                </v-icon>
                {{
                  modalidadesComFaltaCount > 0
                    ? `${modalidadesComFaltaCount} modalidade(s) com insumo em falta no estoque`
                    : 'Todos os materiais e equipamentos em dia para aulas'
                }}
              </div>
            </div>
            <v-avatar color="accent" variant="tonal" size="56" class="flex-shrink-0">
              <v-icon size="30">mdi-book-open-variant</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card
          elevation="2"
          rounded="lg"
          class="pa-5 border-s-lg border-success kpi-card"
        >
          <div class="d-flex align-start justify-space-between h-100">
            <div class="pr-3 flex-grow-1 d-flex flex-column justify-space-between h-100">
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-bold text-uppercase tracking-wide">
                  Receita de Cursos
                </div>
                <div class="text-h4 font-weight-bold text-success mt-1">
                  {{ formatCurrency(totalRecebidoCursos) }}
                </div>
              </div>
              <div
                class="text-body-2 mt-2 font-weight-medium"
                :class="cobrançasEmAtrasoCount > 0 ? 'text-error' : 'text-grey-darken-2'"
              >
                <v-icon size="16" class="mr-1">
                  {{ cobrançasEmAtrasoCount > 0 ? 'mdi-alert-circle-outline' : 'mdi-cash-clock' }}
                </v-icon>
                A receber: {{ formatCurrency(totalPendenteCursos) }}
                <span v-if="cobrançasEmAtrasoCount > 0" class="ml-1">
                  ({{ cobrançasEmAtrasoCount }} em atraso)
                </span>
              </div>
            </div>
            <v-avatar color="success" variant="tonal" size="56" class="flex-shrink-0">
              <v-icon size="30">mdi-cash-multiple</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Abas de Navegação do Módulo de Cursos -->
    <v-card elevation="2" rounded="lg" class="management-card">
      <v-tabs v-model="activeTab" bg-color="primary" color="white" grow>
        <v-tab value="cursos">
          <v-icon start>mdi-school</v-icon>
          Catálogo de Cursos ({{ cursos.length }})
        </v-tab>
        <v-tab value="modalidades">
          <v-icon start>mdi-book-open-page-variant-outline</v-icon>
          Modalidades ({{ modalidades.length }})
          <v-badge
            v-if="modalidadesComFaltaCount > 0"
            color="error"
            :content="modalidadesComFaltaCount"
            inline
            class="ml-2"
          ></v-badge>
        </v-tab>
        <v-tab value="matriculas">
          <v-icon start>mdi-account-school-outline</v-icon>
          Alunos & Matrículas ({{ matriculas.length }})
        </v-tab>
        <v-tab value="pagamentos">
          <v-icon start>mdi-cash-register</v-icon>
          Financeiro ({{ pagamentos.length }})
          <v-badge
            v-if="cobrançasEmAtrasoCount > 0"
            color="error"
            :content="cobrançasEmAtrasoCount"
            inline
            class="ml-2"
          ></v-badge>
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- ABA 1: CATÁLOGO DE CURSOS -->
        <v-window-item value="cursos">
          <div class="pa-4 d-flex flex-wrap align-center justify-space-between ga-3 bg-surface">
            <v-text-field
              v-model="buscaCurso"
              prepend-inner-icon="mdi-magnify"
              label="Buscar por nome do curso ou modalidade..."
              variant="outlined"
              density="compact"
              hide-details
              clearable
              style="max-width: 420px"
            ></v-text-field>
            <v-btn color="primary" variant="tonal" prepend-icon="mdi-plus" @click="openCursoDialog()">
              Adicionar Curso
            </v-btn>
          </div>

          <v-divider></v-divider>

          <v-data-table
            :headers="cursoHeaders"
            :items="cursosFiltrados"
            :loading="loadingCursos"
            :items-per-page="10"
            hover
            class="bg-surface fixed-table-content"
          >
            <template v-slot:item.nome="{ item }">
              <div class="py-2 text-center">
                <span
                  class="font-weight-bold text-body-1 text-primary cursor-pointer clickable-item"
                  @click="abrirDetalhes('curso', item)"
                >
                  {{ item.nome }}
                  <v-tooltip activator="parent" location="top">Clique para visualizar detalhes do curso</v-tooltip>
                </span>
                <div class="text-caption text-grey-darken-1">
                  {{ item.numero_aulas }} aula(s)
                  <span v-if="item.duracao_no_dia"> • {{ item.duracao_no_dia }}/dia</span>
                </div>
              </div>
            </template>

            <template v-slot:item.modalidades="{ item }">
              <div class="py-2 d-flex flex-wrap justify-center ga-1">
                <span
                  v-if="!item.modalidades || !item.modalidades.length"
                  class="text-caption text-grey"
                >
                  Nenhuma modalidade vinculada
                </span>
                <v-chip
                  v-for="mod in item.modalidades"
                  :key="mod.id"
                  size="small"
                  color="accent"
                  variant="tonal"
                  prepend-icon="mdi-book-outline"
                >
                  {{ mod.nome }}
                </v-chip>
              </div>
            </template>

            <template v-slot:item.carga_horaria_total="{ item }">
              <v-chip size="small" color="primary" variant="tonal" prepend-icon="mdi-clock-outline">
                {{ item.carga_horaria_total }}h totais
              </v-chip>
            </template>

            <template v-slot:item.valor_total="{ item }">
              <span class="font-weight-bold text-body-2">
                {{ formatCurrency(item.valor_total) }}
              </span>
            </template>

            <template v-slot:item.matriculas="{ item }">
              <v-chip
                size="small"
                :color="(item.matriculas || []).length > 0 ? 'info' : 'grey'"
                variant="tonal"
                prepend-icon="mdi-account-school"
              >
                {{ (item.matriculas || []).length }} matriculado(s)
              </v-chip>
            </template>

            <template v-slot:item.ativo="{ item }">
              <v-chip
                size="small"
                :color="item.ativo ? 'success' : 'grey-darken-1'"
                variant="flat"
                class="cursor-pointer"
                :prepend-icon="item.ativo ? 'mdi-check-circle' : 'mdi-pause-circle'"
                @click="toggleCursoAtivo(item)"
              >
                {{ item.ativo ? 'Ativo' : 'Inativo' }}
                <v-tooltip activator="parent" location="top">
                  Clique para {{ item.ativo ? 'inativar' : 'ativar' }} este curso
                </v-tooltip>
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="info"
                  @click="openMatriculaDialog(null, { curso_id: item.id })"
                >
                  <v-icon>mdi-account-plus-outline</v-icon>
                  <v-tooltip activator="parent" location="top">Matricular Aluno neste Curso</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="primary" @click="openCursoDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Curso</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('curso', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Curso</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhum curso cadastrado ainda. Clique em "Novo Curso" para montar seu catálogo de ensino.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ABA 2: MODALIDADES & RECURSOS DE ENSINO -->
        <v-window-item value="modalidades">
          <div class="pa-4 d-flex flex-wrap align-center justify-space-between ga-3 bg-surface">
            <v-text-field
              v-model="buscaModalidade"
              prepend-inner-icon="mdi-magnify"
              label="Buscar modalidade por nome ou características..."
              variant="outlined"
              density="compact"
              hide-details
              clearable
              style="max-width: 420px"
            ></v-text-field>
            <v-btn
              color="primary"
              variant="tonal"
              prepend-icon="mdi-plus"
              @click="openModalidadeDialog()"
            >
              Adicionar Modalidade
            </v-btn>
          </div>

          <v-divider></v-divider>

          <v-data-table
            :headers="modalidadeHeaders"
            :items="modalidadesFiltradas"
            :loading="loadingCursos"
            :items-per-page="10"
            hover
            class="bg-surface fixed-table-content"
          >
            <template v-slot:item.nome="{ item }">
              <div class="py-2 text-center">
                <span
                  class="font-weight-bold text-body-1 text-primary cursor-pointer clickable-item"
                  @click="abrirDetalhes('modalidade', item)"
                >
                  {{ item.nome }}
                  <v-tooltip activator="parent" location="top">Clique para visualizar detalhes da modalidade</v-tooltip>
                </span>
              </div>
            </template>

            <template v-slot:item.duracao="{ item }">
              <div class="d-flex justify-center">
                <v-chip size="small" color="accent" variant="tonal" prepend-icon="mdi-timer-outline">
                  {{ item.duracao || 'Carga flexível' }}
                </v-chip>
              </div>
            </template>

            <template v-slot:item.recursos="{ item }">
              <div class="py-2 d-flex flex-wrap justify-center ga-1">
                <span
                  v-if="(!item.materiais || !item.materiais.length) && (!item.equipamentos || !item.equipamentos.length)"
                  class="text-caption text-grey"
                >
                  Nenhum insumo vinculado
                </span>

                <v-chip
                  v-for="mat in item.materiais"
                  :key="'mod-mat-' + mat.id"
                  size="small"
                  :color="isResourceAvailable(mat) ? 'success' : 'error'"
                  :variant="isResourceAvailable(mat) ? 'tonal' : 'flat'"
                  :prepend-icon="isResourceAvailable(mat) ? 'mdi-bottle-tonic-outline' : 'mdi-alert-circle'"
                >
                  {{ mat.nome }} ({{ mat.quantidade }} {{ mat.unidade_medida || 'UN' }})
                  <v-tooltip activator="parent" location="top">
                    Material: {{ isResourceAvailable(mat) ? `Em estoque (${mat.quantidade})` : 'ESGOTADO NO ESTOQUE!' }}
                  </v-tooltip>
                </v-chip>

                <v-chip
                  v-for="eq in item.equipamentos"
                  :key="'mod-eq-' + eq.id"
                  size="small"
                  :color="isResourceAvailable(eq) ? 'primary' : 'error'"
                  :variant="isResourceAvailable(eq) ? 'tonal' : 'flat'"
                  :prepend-icon="isResourceAvailable(eq) ? 'mdi-hair-dryer-outline' : 'mdi-alert-circle'"
                >
                  {{ eq.nome }} ({{ eq.quantidade }})
                  <v-tooltip activator="parent" location="top">
                    Equipamento: {{ isResourceAvailable(eq) ? `Operacional (${eq.quantidade} un.)` : 'INDISPONÍVEL!' }}
                  </v-tooltip>
                </v-chip>
              </div>
            </template>

            <template v-slot:item.recursos_disponiveis="{ item }">
              <v-chip
                size="small"
                :color="item.recursos_disponiveis ? 'success' : 'error'"
                variant="flat"
                :prepend-icon="item.recursos_disponiveis ? 'mdi-check-circle' : 'mdi-close-circle'"
              >
                {{ item.recursos_disponiveis ? 'Pronta p/ Aula' : 'Recurso em Falta' }}
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn icon variant="text" size="small" color="primary" @click="openModalidadeDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Modalidade</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('modalidade', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Modalidade</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhuma modalidade cadastrada. Crie modalidades (módulos de ensino) e vincule os materiais usados nas aulas.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ABA 3: ALUNOS & MATRÍCULAS -->
        <v-window-item value="matriculas">
          <div class="pa-4 bg-surface">
            <!-- Linha 1: Abas de alternância, campo de busca e botão de ação principal -->
            <div class="d-flex flex-wrap align-center justify-space-between ga-3 mb-3">
              <div class="d-flex align-center flex-wrap ga-3 flex-grow-1">
                <v-btn-toggle
                  v-model="subVisaoAlunos"
                  color="primary"
                  variant="outlined"
                  density="comfortable"
                  mandatory
                >
                  <v-btn value="matriculas" prepend-icon="mdi-certificate-outline">
                    Matrículas & Progresso ({{ matriculas.length }})
                  </v-btn>
                  <v-btn value="alunos" prepend-icon="mdi-account-school-outline">
                    Cadastro de Alunos ({{ alunos.length }})
                  </v-btn>
                </v-btn-toggle>

                <v-text-field
                  v-if="subVisaoAlunos === 'matriculas'"
                  v-model="buscaMatricula"
                  prepend-inner-icon="mdi-magnify"
                  label="Buscar por aluno, código ou curso..."
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  style="min-width: 280px; max-width: 420px"
                ></v-text-field>

                <v-text-field
                  v-else
                  v-model="buscaAluno"
                  prepend-inner-icon="mdi-magnify"
                  label="Buscar aluno por nome, matrícula ou telefone..."
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  style="min-width: 280px; max-width: 420px"
                ></v-text-field>
              </div>

              <!-- Botão sempre no extremo-direito da primeira linha -->
              <div>
                <v-btn
                  v-if="subVisaoAlunos === 'alunos'"
                  color="primary"
                  variant="tonal"
                  prepend-icon="mdi-account-plus-outline"
                  @click="openAlunoDialog()"
                >
                  Novo Aluno
                </v-btn>
                <v-btn
                  v-else
                  color="primary"
                  variant="tonal"
                  prepend-icon="mdi-certificate-outline"
                  @click="openMatriculaDialog()"
                >
                  Nova Matrícula
                </v-btn>
              </div>
            </div>

            <!-- Linha 2 (isolada): Filtros de status das matrículas -->
            <div v-if="subVisaoAlunos === 'matriculas'" class="d-flex align-center flex-wrap ga-2 pt-1">
              <span class="text-caption text-grey-darken-1 font-weight-bold mr-1">Filtrar por Status:</span>
              <v-chip
                v-for="st in opcoesFiltroMatricula"
                :key="st.valor"
                size="small"
                :color="filtroStatusMatricula === st.valor ? st.cor : 'grey-darken-1'"
                :variant="filtroStatusMatricula === st.valor ? 'flat' : 'tonal'"
                class="cursor-pointer font-weight-medium"
                @click="filtroStatusMatricula = st.valor"
              >
                {{ st.rotulo }}
              </v-chip>
            </div>
          </div>

          <v-divider></v-divider>

          <!-- Sub-visão 3A: Tabela de Matrículas e Progresso -->
          <v-data-table
            v-if="subVisaoAlunos === 'matriculas'"
            :headers="matriculaHeaders"
            :items="matriculasFiltradas"
            :loading="loadingAlunosMatriculas"
            :items-per-page="10"
            hover
            class="bg-surface fixed-table-content"
          >
            <template v-slot:item.aluno_nome="{ item }">
              <div class="py-2 d-flex align-center justify-center ga-3">
                <v-avatar color="primary" variant="tonal" size="36">
                  <span class="text-caption font-weight-bold">
                    {{ obterIniciaisNome(item.aluno_nome) }}
                  </span>
                </v-avatar>
                <div class="text-left">
                  <span
                    class="font-weight-bold text-body-2 text-primary cursor-pointer clickable-item"
                    @click="abrirDetalhes('matricula', item)"
                  >
                    {{ item.aluno_nome || 'Aluno' }}
                    <v-tooltip activator="parent" location="top">Clique para visualizar detalhes da matrícula</v-tooltip>
                  </span>
                  <div class="text-caption text-grey-darken-1">
                    Matrícula: <strong>{{ item.aluno_matricula || '-' }}</strong>
                  </div>
                </div>
              </div>
            </template>

            <template v-slot:item.curso_nome="{ item }">
              <div>
                <div class="font-weight-medium text-body-2 text-primary">{{ item.curso_nome }}</div>
                <div class="text-caption text-grey-darken-1">
                  Início: {{ formatarDataBr(item.data_matricula) || '-' }}
                  <span v-if="item.data_conclusao">
                    • Fim: {{ formatarDataBr(item.data_conclusao) }}
                  </span>
                </div>
              </div>
            </template>

            <template v-slot:item.progresso="{ item }">
              <div class="py-2" style="min-width: 210px">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-caption font-weight-bold">
                    {{ item.horas_realizadas }}h / {{ item.carga_horaria_total }}h
                  </span>
                  <span class="text-caption text-primary font-weight-bold">
                    {{ item.progresso_percentual }}%
                  </span>
                </div>
                <div class="d-flex align-center ga-2">
                  <v-btn
                    icon="mdi-minus"
                    size="x-small"
                    variant="tonal"
                    color="grey-darken-1"
                    :disabled="item.horas_realizadas <= 0 || atualizandoHorasId === item.id"
                    @click="ajustarHorasMatricula(item, -1)"
                  ></v-btn>
                  <v-progress-linear
                    :model-value="item.progresso_percentual"
                    :color="item.progresso_percentual >= 100 ? 'success' : 'primary'"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  ></v-progress-linear>
                  <v-btn
                    icon="mdi-plus"
                    size="x-small"
                    variant="tonal"
                    color="primary"
                    :loading="atualizandoHorasId === item.id"
                    @click="ajustarHorasMatricula(item, 1)"
                  ></v-btn>
                </div>
              </div>
            </template>

            <template v-slot:item.valor_acordado="{ item }">
              <span class="font-weight-bold text-body-2">
                {{ formatCurrency(item.valor_acordado) }}
              </span>
            </template>

            <template v-slot:item.status="{ item }">
              <v-chip
                size="small"
                :color="obterMetaStatusMatricula(item.status).cor"
                variant="flat"
                :prepend-icon="obterMetaStatusMatricula(item.status).icone"
              >
                {{ obterMetaStatusMatricula(item.status).rotulo }}
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="success"
                  @click="
                    openPagamentoDialog(null, {
                      matricula_id: item.id,
                      aluno_id: item.aluno_id,
                      curso_id: item.curso_id,
                      valor_esperado: item.valor_acordado,
                    })
                  "
                >
                  <v-icon>mdi-cash-plus</v-icon>
                  <v-tooltip activator="parent" location="top">Gerar Cobrança / Mensalidade</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="primary" @click="openMatriculaDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Matrícula</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('matricula', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Matrícula</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhuma matrícula encontrada. Clique em "Nova Matrícula" para inscrever um aluno em um curso.
              </v-alert>
            </template>
          </v-data-table>

          <!-- Sub-visão 3B: Tabela de Alunos Cadastrados -->
          <v-data-table
            v-else
            :headers="alunoHeaders"
            :items="alunosFiltrados"
            :loading="loadingAlunosMatriculas"
            :items-per-page="10"
            hover
            class="bg-surface fixed-table-content"
          >
            <template v-slot:item.nome="{ item }">
              <div class="py-2 d-flex align-center justify-center ga-3">
                <v-avatar color="accent" variant="tonal" size="36">
                  <span class="text-caption font-weight-bold">
                    {{ obterIniciaisNome(item.nome) }}
                  </span>
                </v-avatar>
                <div class="text-left">
                  <div class="d-flex align-center ga-2">
                    <span
                      class="font-weight-bold text-body-2 text-primary cursor-pointer clickable-item"
                      @click="abrirDetalhes('aluno', item)"
                    >
                      {{ item.nome }}
                      <v-tooltip activator="parent" location="top">Clique para visualizar detalhes do aluno</v-tooltip>
                    </span>
                    <v-chip
                      v-if="item.eh_cliente"
                      size="x-small"
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-account-heart-outline"
                    >
                      Cliente & Aluno
                    </v-chip>
                  </div>
                  <div v-if="item.email" class="text-caption text-grey-darken-1">
                    {{ item.email }}
                  </div>
                </div>
              </div>
            </template>

            <template v-slot:item.matricula="{ item }">
              <v-chip
                size="small"
                color="primary"
                variant="outlined"
                prepend-icon="mdi-identifier"
                class="font-weight-bold"
              >
                {{ item.matricula }}
              </v-chip>
            </template>

            <template v-slot:item.cursos="{ item }">
              <div class="py-1 d-flex flex-wrap ga-1">
                <span v-if="!item.cursos || !item.cursos.length" class="text-caption text-grey">
                  Sem curso ativo
                </span>
                <v-chip
                  v-for="c in item.cursos"
                  :key="c.id"
                  size="small"
                  color="info"
                  variant="tonal"
                >
                  {{ c.nome }}
                </v-chip>
              </div>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="info"
                  @click="openMatriculaDialog(null, { aluno_id: item.id })"
                >
                  <v-icon>mdi-certificate-outline</v-icon>
                  <v-tooltip activator="parent" location="top">Matricular em Curso</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="primary" @click="openAlunoDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Aluno</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('aluno', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Aluno</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhum aluno cadastrado ainda. Clique em "Novo Aluno" para cadastrar.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ABA 4: FINANCEIRO (PAGAMENTOS DE CURSOS) -->
        <v-window-item value="pagamentos">
          <div class="pa-4 d-flex flex-wrap align-center justify-space-between ga-3 bg-surface">
            <v-text-field
              v-model="buscaPagamento"
              prepend-inner-icon="mdi-magnify"
              label="Buscar por aluno, curso ou tipo de cobrança..."
              variant="outlined"
              density="compact"
              hide-details
              clearable
              style="min-width: 300px; max-width: 420px"
            ></v-text-field>

            <div class="d-flex align-center flex-wrap ga-2">
              <v-chip
                v-for="fp in opcoesFiltroPagamento"
                :key="fp.valor"
                size="small"
                :color="filtroStatusPagamento === fp.valor ? fp.cor : 'grey-darken-1'"
                :variant="filtroStatusPagamento === fp.valor ? 'flat' : 'tonal'"
                class="cursor-pointer font-weight-medium"
                @click="filtroStatusPagamento = fp.valor"
              >
                {{ fp.rotulo }}
              </v-chip>

              <v-btn
                color="primary"
                variant="tonal"
                prepend-icon="mdi-cash-plus"
                class="ml-2"
                @click="openPagamentoDialog()"
              >
                Nova Cobrança
              </v-btn>
            </div>
          </div>

          <v-divider></v-divider>

          <v-data-table
            :headers="pagamentoHeaders"
            :items="pagamentosFiltrados"
            :loading="loadingPagamentos"
            :items-per-page="10"
            hover
            class="bg-surface fixed-table-content"
          >
            <template v-slot:item.aluno_nome="{ item }">
              <div class="py-2 text-center">
                <span
                  class="font-weight-bold text-body-2 text-primary cursor-pointer clickable-item"
                  @click="abrirDetalhes('pagamento', item)"
                >
                  {{ item.aluno_nome || 'Aluno' }}
                  <v-tooltip activator="parent" location="top">Clique para visualizar detalhes da cobrança</v-tooltip>
                </span>
                <div class="text-caption text-primary font-weight-medium">
                  {{ item.curso_nome || 'Curso' }}
                </div>
              </div>
            </template>

            <template v-slot:item.tipo_cobranca="{ item }">
              <v-chip size="small" color="accent" variant="tonal">
                {{ formatarTipoCobranca(item.tipo_cobranca) }}
              </v-chip>
            </template>

            <template v-slot:item.data_vencimento="{ item }">
              <div>
                <div class="text-body-2 font-weight-medium">
                  {{ formatarDataBr(item.data_vencimento) }}
                </div>
                <div v-if="item.data_pagamento" class="text-caption text-success">
                  Pago em {{ formatarDataBr(item.data_pagamento) }}
                </div>
              </div>
            </template>

            <template v-slot:item.valores="{ item }">
              <div>
                <div class="font-weight-bold text-body-2">
                  {{ formatCurrency(item.valor_esperado) }}
                </div>
                <div
                  v-if="item.valor_pago !== null && item.valor_pago !== undefined"
                  class="text-caption text-success font-weight-medium"
                >
                  Recebido: {{ formatCurrency(item.valor_pago) }}
                </div>
              </div>
            </template>

            <template v-slot:item.forma_pagamento="{ item }">
              <span class="text-body-2">
                {{ formatarFormaPagamento(item.forma_pagamento) }}
              </span>
            </template>

            <template v-slot:item.status="{ item }">
              <v-chip
                size="small"
                :color="obterMetaStatusPagamento(item).cor"
                variant="flat"
                :prepend-icon="obterMetaStatusPagamento(item).icone"
              >
                {{ obterMetaStatusPagamento(item).rotulo }}
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end align-center ga-1">
                <v-btn
                  v-if="item.status !== 'PAGO' && item.status !== 'CANCELADO'"
                  color="success"
                  variant="tonal"
                  size="small"
                  prepend-icon="mdi-cash-check"
                  @click="openBaixaDialog(item)"
                >
                  Receber
                </v-btn>
                <v-btn icon variant="text" size="small" color="primary" @click="openPagamentoDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Cobrança</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('pagamento', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Cobrança</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhuma cobrança registrada. Clique em "Nova Cobrança" para lançar taxas de matrícula ou mensalidades.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- ===================================================================== -->
    <!-- MODAL 1: CRIAR / EDITAR CURSO                                         -->
    <!-- ===================================================================== -->
    <v-dialog v-model="cursoDialog" max-width="680px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-school</v-icon>
          <span class="text-h6">{{ cursoFormTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closeCursoDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="cursoFormRef" v-model="cursoValid" @submit.prevent="saveCurso">
            <v-row>
              <v-col cols="12" sm="8">
                <v-text-field
                  v-model="cursoForm.nome"
                  label="Nome do Curso *"
                  placeholder="Ex: Formação Completa em Design de Sobrancelhas"
                  :rules="cursoNomeRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-school-outline"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="cursoForm.valor_total"
                  label="Valor Total (R$) *"
                  type="number"
                  step="0.01"
                  min="0"
                  prefix="R$"
                  :rules="valorCursoRules"
                  variant="outlined"
                  color="primary"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="cursoForm.numero_aulas"
                  label="Número de Aulas *"
                  type="number"
                  min="1"
                  :rules="numeroAulasRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-counter"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="cursoForm.carga_horaria_total"
                  label="Carga Horária Total (h) *"
                  type="number"
                  min="1"
                  suffix="horas"
                  :rules="cargaHorariaRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-clock-outline"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="cursoForm.duracao_no_dia"
                  label="Duração por Aula/Dia"
                  placeholder="Ex: 4 horas"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-timer-sand"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-subtitle-2 text-grey-darken-2">
                    Grade Curricular (Modalidades do Curso)
                  </span>
                  <v-btn
                    size="x-small"
                    color="secondary"
                    variant="tonal"
                    prepend-icon="mdi-plus"
                    @click="openModalidadeDialog()"
                  >
                    Criar Modalidade
                  </v-btn>
                </div>
                <v-autocomplete
                  v-model="cursoForm.modalidades_ids"
                  :items="modalidades"
                  item-title="nome"
                  item-value="id"
                  label="Selecione as modalidades que compõem este curso"
                  variant="outlined"
                  color="primary"
                  multiple
                  chips
                  closable-chips
                  prepend-inner-icon="mdi-book-open-page-variant-outline"
                ></v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-switch
                  v-model="cursoForm.ativo"
                  color="success"
                  label="Curso ativo e disponível para novas matrículas"
                  hide-details
                ></v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeCursoDialog">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="savingCursoModalidade"
            :disabled="!cursoValid"
            @click="saveCurso"
          >
            Salvar Curso
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 2: CRIAR / EDITAR MODALIDADE                                    -->
    <!-- ===================================================================== -->
    <v-dialog v-model="modalidadeDialog" max-width="650px" persistent :z-index="2500">
      <v-card rounded="lg">
        <v-card-title class="bg-accent text-white pa-4 d-flex align-center">
          <v-icon start>mdi-book-open-page-variant-outline</v-icon>
          <span class="text-h6">{{ modalidadeFormTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closeModalidadeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="modalidadeFormRef" v-model="modalidadeValid" @submit.prevent="saveModalidade()">
            <v-row>
              <v-col cols="12" sm="8">
                <v-text-field
                  v-model="modalidadeForm.nome"
                  label="Nome da Modalidade *"
                  placeholder="Ex: Biossegurança e Anatomia Facial"
                  :rules="modalidadeNomeRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-book-outline"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="modalidadeForm.duracao"
                  label="Duração Estimada"
                  placeholder="Ex: 8 horas"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-clock-outline"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="modalidadeForm.caracteristicas"
                  label="Características e Conteúdo Programático"
                  placeholder="Descreva os tópicos abordados nesta modalidade..."
                  rows="2"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-text-box-outline"
                ></v-textarea>
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="modalidadeForm.materiais_ids"
                  :items="materiais"
                  item-title="nome"
                  item-value="id"
                  label="Materiais (Insumos) utilizados nas aulas"
                  variant="outlined"
                  color="primary"
                  multiple
                  chips
                  closable-chips
                  prepend-inner-icon="mdi-bottle-tonic-plus-outline"
                ></v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="modalidadeForm.equipamentos_ids"
                  :items="equipamentos"
                  item-title="nome"
                  item-value="id"
                  label="Equipamentos utilizados nas aulas"
                  variant="outlined"
                  color="primary"
                  multiple
                  chips
                  closable-chips
                  prepend-inner-icon="mdi-hair-dryer-outline"
                ></v-autocomplete>
              </v-col>

              <v-col v-if="recursosFaltantesNaModalidade.length > 0" cols="12">
                <v-alert type="warning" variant="tonal" density="compact">
                  <strong>Atenção no estoque:</strong> Os seguintes recursos selecionados estão em falta ou indisponíveis:
                  {{ recursosFaltantesNaModalidade.join(', ') }}.
                </v-alert>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeModalidadeDialog">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="savingCursoModalidade"
            :disabled="!modalidadeValid"
            @click="saveModalidade()"
          >
            Salvar Modalidade
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 3: CRIAR / EDITAR ALUNO                                         -->
    <!-- ===================================================================== -->
    <v-dialog v-model="alunoDialog" max-width="640px" persistent :z-index="2500">
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-account-school-outline</v-icon>
          <span class="text-h6">{{ alunoFormTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closeAlunoDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="alunoFormRef" v-model="alunoValid" @submit.prevent="saveAluno">
            <v-row>
              <!-- Opção rápida para importar dados de um cliente já cadastrado -->
              <v-col v-if="!alunoForm.id && clientesDisponiveisParaImportar.length > 0" cols="12">
                <v-autocomplete
                  :model-value="clienteImportadoId"
                  :items="clientesDisponiveisParaImportar"
                  item-title="nome"
                  item-value="id"
                  label="Já é cliente do salão? Selecione para importar os dados"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account-arrow-right-outline"
                  clearable
                  hide-details
                  @update:model-value="aoSelecionarClienteExistente"
                ></v-autocomplete>
              </v-col>

              <v-col cols="12" sm="7">
                <v-text-field
                  v-model="alunoForm.nome"
                  label="Nome completo *"
                  :rules="nomeRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="5">
                <v-text-field
                  v-model="alunoForm.matricula"
                  label="Código de Matrícula"
                  placeholder="Automático (Ano+Trim+4 díg.)"
                  hint="Deixe em branco para gerar automaticamente"
                  persistent-hint
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-identifier"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  :model-value="alunoForm.telefone"
                  label="Telefone *"
                  placeholder="(00) 00000-0000"
                  maxlength="15"
                  :rules="telefoneRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-phone"
                  required
                  @update:model-value="aoAlterarTelefoneAluno"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  :model-value="alunoForm.cpf"
                  label="CPF"
                  placeholder="000.000.000-00"
                  maxlength="14"
                  :rules="cpfRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-card-account-details"
                  @update:model-value="aoAlterarCpfAluno"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="alunoForm.email"
                  label="E-mail"
                  type="email"
                  :rules="emailRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-email"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-combobox
                  v-model="alunoForm.endereco"
                  :search="addressSearch"
                  :items="addressSuggestions"
                  :loading="addressLoading"
                  item-title="formatted_address"
                  item-value="formatted_address"
                  :return-object="false"
                  label="Endereço"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-map-marker"
                  hide-no-data
                  clearable
                  @update:search="fetchAddressSuggestions"
                ></v-combobox>
              </v-col>

              <v-col cols="12">
                <v-checkbox
                  v-model="alunoForm.eh_cliente"
                  color="primary"
                  label="Esta pessoa também é cliente de procedimentos do salão"
                  hide-details
                ></v-checkbox>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeAlunoDialog">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="savingAlunoMatricula"
            :disabled="!alunoValid"
            @click="saveAluno"
          >
            Salvar Aluno
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 4: CRIAR / EDITAR MATRÍCULA                                     -->
    <!-- ===================================================================== -->
    <v-dialog v-model="matriculaDialog" max-width="640px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-certificate-outline</v-icon>
          <span class="text-h6">{{ matriculaFormTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closeMatriculaDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="matriculaFormRef" v-model="matriculaValid" @submit.prevent="saveMatricula">
            <v-row>
              <v-col cols="12">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-subtitle-2 text-grey-darken-2">Aluno *</span>
                  <v-btn
                    size="x-small"
                    color="accent"
                    variant="tonal"
                    prepend-icon="mdi-account-plus-outline"
                    @click="openAlunoDialog()"
                  >
                    Cadastrar Novo Aluno
                  </v-btn>
                </div>
                <v-autocomplete
                  v-model="matriculaForm.aluno_id"
                  :items="alunos"
                  item-title="nome"
                  item-value="id"
                  label="Selecione o aluno *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account-school"
                  required
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :subtitle="`Matrícula: ${(item.raw || item).matricula || '-'}`"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-autocomplete
                  v-model="matriculaForm.curso_id"
                  :items="cursos"
                  item-title="nome"
                  item-value="id"
                  label="Curso *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-school"
                  required
                  @update:model-value="aoSelecionarCursoMatricula"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :subtitle="`${(item.raw || item).carga_horaria_total}h • ${formatCurrency((item.raw || item).valor_total)}`"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="matriculaForm.valor_acordado"
                  label="Valor Acordado (R$) *"
                  type="number"
                  step="0.01"
                  min="0"
                  prefix="R$"
                  :rules="valorAcordadoRules"
                  variant="outlined"
                  color="primary"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="matriculaForm.horas_realizadas"
                  label="Horas Realizadas"
                  type="number"
                  min="0"
                  suffix="h"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-clock-check-outline"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-select
                  v-model="matriculaForm.status"
                  :items="opcoesStatusMatricula"
                  item-title="rotulo"
                  item-value="valor"
                  label="Status *"
                  variant="outlined"
                  color="primary"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="matriculaForm.data_matricula"
                  label="Data de Matrícula *"
                  type="date"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="matriculaForm.data_conclusao"
                  label="Data de Conclusão"
                  type="date"
                  variant="outlined"
                  color="primary"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="matriculaForm.observacoes"
                  label="Observações da Matrícula"
                  placeholder="Acordos de horário, bolsas ou anotações pedagógicas..."
                  rows="2"
                  variant="outlined"
                  color="primary"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeMatriculaDialog">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="savingAlunoMatricula"
            :disabled="!matriculaValid"
            @click="saveMatricula"
          >
            Salvar Matrícula
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 5: CRIAR / EDITAR COBRANÇA FINANCEIRA                           -->
    <!-- ===================================================================== -->
    <v-dialog v-model="pagamentoDialog" max-width="640px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-cash-register</v-icon>
          <span class="text-h6">{{ pagamentoFormTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closePagamentoDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="pagamentoFormRef" v-model="pagamentoValid" @submit.prevent="savePagamento">
            <v-row>
              <v-col cols="12">
                <v-autocomplete
                  v-model="pagamentoForm.matricula_id"
                  :items="matriculas"
                  item-title="aluno_nome"
                  item-value="id"
                  label="Vincular a uma Matrícula (preenche Aluno e Curso automaticamente)"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-certificate-outline"
                  clearable
                  @update:model-value="aoSelecionarMatriculaNoPagamento"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="`${(item.raw || item).aluno_nome} — ${(item.raw || item).curso_nome}`"
                      :subtitle="`Matrícula #${(item.raw || item).id} • Acordado: ${formatCurrency((item.raw || item).valor_acordado)}`"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" sm="6">
                <v-autocomplete
                  v-model="pagamentoForm.aluno_id"
                  :items="alunos"
                  item-title="nome"
                  item-value="id"
                  label="Aluno *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account-school"
                  required
                ></v-autocomplete>
              </v-col>

              <v-col cols="12" sm="6">
                <v-autocomplete
                  v-model="pagamentoForm.curso_id"
                  :items="cursos"
                  item-title="nome"
                  item-value="id"
                  label="Curso *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-school"
                  required
                ></v-autocomplete>
              </v-col>

              <v-col cols="12" sm="6">
                <v-select
                  v-model="pagamentoForm.tipo_cobranca"
                  :items="opcoesTipoCobranca"
                  item-title="rotulo"
                  item-value="valor"
                  label="Tipo de Cobrança *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6">
                <v-select
                  v-model="pagamentoForm.status"
                  :items="opcoesStatusPagamento"
                  item-title="rotulo"
                  item-value="valor"
                  label="Status do Pagamento *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="pagamentoForm.valor_esperado"
                  label="Valor Esperado (R$) *"
                  type="number"
                  step="0.01"
                  min="0"
                  prefix="R$"
                  :rules="valorPositivoRule"
                  variant="outlined"
                  color="primary"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="pagamentoForm.data_vencimento"
                  label="Data de Vencimento *"
                  type="date"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="primary"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-select
                  v-model="pagamentoForm.forma_pagamento"
                  :items="opcoesFormaPagamento"
                  item-title="rotulo"
                  item-value="valor"
                  label="Forma de Pagamento"
                  variant="outlined"
                  color="primary"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model.number="pagamentoForm.valor_pago"
                  label="Valor Pago (R$)"
                  type="number"
                  step="0.01"
                  min="0"
                  prefix="R$"
                  variant="outlined"
                  color="primary"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="pagamentoForm.data_pagamento"
                  label="Data do Pagamento"
                  type="date"
                  variant="outlined"
                  color="primary"
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closePagamentoDialog">Cancelar</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="savingPagamento"
            :disabled="!pagamentoValid"
            @click="savePagamento"
          >
            Salvar Cobrança
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 6: BAIXA RÁPIDA ("RECEBER PAGAMENTO")                           -->
    <!-- ===================================================================== -->
    <v-dialog v-model="baixaDialog" max-width="460px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-success text-white pa-4 d-flex align-center">
          <v-icon start>mdi-cash-check</v-icon>
          <span class="text-h6">Receber Pagamento</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" color="white" @click="closeBaixaDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text v-if="pagamentoEmBaixa" class="pa-6">
          <div class="mb-4 pa-3 rounded bg-background">
            <div class="text-subtitle-2 font-weight-bold text-primary">
              {{ pagamentoEmBaixa.aluno_nome }}
            </div>
            <div class="text-caption text-grey-darken-2">
              {{ pagamentoEmBaixa.curso_nome }} • {{ formatarTipoCobranca(pagamentoEmBaixa.tipo_cobranca) }}
            </div>
            <div class="text-body-2 font-weight-bold mt-1">
              Valor esperado: {{ formatCurrency(pagamentoEmBaixa.valor_esperado) }}
            </div>
          </div>

          <v-form ref="baixaFormRef" v-model="baixaValid" @submit.prevent="confirmarBaixaPagamento">
            <v-row>
              <v-col cols="12">
                <v-select
                  v-model="baixaForm.forma_pagamento"
                  :items="opcoesFormaPagamento"
                  item-title="rotulo"
                  item-value="valor"
                  label="Forma de Pagamento *"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="success"
                  prepend-inner-icon="mdi-credit-card-check-outline"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="baixaForm.valor_pago"
                  label="Valor Recebido (R$) *"
                  type="number"
                  step="0.01"
                  min="0"
                  prefix="R$"
                  :rules="valorPositivoRule"
                  variant="outlined"
                  color="success"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="baixaForm.data_pagamento"
                  label="Data do Recebimento *"
                  type="date"
                  :rules="obrigatorioRule"
                  variant="outlined"
                  color="success"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeBaixaDialog">Cancelar</v-btn>
          <v-btn
            color="success"
            variant="flat"
            :loading="savingPagamento"
            :disabled="!baixaValid"
            @click="confirmarBaixaPagamento"
          >
            Confirmar Recebimento
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 7: CONFIRMAÇÃO DE EXCLUSÃO UNIFICADA                            -->
    <!-- ===================================================================== -->
    <v-dialog v-model="deleteDialog" max-width="460px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-error text-white pa-4">Confirmar Exclusão</v-card-title>
        <v-card-text class="pa-6">
          Tem certeza que deseja excluir {{ deleteTarget.rotuloTipo }}
          <strong>{{ deleteTarget.nome }}</strong>?
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn
            color="error"
            variant="flat"
            :loading="savingCursoModalidade || savingAlunoMatricula || savingPagamento"
            @click="executeDelete"
          >
            Sim, Excluir
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 8: VISUALIZAÇÃO DE REGISTRO UNIFICADO (COMPONENTE REUTILIZÁVEL) -->
    <!-- ===================================================================== -->
    <ModalDetalhesRegistro
      v-model="detalhesModal"
      :title="
        detalhesTipo === 'curso'
          ? 'Detalhes do Curso'
          : detalhesTipo === 'modalidade'
            ? 'Detalhes da Modalidade'
            : detalhesTipo === 'matricula'
              ? 'Detalhes da Matrícula'
              : detalhesTipo === 'aluno'
                ? 'Detalhes do Aluno'
                : detalhesTipo === 'pagamento'
                  ? 'Detalhes da Cobrança'
                  : 'Detalhes'
      "
      :icon="
        detalhesTipo === 'curso'
          ? 'mdi-school'
          : detalhesTipo === 'modalidade'
            ? 'mdi-book-open-page-variant-outline'
            : detalhesTipo === 'matricula'
              ? 'mdi-certificate-outline'
              : detalhesTipo === 'aluno'
                ? 'mdi-account-school-outline'
                : detalhesTipo === 'pagamento'
                  ? 'mdi-cash-register'
                  : 'mdi-information-outline'
      "
      :color="
        detalhesTipo === 'modalidade'
          ? 'secondary'
          : detalhesTipo === 'matricula'
            ? 'info'
            : detalhesTipo === 'pagamento'
              ? 'success'
              : 'primary'
      "
      @close="fecharDetalhes"
    >
      <div v-if="detalhesItem" class="detalhes-container">
        <!-- DETALHES DE CURSO -->
        <template v-if="detalhesTipo === 'curso'">
          <div class="mb-4 d-flex align-center justify-space-between">
            <h2 class="text-h6 font-weight-bold text-primary">{{ detalhesItem.nome }}</h2>
            <v-chip
              size="small"
              :color="detalhesItem.ativo ? 'success' : 'grey'"
              variant="flat"
              :prepend-icon="detalhesItem.ativo ? 'mdi-check-circle' : 'mdi-pause-circle'"
            >
              {{ detalhesItem.ativo ? 'Ativo' : 'Inativo' }}
            </v-chip>
          </div>

          <v-row class="mb-2" density="compact">
            <v-col cols="12" sm="4">
              <div class="text-caption text-grey-darken-1 font-weight-bold">VALOR TOTAL</div>
              <div class="text-subtitle-1 font-weight-bold text-success">
                {{ formatCurrency(detalhesItem.valor_total) }}
              </div>
            </v-col>
            <v-col cols="12" sm="4">
              <div class="text-caption text-grey-darken-1 font-weight-bold">AULAS</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ detalhesItem.numero_aulas }} aula(s)
              </div>
            </v-col>
            <v-col cols="12" sm="4">
              <div class="text-caption text-grey-darken-1 font-weight-bold">CARGA HORÁRIA</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ detalhesItem.carga_horaria_total }} horas
              </div>
            </v-col>
            <v-col v-if="detalhesItem.duracao_no_dia" cols="12">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DURAÇÃO ESTIMADA POR AULA</div>
              <div class="text-body-2">{{ detalhesItem.duracao_no_dia }}</div>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <!-- Campo Modalidades com tamanho fixo e scroll para não extrapolar -->
          <div>
            <div class="text-caption text-grey-darken-1 font-weight-bold mb-2">
              MODALIDADES DO CURSO (GRADE CURRICULAR)
            </div>
            <div class="modalidade-scroll-box rounded border pa-3 bg-grey-lighten-4">
              <template v-if="detalhesItem.modalidades && detalhesItem.modalidades.length">
                <div
                  v-for="mod in detalhesItem.modalidades"
                  :key="mod.id"
                  class="mb-2 pa-2 rounded bg-white border"
                >
                  <div class="d-flex align-center justify-space-between mb-1">
                    <span class="font-weight-bold text-body-2 text-primary">{{ mod.nome }}</span>
                    <v-chip size="x-small" color="secondary" variant="tonal">
                      {{ mod.duracao || 'Flexível' }}
                    </v-chip>
                  </div>
                  <div v-if="mod.caracteristicas" class="text-caption text-grey-darken-2">
                    {{ mod.caracteristicas }}
                  </div>
                </div>
              </template>
              <div v-else class="text-body-2 text-grey-darken-1 py-3 text-center">
                Nenhuma modalidade vinculada a este curso.
              </div>
            </div>
          </div>
        </template>

        <!-- DETALHES DE MODALIDADE -->
        <template v-else-if="detalhesTipo === 'modalidade'">
          <div class="mb-4 d-flex align-center justify-space-between">
            <h2 class="text-h6 font-weight-bold text-secondary">{{ detalhesItem.nome }}</h2>
            <v-chip
              size="small"
              :color="detalhesItem.recursos_disponiveis ? 'success' : 'error'"
              variant="flat"
              :prepend-icon="detalhesItem.recursos_disponiveis ? 'mdi-check-circle' : 'mdi-close-circle'"
            >
              {{ detalhesItem.recursos_disponiveis ? 'Pronta para Aula' : 'Insumo em Falta' }}
            </v-chip>
          </div>

          <v-row class="mb-2" density="compact">
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DURAÇÃO ESTIMADA</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ detalhesItem.duracao || 'Carga horária flexível' }}
              </div>
            </v-col>
            <v-col v-if="detalhesItem.caracteristicas" cols="12">
              <div class="text-caption text-grey-darken-1 font-weight-bold">CONTEÚDO PROGRAMÁTICO</div>
              <div class="text-body-2 pa-2 bg-grey-lighten-4 rounded border">
                {{ detalhesItem.caracteristicas }}
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <!-- Insumos e Materiais vinculados com tamanho fixo e scroll -->
          <div>
            <div class="text-caption text-grey-darken-1 font-weight-bold mb-2">
              INSUMOS E EQUIPAMENTOS EXIGIDOS
            </div>
            <div class="modalidade-scroll-box rounded border pa-3 bg-grey-lighten-4">
              <div class="text-caption font-weight-bold text-grey-darken-2 mb-1">Materiais de Consumo:</div>
              <div class="d-flex flex-wrap ga-2 mb-3">
                <template v-if="detalhesItem.materiais && detalhesItem.materiais.length">
                  <v-chip
                    v-for="mat in detalhesItem.materiais"
                    :key="'det-mat-' + mat.id"
                    size="small"
                    :color="isResourceAvailable(mat) ? 'success' : 'error'"
                    :variant="isResourceAvailable(mat) ? 'tonal' : 'flat'"
                    :prepend-icon="isResourceAvailable(mat) ? 'mdi-bottle-tonic-outline' : 'mdi-alert-circle'"
                  >
                    {{ mat.nome }} ({{ mat.quantidade }} {{ mat.unidade_medida || 'UN' }})
                  </v-chip>
                </template>
                <span v-else class="text-caption text-grey">Nenhum material cadastrado</span>
              </div>

              <div class="text-caption font-weight-bold text-grey-darken-2 mb-1">Equipamentos:</div>
              <div class="d-flex flex-wrap ga-2">
                <template v-if="detalhesItem.equipamentos && detalhesItem.equipamentos.length">
                  <v-chip
                    v-for="eq in detalhesItem.equipamentos"
                    :key="'det-eq-' + eq.id"
                    size="small"
                    :color="isResourceAvailable(eq) ? 'primary' : 'error'"
                    :variant="isResourceAvailable(eq) ? 'tonal' : 'flat'"
                    :prepend-icon="isResourceAvailable(eq) ? 'mdi-hair-dryer-outline' : 'mdi-alert-circle'"
                  >
                    {{ eq.nome }} ({{ eq.quantidade }})
                  </v-chip>
                </template>
                <span v-else class="text-caption text-grey">Nenhum equipamento cadastrado</span>
              </div>
            </div>
          </div>
        </template>

        <!-- DETALHES DE MATRÍCULA -->
        <template v-else-if="detalhesTipo === 'matricula'">
          <div class="mb-4 d-flex align-center justify-space-between">
            <div>
              <h2 class="text-h6 font-weight-bold text-primary">{{ detalhesItem.aluno_nome }}</h2>
              <div class="text-caption text-grey-darken-1">
                Matrícula Aluno: <strong>{{ detalhesItem.aluno_matricula || '-' }}</strong>
              </div>
            </div>
            <v-chip
              size="small"
              :color="obterMetaStatusMatricula(detalhesItem.status).cor"
              variant="flat"
              :prepend-icon="obterMetaStatusMatricula(detalhesItem.status).icone"
            >
              {{ obterMetaStatusMatricula(detalhesItem.status).rotulo }}
            </v-chip>
          </div>

          <v-row class="mb-2" density="compact">
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">CURSO</div>
              <div class="text-subtitle-2 font-weight-bold text-primary">
                {{ detalhesItem.curso_nome }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">VALOR ACORDADO</div>
              <div class="text-subtitle-2 font-weight-bold text-success">
                {{ formatCurrency(detalhesItem.valor_acordado) }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DATA DE MATRÍCULA</div>
              <div class="text-body-2">{{ formatarDataBr(detalhesItem.data_matricula) || '-' }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DATA DE CONCLUSÃO</div>
              <div class="text-body-2">{{ formatarDataBr(detalhesItem.data_conclusao) || 'Em andamento' }}</div>
            </v-col>
            <v-col cols="12">
              <div class="text-caption text-grey-darken-1 font-weight-bold mb-1">PROGRESSO DAS AULAS</div>
              <div class="d-flex align-center ga-3">
                <v-progress-linear
                  :model-value="detalhesItem.progresso_percentual"
                  :color="detalhesItem.progresso_percentual >= 100 ? 'success' : 'primary'"
                  height="10"
                  rounded
                  class="flex-grow-1"
                ></v-progress-linear>
                <span class="text-body-2 font-weight-bold">
                  {{ detalhesItem.horas_realizadas }}/{{ detalhesItem.curso_carga_horaria }}h
                  ({{ detalhesItem.progresso_percentual }}%)
                </span>
              </div>
            </v-col>
            <v-col v-if="detalhesItem.observacoes" cols="12">
              <div class="text-caption text-grey-darken-1 font-weight-bold">OBSERVAÇÕES</div>
              <div class="text-body-2 pa-2 bg-grey-lighten-4 rounded border">
                {{ detalhesItem.observacoes }}
              </div>
            </v-col>
          </v-row>
        </template>

        <!-- DETALHES DE ALUNO -->
        <template v-else-if="detalhesTipo === 'aluno'">
          <div class="mb-4 d-flex align-center justify-space-between">
            <div>
              <h2 class="text-h6 font-weight-bold text-primary">{{ detalhesItem.nome }}</h2>
              <v-chip size="small" color="primary" variant="outlined" class="mt-1 font-weight-bold">
                Matrícula: {{ detalhesItem.matricula }}
              </v-chip>
            </div>
            <v-chip
              v-if="detalhesItem.eh_cliente"
              size="small"
              color="accent"
              variant="tonal"
              prepend-icon="mdi-account-heart-outline"
            >
              Cliente & Aluno
            </v-chip>
          </div>

          <v-row class="mb-2" density="compact">
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">TELEFONE</div>
              <div class="text-body-1 font-weight-medium">{{ detalhesItem.telefone }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">CPF</div>
              <div class="text-body-1">{{ detalhesItem.cpf || '-' }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">E-MAIL</div>
              <div class="text-body-1">{{ detalhesItem.email || '-' }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">ENDEREÇO</div>
              <div class="text-body-1">{{ detalhesItem.endereco || '-' }}</div>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <div>
            <div class="text-caption text-grey-darken-1 font-weight-bold mb-2">CURSOS MATRICULADOS</div>
            <div class="modalidade-scroll-box rounded border pa-3 bg-grey-lighten-4">
              <template v-if="detalhesItem.cursos && detalhesItem.cursos.length">
                <div
                  v-for="c in detalhesItem.cursos"
                  :key="c.id"
                  class="mb-2 pa-2 rounded bg-white border d-flex align-center justify-space-between"
                >
                  <span class="font-weight-medium text-body-2">{{ c.nome }}</span>
                  <v-chip size="x-small" color="primary" variant="tonal">Inscrito</v-chip>
                </div>
              </template>
              <div v-else class="text-body-2 text-grey-darken-1 py-3 text-center">
                Nenhum curso matriculado no momento.
              </div>
            </div>
          </div>
        </template>

        <!-- DETALHES DE PAGAMENTO/COBRANÇA -->
        <template v-else-if="detalhesTipo === 'pagamento'">
          <div class="mb-4 d-flex align-center justify-space-between">
            <div>
              <h2 class="text-h6 font-weight-bold text-primary">{{ detalhesItem.aluno_nome }}</h2>
              <div class="text-caption text-primary font-weight-medium">
                {{ detalhesItem.curso_nome || 'Curso' }}
              </div>
            </div>
            <v-chip
              size="small"
              :color="obterMetaStatusPagamento(detalhesItem).cor"
              variant="flat"
              :prepend-icon="obterMetaStatusPagamento(detalhesItem).icone"
            >
              {{ obterMetaStatusPagamento(detalhesItem).rotulo }}
            </v-chip>
          </div>

          <v-row class="mb-2" density="compact">
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">TIPO DE COBRANÇA</div>
              <div class="text-subtitle-2 font-weight-bold">
                {{ formatarTipoCobranca(detalhesItem.tipo_cobranca) }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">FORMA DE PAGAMENTO</div>
              <div class="text-subtitle-2">
                {{ formatarFormaPagamento(detalhesItem.forma_pagamento) }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">VALOR ESPERADO</div>
              <div class="text-subtitle-1 font-weight-bold text-primary">
                {{ formatCurrency(detalhesItem.valor_esperado) }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">VALOR RECEBIDO</div>
              <div class="text-subtitle-1 font-weight-bold text-success">
                {{ detalhesItem.valor_pago !== null && detalhesItem.valor_pago !== undefined ? formatCurrency(detalhesItem.valor_pago) : '-' }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DATA DE VENCIMENTO</div>
              <div class="text-body-2 font-weight-medium">
                {{ formatarDataBr(detalhesItem.data_vencimento) }}
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1 font-weight-bold">DATA DO RECEBIMENTO</div>
              <div class="text-body-2">
                {{ detalhesItem.data_pagamento ? formatarDataBr(detalhesItem.data_pagamento) : '-' }}
              </div>
            </v-col>
          </v-row>
        </template>
      </div>
    </ModalDetalhesRegistro>

    <!-- Snackbar Global de Feedback -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3500" location="top right">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn icon variant="text" @click="snackbar = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ModalDetalhesRegistro from '@/components/ModalDetalhesRegistro.vue'
import { useSnackbar } from '@/composables/shared/useSnackbar'
import { useAddressAutocomplete } from '@/composables/shared/useAddressAutocomplete'
import { useCursosModalidades } from '@/composables/cursos/useCursosModalidades'
import { useAlunosMatriculas } from '@/composables/cursos/useAlunosMatriculas'
import { usePagamentosCurso } from '@/composables/cursos/usePagamentosCurso'
import { isResourceAvailable } from '@/utils/estoque/estoqueUtils'
import { formatCurrency, formatarDataBr } from '@/utils/shared/formatters'
import {
  opcoesStatusMatricula,
  opcoesTipoCobranca,
  opcoesStatusPagamento,
  opcoesFormaPagamento,
  obterMetaStatusMatricula,
  obterMetaStatusPagamento,
  formatarTipoCobranca,
  formatarFormaPagamento,
  obterIniciaisNome,
} from '@/utils/cursos/cursosUtils'

const activeTab = ref('cursos')

// notificações e autocompletar de endereço (composables compartilhados)
const { snackbar, snackbarText, snackbarColor, showMessage } = useSnackbar()
const {
  addressSearch,
  addressSuggestions,
  addressLoading,
  fetchAddressSuggestions,
  resetAddressSearch,
} = useAddressAutocomplete()

// composable de cursos, modalidades e vínculo com estoque
const {
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
} = useCursosModalidades(showMessage)

// composable de alunos e matrículas
const {
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
} = useAlunosMatriculas(showMessage, cursos, fetchCursosEModalidades, resetAddressSearch)

// composable financeiro de pagamentos de cursos
const {
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
} = usePagamentosCurso(showMessage, matriculas)

// opções de chips para filtros rápidos nas abas
const opcoesFiltroMatricula = [
  { valor: 'TODOS', rotulo: 'Todas', cor: 'primary' },
  ...opcoesStatusMatricula,
]

const opcoesFiltroPagamento = [
  { valor: 'TODOS', rotulo: 'Todos', cor: 'primary' },
  ...opcoesStatusPagamento,
]

// cabeçalhos das tabelas de cada aba
const cursoHeaders = [
  { title: 'Curso', key: 'nome', align: 'center' },
  { title: 'Modalidades (Grade)', key: 'modalidades', sortable: false, align: 'center' },
  { title: 'Carga Horária', key: 'carga_horaria_total', align: 'center' },
  { title: 'Valor Total', key: 'valor_total', align: 'center' },
  { title: 'Matrículas', key: 'matriculas', sortable: false, align: 'center' },
  { title: 'Status', key: 'ativo', align: 'center' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'center', width: '140px' },
]

const modalidadeHeaders = [
  { title: 'Modalidade', key: 'nome', align: 'center' },
  { title: 'Duração', key: 'duracao', align: 'center' },
  { title: 'Materiais & Equipamentos Exigidos', key: 'recursos', sortable: false, align: 'center' },
  { title: 'Disponibilidade', key: 'recursos_disponiveis', align: 'center' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'center', width: '110px' },
]

const matriculaHeaders = [
  { title: 'Aluno', key: 'aluno_nome', align: 'center' },
  { title: 'Curso & Período', key: 'curso_nome', align: 'center' },
  { title: 'Progresso de Horas', key: 'progresso', sortable: false, align: 'center' },
  { title: 'Valor Acordado', key: 'valor_acordado', align: 'center' },
  { title: 'Status', key: 'status', align: 'center' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'center', width: '140px' },
]

const alunoHeaders = [
  { title: 'Aluno', key: 'nome', align: 'center' },
  { title: 'Matrícula', key: 'matricula', align: 'center' },
  { title: 'Telefone', key: 'telefone', sortable: false, align: 'center' },
  { title: 'CPF', key: 'cpf', sortable: false, align: 'center' },
  { title: 'Cursos Inscritos', key: 'cursos', sortable: false, align: 'center' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'center', width: '140px' },
]

const pagamentoHeaders = [
  { title: 'Aluno / Curso', key: 'aluno_nome', align: 'center' },
  { title: 'Tipo', key: 'tipo_cobranca', align: 'center' },
  { title: 'Vencimento', key: 'data_vencimento', align: 'center' },
  { title: 'Valor', key: 'valores', sortable: false, align: 'center' },
  { title: 'Forma', key: 'forma_pagamento', align: 'center' },
  { title: 'Status', key: 'status', align: 'center' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'center', width: '200px' },
]

// controle unificado de exclusão
const deleteDialog = ref(false)
const deleteTarget = ref({ tipo: '', id: null, nome: '', rotuloTipo: '' })

// controle unificado de visualização/detalhes dos registros
const detalhesModal = ref(false)
const detalhesTipo = ref('')
const detalhesItem = ref(null)

function abrirDetalhes(tipo, item) {
  detalhesTipo.value = tipo
  detalhesItem.value = item
  detalhesModal.value = true
}

function fecharDetalhes() {
  detalhesModal.value = false
  detalhesTipo.value = ''
  detalhesItem.value = null
}

function confirmDelete(tipo, item) {
  const mapaRotulos = {
    curso: 'o curso',
    modalidade: 'a modalidade',
    aluno: 'o aluno',
    matricula: 'a matrícula de',
    pagamento: 'a cobrança de',
  }
  const nomeExibicao =
    tipo === 'matricula'
      ? `${item.aluno_nome} (${item.curso_nome})`
      : tipo === 'pagamento'
        ? `${item.aluno_nome} (${formatCurrency(item.valor_esperado)})`
        : item.nome
  deleteTarget.value = {
    tipo,
    id: item.id,
    nome: nomeExibicao,
    rotuloTipo: mapaRotulos[tipo] || 'o registro',
  }
  deleteDialog.value = true
}

async function executeDelete() {
  const { tipo, id } = deleteTarget.value
  let sucesso = false
  if (tipo === 'curso' || tipo === 'modalidade') {
    sucesso = await removerCursoOuModalidade(tipo, id)
  } else if (tipo === 'aluno' || tipo === 'matricula') {
    sucesso = await removerAlunoOuMatricula(tipo, id)
  } else if (tipo === 'pagamento') {
    sucesso = await removerPagamento(id)
  }

  if (sucesso) {
    showMessage('Registro excluído com sucesso!')
    deleteDialog.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    fetchCursosEModalidades(),
    fetchAlunosEMatriculas(),
    fetchPagamentos(),
  ])
})
</script>

<style scoped>
.management-card {
  min-height: 720px;
  display: flex;
  flex-direction: column;
}

.management-card :deep(.v-window) {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}

.management-card :deep(.v-window-item) {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}

.management-card :deep(.fixed-table-content) {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}

.management-card :deep(.v-table__wrapper) {
  min-height: 540px;
}

.clickable-item {
  transition: opacity 0.2s ease, text-decoration 0.2s ease;
}

.clickable-item:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.modalidade-scroll-box {
  max-height: 180px;
  overflow-y: auto;
}

.kpi-card {
  height: 145px;
  min-height: 145px;
  max-height: 145px;
  overflow: hidden;
}

.tracking-wide {
  letter-spacing: 0.5px;
}

.v-btn {
  text-transform: none;
  letter-spacing: 0.4px;
}
</style>
