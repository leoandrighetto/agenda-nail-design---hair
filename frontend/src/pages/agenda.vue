<template>
  <v-container fluid class="pa-4">
    <!-- Cabeçalho da Página e Navegação de Mês -->
    <v-row align="center" justify="space-between" class="mb-4">
      <v-col cols="12" md="4">
        <h1 class="text-h4 text-primary font-weight-bold">Minha Agenda</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Acompanhe seus horários e gerencie os atendimentos do salão.
        </p>
      </v-col>

      <v-col cols="12" md="4" class="d-flex align-center justify-center ga-1">
        <v-btn
          icon="mdi-chevron-left"
          variant="tonal"
          color="primary"
          size="small"
          title="Mês anterior"
          @click="prevMonth"
        ></v-btn>

        <div class="text-center mx-4" style="min-width: 200px">
          <span class="text-h5 font-weight-bold text-primary text-capitalize">
            {{ monthName }} {{ currentYear }}
          </span>
        </div>

        <v-btn
          icon="mdi-chevron-right"
          variant="tonal"
          color="primary"
          size="small"
          title="Próximo mês"
          @click="nextMonth"
        ></v-btn>

        <v-btn
          variant="outlined"
          color="primary"
          size="small"
          class="ml-2"
           prepend-icon="mdi-calendar-today"
          @click="irParaHoje"
        >
          Hoje
        </v-btn>
      </v-col>

      <v-col cols="12" md="4" class="text-md-right text-center">
        <v-btn
          color="primary"
          rounded="pill"
          size="large"
          prepend-icon="mdi-calendar-plus"
          elevation="3"
          @click="abrirNovoAgendamento()"
        >
          Novo Agendamento
        </v-btn>
      </v-col>
    </v-row>

    <!-- Cards de Resumo (KPIs da Agenda) -->
    <v-row class="mb-5">
      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4 border-s-lg border-primary">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Atendimentos Hoje
              </div>
              <div class="text-h4 font-weight-bold text-primary mt-1">
                {{ agendamentosHoje.length }}
              </div>
              <div class="text-caption text-grey-darken-1 mt-1">
                <v-icon size="14" color="primary" class="mr-1">mdi-clock-fast</v-icon>
                {{
                  proximoAtendimentoHoje
                    ? `Próximo às ${proximoAtendimentoHoje.hora} (${proximoAtendimentoHoje.cliente})`
                    : 'Nenhum horário pendente hoje'
                }}
              </div>
            </div>
            <v-avatar color="primary" variant="tonal" size="52">
              <v-icon size="28">mdi-calendar-today</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Agendamentos em {{ monthName }}
              </div>
              <div class="text-h4 font-weight-bold text-accent mt-1">
                {{ agendamentosDoMes.length }}
              </div>
              <div class="text-caption text-grey-darken-1 mt-1">
                <v-icon size="14" color="accent" class="mr-1">mdi-calendar-clock</v-icon>
                {{ pendentesOuConfirmadosMes }} ativo(s) • {{ canceladosMes }} cancelado(s)
              </div>
            </div>
            <v-avatar color="secondary" variant="tonal" size="52">
              <v-icon size="28" color="primary">mdi-calendar-month</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Concluídos no Mês
              </div>
              <div class="text-h4 font-weight-bold text-success mt-1">
                {{ concluidosMes }}
              </div>
              <div class="text-caption text-success mt-1 font-weight-medium">
                <v-icon size="14" class="mr-1">mdi-cash-check</v-icon>
                Receita realizada: R$ {{ formatarMoeda(receitaConcluidaMes) }}
              </div>
            </div>
            <v-avatar color="success" variant="tonal" size="52">
              <v-icon size="28">mdi-check-decagram</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Barra de Filtros e Legenda de Status -->
    <v-card elevation="1" rounded="lg" class="pa-3 mb-4">
      <v-row align="center" no-gutters class="ga-3">
        <v-col cols="12" md="5">
          <v-text-field
            v-model="termoBusca"
            prepend-inner-icon="mdi-magnify"
            label="Buscar por cliente ou serviço..."
            variant="outlined"
            density="compact"
            hide-details
            clearable
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="7" class="d-flex align-center justify-md-end flex-wrap ga-2">
          <span class="text-caption text-grey-darken-1 font-weight-medium mr-1">
            Filtrar status:
          </span>
          <v-chip
            v-for="item in opcoesFiltroStatus"
            :key="item.valor"
            :color="filtroStatus === item.valor ? item.cor : 'grey-darken-1'"
            :variant="filtroStatus === item.valor ? 'flat' : 'tonal'"
            size="small"
            class="font-weight-medium cursor-pointer"
            @click="filtroStatus = item.valor"
          >
            <v-icon v-if="item.icone" start size="14">{{ item.icone }}</v-icon>
            {{ item.rotulo }}
          </v-chip>
        </v-col>
      </v-row>
    </v-card>

    <!-- Estado de Carregamento -->
    <v-progress-linear
      v-if="store.loading"
      indeterminate
      color="primary"
      class="mb-2 rounded"
    ></v-progress-linear>

    <!-- Grade Mensal de Calendário -->
    <v-row>
      <v-col cols="12">
        <CalendarGrid
          :year="currentYear"
          :month="currentMonth"
          :events="eventosFiltrados"
          @select-date="abrirNovoAgendamento"
          @select-event="abrirDetalhesAgendamento"
        />
      </v-col>
    </v-row>

    <!-- ===================================================================== -->
    <!-- MODAL 1: VISUALIZAR DETALHES E ALTERAR STATUS RAPIDAMENTE             -->
    <!-- ===================================================================== -->
    <v-dialog v-model="detalheDialog" max-width="520px">
      <v-card v-if="agendamentoSelecionado" rounded="lg">
        <v-card-title
          class="text-white pa-4 d-flex align-center justify-space-between"
          :class="`bg-${agendamentoSelecionado.color || 'primary'}`"
        >
          <div class="d-flex align-center">
            <v-icon class="mr-2">mdi-calendar-account</v-icon>
            <span>Detalhes do Agendamento</span>
          </div>
          <v-chip size="small" color="white" variant="outlined" class="font-weight-bold">
            {{ agendamentoSelecionado.status }}
          </v-chip>
        </v-card-title>

        <v-card-text class="pa-5">
          <!-- Dados da Cliente -->
          <div class="d-flex align-center mb-4">
            <v-avatar color="primary" variant="tonal" size="46" class="mr-3">
              <v-icon size="24">mdi-account-heart</v-icon>
            </v-avatar>
            <div>
              <div class="text-caption text-grey-darken-1">Cliente</div>
              <div class="text-h6 font-weight-bold text-primary">
                {{ agendamentoSelecionado.cliente }}
              </div>
              <div v-if="clienteDetalhe?.telefone" class="text-body-2 text-grey-darken-2">
                <v-icon size="14" class="mr-1">mdi-phone</v-icon>
                {{ clienteDetalhe.telefone }}
              </div>
            </div>
          </div>

          <v-divider class="mb-4"></v-divider>

          <!-- Dados do Serviço e Horário -->
          <v-row dense class="mb-3">
            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1">Serviço / Procedimento</div>
              <div class="text-subtitle-1 font-weight-bold text-accent">
                {{ agendamentoSelecionado.servico }}
              </div>
              <div v-if="servicoDetalhe?.preco != null" class="text-caption text-grey-darken-2">
                Valor: <strong>R$ {{ formatarMoeda(servicoDetalhe.preco) }}</strong>
                ({{ servicoDetalhe.duracao_minutos }} min)
              </div>
            </v-col>

            <v-col cols="12" sm="6">
              <div class="text-caption text-grey-darken-1">Data e Horário</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ formatarDataBr(agendamentoSelecionado.data) }}
              </div>
              <div class="text-body-2 text-grey-darken-2">
                <v-icon size="14" class="mr-1">mdi-clock-outline</v-icon>
                {{ agendamentoSelecionado.hora }}
                {{ agendamentoSelecionado.hora_fim ? `às ${agendamentoSelecionado.hora_fim}` : '' }}
              </div>
            </v-col>
          </v-row>

          <!-- Alerta se o serviço tiver recursos em falta no estoque -->
          <v-alert
            v-if="servicoDetalhe && !servicoDetalhe.recursos_disponiveis"
            type="warning"
            variant="tonal"
            density="compact"
            class="mb-4"
            icon="mdi-alert-circle-outline"
          >
            <div class="text-caption font-weight-bold">
              Atenção: Este serviço possui recursos sem estoque ou indisponíveis!
            </div>
            <div class="text-caption">
              Itens em falta: {{ listarRecursosIndisponiveis(servicoDetalhe).join(', ') }}
            </div>
          </v-alert>

          <v-divider class="mb-4"></v-divider>

          <!-- Alteração rápida de Status -->
          <div class="text-caption text-grey-darken-1 font-weight-medium mb-2">
            Alterar status rapidamente:
          </div>
          <div class="d-flex flex-wrap ga-2">
            <v-btn
              v-for="st in opcoesStatus"
              :key="st.valor"
              :color="st.cor"
              :variant="agendamentoSelecionado.status === st.valor ? 'flat' : 'tonal'"
              size="small"
              :prepend-icon="st.icone"
              :loading="atualizandoStatus === st.valor"
              @click="alterarStatusRapido(st.valor)"
            >
              {{ st.valor }}
            </v-btn>
          </div>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0 d-flex justify-space-between">
          <v-btn
            color="error"
            variant="tonal"
            prepend-icon="mdi-delete-outline"
            @click="confirmarExclusao(agendamentoSelecionado)"
          >
            Excluir
          </v-btn>

          <div class="d-flex ga-2">
            <v-btn color="grey-darken-1" variant="text" @click="detalheDialog = false">
              Fechar
            </v-btn>
            <v-btn
              color="primary"
              variant="flat"
              prepend-icon="mdi-pencil"
              @click="abrirEdicaoAgendamento(agendamentoSelecionado)"
            >
              Editar
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 2: CRIAR OU EDITAR AGENDAMENTO                                  -->
    <!-- ===================================================================== -->
    <v-dialog v-model="agendamentoDialog" max-width="620px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon class="mr-2">
            {{ form.id ? 'mdi-calendar-edit' : 'mdi-calendar-plus' }}
          </v-icon>
          <span>{{ form.id ? 'Editar Agendamento' : 'Novo Agendamento' }}</span>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="formRef" v-model="formValido" @submit.prevent="salvarAgendamento">
            <v-row>
              <!-- Seleção de Cliente -->
              <v-col cols="12">
                <v-autocomplete
                  v-model="form.cliente_id"
                  :items="store.clientes"
                  item-title="nome"
                  item-value="id"
                  label="Cliente *"
                  placeholder="Digite o nome da cliente..."
                  prepend-inner-icon="mdi-account-outline"
                  variant="outlined"
                  :rules="[rules.required]"
                  no-data-text="Nenhum cliente encontrado"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item.raw.nome"
                      :subtitle="item.raw.telefone || 'Sem telefone'"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <!-- Seleção de Serviço -->
              <v-col cols="12">
                <v-autocomplete
                  v-model="form.servico_id"
                  :items="store.servicos"
                  item-title="nome"
                  item-value="id"
                  label="Serviço / Procedimento *"
                  placeholder="Selecione o procedimento..."
                  prepend-inner-icon="mdi-content-cut"
                  variant="outlined"
                  :rules="[rules.required]"
                  no-data-text="Nenhum serviço cadastrado"
                  @update:model-value="aoSelecionarServico"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.raw.nome">
                      <template v-slot:subtitle>
                        <span>
                          {{ item.raw.duracao_minutos || 30 }} min • R$
                          {{ formatarMoeda(item.raw.preco) }}
                        </span>
                      </template>
                      <template v-slot:append>
                        <v-chip
                          :color="item.raw.recursos_disponiveis ? 'success' : 'warning'"
                          size="x-small"
                          variant="tonal"
                        >
                          {{
                            item.raw.recursos_disponiveis ? 'Estoque OK' : 'Recurso em falta'
                          }}
                        </v-chip>
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <!-- Alerta Inteligente se o Serviço Selecionado não tiver Recursos Disponíveis -->
              <v-col v-if="servicoSelecionadoForm && !servicoSelecionadoForm.recursos_disponiveis" cols="12" class="pt-0">
                <v-alert
                  type="warning"
                  variant="tonal"
                  border="start"
                  density="comfortable"
                  icon="mdi-alert"
                >
                  <div class="font-weight-bold mb-1">
                    Recurso indisponível ou esgotado para "{{ servicoSelecionadoForm.nome }}"!
                  </div>
                  <div class="text-body-2">
                    Verifique a reposição antes do atendimento. Itens afetados:
                    <strong>{{ listarRecursosIndisponiveis(servicoSelecionadoForm).join(', ') }}</strong>
                  </div>
                </v-alert>
              </v-col>

              <!-- Resumo do Serviço Selecionado -->
              <v-col v-if="servicoSelecionadoForm" cols="12" class="pt-0">
                <v-sheet
                  color="background"
                  rounded="md"
                  class="pa-3 d-flex align-center justify-space-between border"
                >
                  <div class="d-flex align-center ga-2">
                    <v-icon color="primary" size="20">mdi-timer-outline</v-icon>
                    <span class="text-body-2">
                      Duração estimada:
                      <strong>{{ servicoSelecionadoForm.duracao_minutos || 30 }} minutos</strong>
                    </span>
                  </div>
                  <div class="text-body-2 font-weight-bold text-primary">
                    Valor: R$ {{ formatarMoeda(servicoSelecionadoForm.preco) }}
                  </div>
                </v-sheet>
              </v-col>

              <!-- Data e Horários -->
              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="form.data"
                  label="Data *"
                  type="date"
                  prepend-inner-icon="mdi-calendar"
                  variant="outlined"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="form.hora_inicio"
                  label="Início *"
                  type="time"
                  prepend-inner-icon="mdi-clock-start"
                  variant="outlined"
                  :rules="[rules.required]"
                  @update:model-value="recalcularHoraFim"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="form.hora_fim"
                  label="Término previsto"
                  type="time"
                  prepend-inner-icon="mdi-clock-end"
                  variant="outlined"
                  hint="Calculado pela duração"
                  persistent-hint
                ></v-text-field>
              </v-col>

              <!-- Alerta de Conflito de Horário na Agenda -->
              <v-col v-if="conflitoHorario" cols="12" class="pt-0">
                <v-alert
                  type="info"
                  color="accent"
                  variant="tonal"
                  density="compact"
                  icon="mdi-calendar-alert"
                >
                  <span class="text-caption">
                    Nota: Já existe um agendamento neste horário para
                    <strong>{{ conflitoHorario.cliente }}</strong> ({{ conflitoHorario.servico }} das
                    {{ conflitoHorario.hora }} às {{ conflitoHorario.hora_fim }}).
                  </span>
                </v-alert>
              </v-col>

              <!-- Status do Agendamento -->
              <v-col cols="12">
                <v-select
                  v-model="form.status"
                  :items="opcoesStatus.map((s) => s.valor)"
                  label="Status do Agendamento"
                  prepend-inner-icon="mdi-list-status"
                  variant="outlined"
                ></v-select>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="agendamentoDialog = false">
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="salvando"
            :disabled="!formValido"
            @click="salvarAgendamento"
          >
            {{ form.id ? 'Salvar Alterações' : 'Confirmar Agendamento' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================================================================== -->
    <!-- MODAL 3: CONFIRMAÇÃO DE EXCLUSÃO                                      -->
    <!-- ===================================================================== -->
    <v-dialog v-model="deleteDialog" max-width="440px">
      <v-card rounded="lg">
        <v-card-title class="bg-error text-white pa-4">Excluir Agendamento</v-card-title>
        <v-card-text class="pa-6">
          Tem certeza que deseja excluir o agendamento de
          <strong>{{ agendamentoParaExcluir?.cliente }}</strong>
          ({{ agendamentoParaExcluir?.servico }}) no dia
          <strong>{{ formatarDataBr(agendamentoParaExcluir?.data) }}</strong> às
          <strong>{{ agendamentoParaExcluir?.hora }}</strong>?
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            variant="flat"
            :loading="excluindo"
            @click="executarExclusao"
          >
            Sim, Excluir
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar de Feedback -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3500" location="top right">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" @click="snackbar = false"></v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CalendarGrid from '@/components/CalendarGrid.vue'
import { useAgendaStore } from '@/stores/agenda'

const store = useAgendaStore()

// controle de data atual e navegação do calendário
const today = new Date()
const hojeIso = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth())

const monthNames = [
  'janeiro',
  'fevereiro',
  'março',
  'abril',
  'maio',
  'junho',
  'julho',
  'agosto',
  'setembro',
  'outubro',
  'novembro',
  'dezembro',
]

const monthName = computed(() => monthNames[currentMonth.value])

// estados de busca e filtro de status
const termoBusca = ref('')
const filtroStatus = ref('TODOS')

const opcoesStatus = [
  { valor: 'Pendente', cor: 'accent', icone: 'mdi-clock-outline' },
  { valor: 'Confirmado', cor: 'primary', icone: 'mdi-calendar-check' },
  { valor: 'Concluído', cor: 'success', icone: 'mdi-check-decagram' },
  { valor: 'Cancelado', cor: 'grey-darken-1', icone: 'mdi-cancel' },
]

const opcoesFiltroStatus = [
  { valor: 'TODOS', rotulo: 'Todos', cor: 'primary', icone: 'mdi-view-grid-outline' },
  { valor: 'Pendente', rotulo: 'Pendentes', cor: 'accent', icone: 'mdi-clock-outline' },
  { valor: 'Confirmado', rotulo: 'Confirmados', cor: 'primary', icone: 'mdi-calendar-check' },
  { valor: 'Concluído', rotulo: 'Concluídos', cor: 'success', icone: 'mdi-check-decagram' },
  { valor: 'Cancelado', rotulo: 'Cancelados', cor: 'grey-darken-1', icone: 'mdi-cancel' },
]

// eventos filtrados por busca e status
const eventosFiltrados = computed(() => {
  return store.agendamentos.filter((ag) => {
    const passaStatus = filtroStatus.value === 'TODOS' || ag.status === filtroStatus.value
    if (!passaStatus) return false

    if (!termoBusca.value) return true
    const termo = termoBusca.value.toLowerCase().trim()
    return (
      (ag.cliente && ag.cliente.toLowerCase().includes(termo)) ||
      (ag.servico && ag.servico.toLowerCase().includes(termo))
    )
  })
})

// indicadores (KPIs) calculados em tempo real
const agendamentosHoje = computed(() => {
  return store.agendamentos
    .filter((ag) => ag.data === hojeIso && ag.status !== 'Cancelado')
    .sort((a, b) => a.hora.localeCompare(b.hora))
})

const proximoAtendimentoHoje = computed(() => {
  return agendamentosHoje.value.find(
    (ag) => ag.status === 'Pendente' || ag.status === 'Confirmado'
  )
})

const agendamentosDoMes = computed(() => {
  return store.getAgendamentosPorMes(currentYear.value, currentMonth.value)
})

const pendentesOuConfirmadosMes = computed(() => {
  return agendamentosDoMes.value.filter(
    (ag) => ag.status === 'Pendente' || ag.status === 'Confirmado'
  ).length
})

const canceladosMes = computed(() => {
  return agendamentosDoMes.value.filter((ag) => ag.status === 'Cancelado').length
})

const concluidosMes = computed(() => {
  return agendamentosDoMes.value.filter((ag) => ag.status === 'Concluído').length
})

const receitaConcluidaMes = computed(() => {
  return agendamentosDoMes.value
    .filter((ag) => ag.status === 'Concluído')
    .reduce((soma, ag) => {
      const servicoObj = store.servicos.find((s) => s.id === ag.servico_id)
      return soma + (servicoObj?.preco ? Number(servicoObj.preco) : 0)
    }, 0)
})

// estados dos modais
const detalheDialog = ref(false)
const agendamentoSelecionado = ref(null)
const atualizandoStatus = ref(null)

const agendamentoDialog = ref(false)
const formValido = ref(false)
const formRef = ref(null)
const salvando = ref(false)

const padraoForm = () => ({
  id: null,
  cliente_id: null,
  servico_id: null,
  data: hojeIso,
  hora_inicio: '09:00',
  hora_fim: '10:00',
  status: 'Pendente',
})

const form = ref(padraoForm())

const deleteDialog = ref(false)
const agendamentoParaExcluir = ref(null)
const excluindo = ref(false)

// snackbar de notificações
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

function mostrarMensagem(texto, cor = 'success') {
  snackbarText.value = texto
  snackbarColor.value = cor
  snackbar.value = true
}

const rules = {
  required: (v) => (v !== null && v !== undefined && v !== '') || 'Campo obrigatório',
}

// objetos auxiliares computados para os modais
const servicoSelecionadoForm = computed(() => {
  if (!form.value.servico_id) return null
  return store.servicos.find((s) => s.id === form.value.servico_id) || null
})

const clienteDetalhe = computed(() => {
  if (!agendamentoSelecionado.value) return null
  return store.clientes.find((c) => c.id === agendamentoSelecionado.value.cliente_id) || null
})

const servicoDetalhe = computed(() => {
  if (!agendamentoSelecionado.value) return null
  return store.servicos.find((s) => s.id === agendamentoSelecionado.value.servico_id) || null
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

// retorna lista de nomes dos materiais e equipamentos indisponíveis de um serviço
function listarRecursosIndisponiveis(servico) {
  if (!servico) return []
  const indisponiveis = []

  if (Array.isArray(servico.materiais)) {
    servico.materiais.forEach((m) => {
      if (!m.disponivel || m.quantidade <= 0) {
        indisponiveis.push(`${m.nome} (Material)`)
      }
    })
  }

  if (Array.isArray(servico.equipamentos)) {
    servico.equipamentos.forEach((eq) => {
      if (!eq.disponivel || eq.quantidade <= 0) {
        indisponiveis.push(`${eq.nome} (Equipamento)`)
      }
    })
  }

  return indisponiveis
}

// soma a duração do serviço ao horário de início para sugerir o término
function somarMinutosNaHora(horaStr, minutos) {
  if (!horaStr || !horaStr.includes(':')) return ''
  const [h, m] = horaStr.split(':').map(Number)
  const totalMinutos = h * 60 + m + (Number(minutos) || 30)
  const horasFinais = Math.floor(totalMinutos / 60) % 24
  const minutosFinais = totalMinutos % 60
  return `${String(horasFinais).padStart(2, '0')}:${String(minutosFinais).padStart(2, '0')}`
}

function aoSelecionarServico() {
  recalcularHoraFim()
}

function recalcularHoraFim() {
  if (!form.value.hora_inicio) return
  const duracao = servicoSelecionadoForm.value?.duracao_minutos || 30
  form.value.hora_fim = somarMinutosNaHora(form.value.hora_inicio, duracao)
}

// funções de navegação do calendário
function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function irParaHoje() {
  const agora = new Date()
  currentYear.value = agora.getFullYear()
  currentMonth.value = agora.getMonth()
}

// abertura dos modais de criação, detalhes e edição
function abrirNovoAgendamento(dataPreSelecionada = null) {
  form.value = padraoForm()
  if (typeof dataPreSelecionada === 'string' && dataPreSelecionada) {
    form.value.data = dataPreSelecionada
  }
  agendamentoDialog.value = true
}

function abrirDetalhesAgendamento(evento) {
  agendamentoSelecionado.value = evento
  detalheDialog.value = true
}

function abrirEdicaoAgendamento(evento) {
  detalheDialog.value = false
  form.value = {
    id: evento.id,
    cliente_id: evento.cliente_id,
    servico_id: evento.servico_id,
    data: evento.data,
    hora_inicio: evento.hora,
    hora_fim: evento.hora_fim || somarMinutosNaHora(evento.hora, 30),
    status: evento.status || 'Pendente',
  }
  agendamentoDialog.value = true
}

// salva novo agendamento ou atualiza existente
async function salvarAgendamento() {
  if (!formValido.value) return
  salvando.value = true

  try {
    const payload = {
      cliente_id: form.value.cliente_id,
      servico_id: form.value.servico_id,
      data_hora_inicio: `${form.value.data}T${form.value.hora_inicio}:00`,
      status: form.value.status,
    }

    if (form.value.hora_fim) {
      payload.data_hora_fim = `${form.value.data}T${form.value.hora_fim}:00`
    }

    if (form.value.id) {
      await store.atualizarAgendamento(form.value.id, payload)
      mostrarMensagem('Agendamento atualizado com sucesso!')
    } else {
      await store.criarAgendamento(payload)
      mostrarMensagem('Agendamento registrado com sucesso!')
    }

    agendamentoDialog.value = false
  } catch (err) {
    mostrarMensagem(err.message || 'Erro ao salvar agendamento', 'error')
  } finally {
    salvando.value = false
  }
}

// altera rapidamente o status de um agendamento diretamente do modal de detalhes
async function alterarStatusRapido(novoStatus) {
  if (!agendamentoSelecionado.value || agendamentoSelecionado.value.status === novoStatus) return
  atualizandoStatus.value = novoStatus

  try {
    await store.atualizarAgendamento(agendamentoSelecionado.value.id, {
      status: novoStatus,
    })
    const atualizado = store.agendamentos.find((a) => a.id === agendamentoSelecionado.value.id)
    if (atualizado) {
      agendamentoSelecionado.value = atualizado
    }
    mostrarMensagem(`Status alterado para "${novoStatus}"!`)
  } catch (err) {
    mostrarMensagem(err.message || 'Erro ao alterar status', 'error')
  } finally {
    atualizandoStatus.value = null
  }
}

// fluxo de exclusão de agendamento
function confirmarExclusao(evento) {
  agendamentoParaExcluir.value = evento
  detalheDialog.value = false
  deleteDialog.value = true
}

async function executarExclusao() {
  if (!agendamentoParaExcluir.value) return
  excluindo.value = true

  try {
    await store.deletarAgendamento(agendamentoParaExcluir.value.id)
    mostrarMensagem('Agendamento excluído com sucesso!')
    deleteDialog.value = false
    agendamentoParaExcluir.value = null
  } catch (err) {
    mostrarMensagem(err.message || 'Erro ao excluir agendamento', 'error')
  } finally {
    excluindo.value = false
  }
}

// utilitários de formatação
function formatarMoeda(valor) {
  if (valor === null || valor === undefined || valor === '') return '0,00'
  return Number(valor).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

function formatarDataBr(dataIso) {
  if (!dataIso || !dataIso.includes('-')) return dataIso || ''
  const [ano, mes, dia] = dataIso.split('-')
  return `${dia}/${mes}/${ano}`
}

onMounted(async () => {
  try {
    await store.carregarDadosAgenda()
  } catch {
    mostrarMensagem('Não foi possível conectar ao servidor da API.', 'error')
  }
})
</script>
