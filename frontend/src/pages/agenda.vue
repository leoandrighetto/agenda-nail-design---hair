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
          <v-form ref="formRef" v-model="formValido" autocomplete="off" @submit.prevent="salvarAgendamento">
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
                  clearable
                  autocomplete="off"
                  :input-props="{
                    autocomplete: 'off',
                    autocorrect: 'off',
                    autocapitalize: 'off',
                    spellcheck: false,
                  }"
                  :loading="carregandoClientes"
                  :rules="[rules.required]"
                  no-data-text="Nenhum cliente encontrado"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item.nome"
                      :subtitle="item.telefone || 'Sem telefone'"
                    ></v-list-item>
                  </template>
                  <template v-slot:append-item>
                    <v-divider class="my-1"></v-divider>
                    <v-list-item
                      class="text-primary font-weight-bold"
                      prepend-icon="mdi-account-plus"
                      title="Cadastrar novo cliente"
                      @click="modalNovoCliente = true"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <!-- Seleção de Procedimento -->
              <v-col cols="12">
                <v-autocomplete
                  v-model="form.servico_id"
                  :items="store.servicos"
                  item-title="nome"
                  item-value="id"
                  label="Procedimento *"
                  placeholder="Selecione o procedimento..."
                  prepend-inner-icon="mdi-content-cut"
                  variant="outlined"
                  clearable
                  autocomplete="off"
                  :input-props="{
                    autocomplete: 'off',
                    autocorrect: 'off',
                    autocapitalize: 'off',
                    spellcheck: false,
                  }"
                  :loading="carregandoProcedimentos"
                  :rules="[rules.required]"
                  no-data-text="Nenhum procedimento cadastrado"
                  @update:model-value="aoSelecionarServico"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.nome">
                      <template v-slot:subtitle>
                        <span>
                          {{ item.duracao_minutos || 30 }} min • R$
                          {{ formatarMoeda(item.preco) }}
                        </span>
                      </template>
                      <template v-slot:append>
                        <v-chip
                          :color="item.recursos_disponiveis ? 'success' : 'warning'"
                          size="x-small"
                          variant="tonal"
                        >
                          {{
                            item.recursos_disponiveis ? 'Estoque OK' : 'Recurso em falta'
                          }}
                        </v-chip>
                      </template>
                    </v-list-item>
                  </template>
                  <template v-slot:append-item>
                    <v-divider class="my-1"></v-divider>
                    <v-list-item
                      class="text-primary font-weight-bold"
                      prepend-icon="mdi-plus-circle-outline"
                      title="Cadastrar novo procedimento"
                      @click="modalNovoProcedimento = true"
                    ></v-list-item>
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
                <CampoDataHora
                  v-model="form.data"
                  tipo="date"
                  label="Data *"
                  variant="outlined"
                  :rules="[rules.required]"
                />
              </v-col>

              <v-col cols="12" sm="4">
                <CampoDataHora
                  v-model="form.hora_inicio"
                  tipo="time"
                  label="Início *"
                  variant="outlined"
                  :rules="[rules.required]"
                  @update:model-value="recalcularHoraFim"
                />
              </v-col>

              <v-col cols="12" sm="4">
                <CampoDataHora
                  v-model="form.hora_fim"
                  tipo="time"
                  label="Término previsto"
                  variant="outlined"
                  hint="Calculado pela duração"
                  persistent-hint
                />
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

    <!-- Modal Rápido: Novo Cliente -->
    <ModalNovoCliente
      v-model="modalNovoCliente"
      @salvo="aoSalvarNovoCliente"
    />

    <!-- Modal Rápido: Novo Procedimento -->
    <ModalNovoProcedimento
      v-model="modalNovoProcedimento"
      @salvo="aoSalvarNovoProcedimento"
    />

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
import { ref, computed, onMounted, nextTick } from 'vue'
import CalendarGrid from '@/components/CalendarGrid.vue'
import CampoDataHora from '@/components/CampoDataHora.vue'
import ModalNovoCliente from '@/components/ModalNovoCliente.vue'
import ModalNovoProcedimento from '@/components/ModalNovoProcedimento.vue'
import { useAgendaStore } from '@/stores/agenda'
import { useAgendaCalendar } from '@/composables/agenda/useAgendaCalendar'
import { useAgendamentoForm } from '@/composables/agenda/useAgendamentoForm'
import { useSnackbar } from '@/composables/shared/useSnackbar'
import { formatarMoeda, formatarDataBr } from '@/utils/shared/formatters'
import { listarRecursosIndisponiveis } from '@/utils/estoque/estoqueUtils'

const store = useAgendaStore()

// notificações visuais compartilhadas
const { snackbar, snackbarText, snackbarColor, mostrarMensagem } = useSnackbar()

// navegação de calendário, busca/filtros reativos e KPIs da agenda
const {
  hojeIso,
  currentYear,
  currentMonth,
  monthName,
  termoBusca,
  filtroStatus,
  eventosFiltrados,
  agendamentosHoje,
  proximoAtendimentoHoje,
  agendamentosDoMes,
  pendentesOuConfirmadosMes,
  canceladosMes,
  concluidosMes,
  receitaConcluidaMes,
  prevMonth,
  nextMonth,
  irParaHoje,
} = useAgendaCalendar(store)

// formulário de agendamento, conflito de horário e ações de persistência
const {
  form,
  salvando,
  excluindo,
  atualizandoStatus,
  rules,
  servicoSelecionadoForm,
  conflitoHorario,
  recalcularHoraFim,
  aoSelecionarServico,
  iniciarNovoForm,
  preencherFormEdicao,
  salvarAgendamento: persistirAgendamento,
  alterarStatusRapido: persistirStatusRapido,
  executarExclusao: persistirExclusao,
} = useAgendamentoForm(store, hojeIso, mostrarMensagem)

// opções visuais de status e filtros da UI
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

// estados puramente visuais/UI locais dos modais
const detalheDialog = ref(false)
const agendamentoSelecionado = ref(null)

const agendamentoDialog = ref(false)
const formValido = ref(false)
const formRef = ref(null)

const deleteDialog = ref(false)
const agendamentoParaExcluir = ref(null)

// controle dos modais rápidos de criação e loading reativo dos selects
const modalNovoCliente = ref(false)
const modalNovoProcedimento = ref(false)
const carregandoClientes = ref(false)
const carregandoProcedimentos = ref(false)

async function aoSalvarNovoCliente(clienteCriado) {
  carregandoClientes.value = true
  try {
    await store.fetchClientes()
    if (clienteCriado?.id) {
      form.value.cliente_id = clienteCriado.id
    }
    mostrarMensagem(`Cliente "${clienteCriado.nome}" cadastrado com sucesso!`)
  } catch (err) {
    mostrarMensagem(err.message || 'Erro ao atualizar lista de clientes', 'error')
  } finally {
    carregandoClientes.value = false
  }
}

async function aoSalvarNovoProcedimento(procedimentoCriado) {
  carregandoProcedimentos.value = true
  try {
    await store.fetchServicos()
    if (procedimentoCriado?.id) {
      form.value.servico_id = procedimentoCriado.id
      await nextTick()
      aoSelecionarServico()
    }
    mostrarMensagem(`Procedimento "${procedimentoCriado.nome}" cadastrado com sucesso!`)
  } catch (err) {
    mostrarMensagem(err.message || 'Erro ao atualizar catálogo de procedimentos', 'error')
  } finally {
    carregandoProcedimentos.value = false
  }
}

// objetos auxiliares para exibição no modal de detalhes
const clienteDetalhe = computed(() => {
  if (!agendamentoSelecionado.value) return null
  return store.clientes.find((c) => c.id === agendamentoSelecionado.value.cliente_id) || null
})

const servicoDetalhe = computed(() => {
  if (!agendamentoSelecionado.value) return null
  return store.servicos.find((s) => s.id === agendamentoSelecionado.value.servico_id) || null
})

// abertura e controle dos modais
function abrirNovoAgendamento(dataPreSelecionada = null) {
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

async function salvarAgendamento() {
  if (!formValido.value) return
  const sucesso = await persistirAgendamento()
  if (sucesso) {
    agendamentoDialog.value = false
  }
}

async function alterarStatusRapido(novoStatus) {
  const atualizado = await persistirStatusRapido(agendamentoSelecionado.value, novoStatus)
  if (atualizado) {
    agendamentoSelecionado.value = atualizado
  }
}

function confirmarExclusao(evento) {
  agendamentoParaExcluir.value = evento
  detalheDialog.value = false
  deleteDialog.value = true
}

async function executarExclusao() {
  if (!agendamentoParaExcluir.value) return
  const sucesso = await persistirExclusao(agendamentoParaExcluir.value.id)
  if (sucesso) {
    deleteDialog.value = false
    agendamentoParaExcluir.value = null
  }
}

onMounted(async () => {
  try {
    await store.carregarDadosAgenda()
  } catch {
    mostrarMensagem('Não foi possível conectar ao servidor da API.', 'error')
  }
})
</script>
