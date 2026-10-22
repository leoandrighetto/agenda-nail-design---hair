<template>
  <v-container>
    <!-- Cabeçalho da Página -->
    <v-row class="mb-4 align-center">
      <v-col cols="12" md="7">
        <h1 class="text-h4 font-weight-bold text-primary">Serviços & Recursos</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Gerencie os procedimentos do salão e acompanhe em tempo real a disponibilidade de materiais e equipamentos
        </p>
      </v-col>
      <v-col cols="12" md="5" class="d-flex justify-md-end flex-wrap ga-2">
        <v-btn
          color="secondary"
          variant="tonal"
          prepend-icon="mdi-bottle-tonic-plus-outline"
          @click="openMaterialDialog()"
        >
          Novo Material
        </v-btn>
        <v-btn
          color="accent"
          variant="tonal"
          prepend-icon="mdi-hair-dryer-outline"
          @click="openEquipamentoDialog()"
        >
          Novo Equipamento
        </v-btn>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          size="large"
          elevation="2"
          @click="openServicoDialog()"
        >
          Novo Serviço
        </v-btn>
      </v-col>
    </v-row>

    <!-- Cards de Resumo (KPIs) -->
    <v-row class="mb-6">
      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4 border-s-lg border-primary">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Serviços Cadastrados
              </div>
              <div class="text-h4 font-weight-bold text-primary mt-1">
                {{ servicos.length }}
              </div>
              <div class="text-caption mt-1" :class="servicosComFalta > 0 ? 'text-error' : 'text-success'">
                <v-icon size="14" class="mr-1">
                  {{ servicosComFalta > 0 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                </v-icon>
                {{
                  servicosComFalta > 0
                    ? `${servicosComFalta} com recurso em falta`
                    : 'Todos prontos para execução'
                }}
              </div>
            </div>
            <v-avatar color="primary" variant="tonal" size="52">
              <v-icon size="28">mdi-content-cut</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Materiais (Insumos)
              </div>
              <div class="text-h4 font-weight-bold text-accent mt-1">
                {{ materiais.length }}
              </div>
              <div class="text-caption mt-1" :class="materiaisEmFalta > 0 ? 'text-error' : 'text-success'">
                <v-icon size="14" class="mr-1">
                  {{ materiaisEmFalta > 0 ? 'mdi-package-variant-closed-remove' : 'mdi-package-variant-closed-check' }}
                </v-icon>
                {{
                  materiaisEmFalta > 0
                    ? `${materiaisEmFalta} esgotado(s) ou indisponível(is)`
                    : 'Estoque em dia'
                }}
              </div>
            </div>
            <v-avatar color="secondary" variant="tonal" size="52">
              <v-icon size="28" color="primary">mdi-bottle-tonic-plus-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card elevation="2" rounded="lg" class="pa-4">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption text-grey-darken-1 font-weight-medium text-uppercase">
                Equipamentos
              </div>
              <div class="text-h4 font-weight-bold text-accent mt-1">
                {{ equipamentos.length }}
              </div>
              <div class="text-caption mt-1" :class="equipamentosIndisponiveis > 0 ? 'text-warning' : 'text-success'">
                <v-icon size="14" class="mr-1">
                  {{ equipamentosIndisponiveis > 0 ? 'mdi-wrench-clock' : 'mdi-check-decagram' }}
                </v-icon>
                {{
                  equipamentosIndisponiveis > 0
                    ? `${equipamentosIndisponiveis} indisponível(is)`
                    : 'Todos operacionais'
                }}
              </div>
            </div>
            <v-avatar color="accent" variant="tonal" size="52">
              <v-icon size="28">mdi-hair-dryer-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Abas de Navegação -->
    <v-card elevation="2" rounded="lg">
      <v-tabs v-model="activeTab" bg-color="primary" color="white" grow>
        <v-tab value="servicos">
          <v-icon start>mdi-content-cut</v-icon>
          Catálogo de Serviços ({{ servicos.length }})
        </v-tab>
        <v-tab value="materiais">
          <v-icon start>mdi-bottle-tonic-plus-outline</v-icon>
          Materiais & Insumos ({{ materiais.length }})
          <v-badge
            v-if="materiaisEmFalta > 0"
            color="error"
            :content="materiaisEmFalta"
            inline
            class="ml-2"
          ></v-badge>
        </v-tab>
        <v-tab value="equipamentos">
          <v-icon start>mdi-hair-dryer-outline</v-icon>
          Equipamentos ({{ equipamentos.length }})
          <v-badge
            v-if="equipamentosIndisponiveis > 0"
            color="warning"
            :content="equipamentosIndisponiveis"
            inline
            class="ml-2"
          ></v-badge>
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- ABA 1: SERVIÇOS -->
        <v-window-item value="servicos">
          <v-data-table
            :headers="servicoHeaders"
            :items="servicos"
            :loading="loading"
            hover
            class="bg-surface"
          >
            <template v-slot:item.nome="{ item }">
              <div class="py-2">
                <div class="font-weight-bold text-body-1 text-primary">{{ item.nome }}</div>
                <div v-if="item.descricao" class="text-caption text-grey-darken-1">
                  {{ item.descricao }}
                </div>
              </div>
            </template>

            <template v-slot:item.duracao_minutos="{ item }">
              <v-chip size="small" color="accent" variant="tonal" prepend-icon="mdi-clock-outline">
                {{ formatDuration(item.duracao_minutos) }}
              </v-chip>
            </template>

            <template v-slot:item.preco="{ item }">
              <span class="font-weight-bold text-body-2">
                {{ formatCurrency(item.preco) }}
              </span>
            </template>

            <template v-slot:item.recursos="{ item }">
              <div class="py-2 d-flex flex-wrap ga-1">
                <span
                  v-if="(!item.materiais || !item.materiais.length) && (!item.equipamentos || !item.equipamentos.length)"
                  class="text-caption text-grey"
                >
                  Nenhum recurso exigido
                </span>

                <!-- Chips de Materiais -->
                <v-chip
                  v-for="mat in item.materiais"
                  :key="'mat-' + mat.id"
                  size="small"
                  :color="isResourceAvailable(mat) ? 'success' : 'error'"
                  :variant="isResourceAvailable(mat) ? 'tonal' : 'flat'"
                  :prepend-icon="isResourceAvailable(mat) ? 'mdi-bottle-tonic-outline' : 'mdi-alert-circle'"
                >
                  {{ mat.nome }} ({{ mat.quantidade }})
                  <v-tooltip activator="parent" location="top">
                    Material: {{ isResourceAvailable(mat) ? `Disponível (${mat.quantidade} em estoque)` : 'EM FALTA NO ESTOQUE!' }}
                  </v-tooltip>
                </v-chip>

                <!-- Chips de Equipamentos -->
                <v-chip
                  v-for="eq in item.equipamentos"
                  :key="'eq-' + eq.id"
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

            <template v-slot:item.status_estoque="{ item }">
              <v-chip
                size="small"
                :color="item.recursos_disponiveis ? 'success' : 'error'"
                variant="flat"
                :prepend-icon="item.recursos_disponiveis ? 'mdi-check-circle' : 'mdi-close-circle'"
              >
                {{ item.recursos_disponiveis ? 'Pronto p/ Executar' : 'Recurso em Falta' }}
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn icon variant="text" size="small" color="primary" @click="openServicoDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Serviço</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('servico', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Serviço</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhum serviço cadastrado ainda. Clique em "Novo Serviço" para cadastrar o primeiro procedimento.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ABA 2: MATERIAIS -->
        <v-window-item value="materiais">
          <v-data-table
            :headers="recursoHeaders"
            :items="materiais"
            :loading="loading"
            hover
            class="bg-surface"
          >
            <template v-slot:item.nome="{ item }">
              <div class="font-weight-bold text-primary">{{ item.nome }}</div>
            </template>

            <template v-slot:item.quantidade="{ item }">
              <div class="d-flex align-center ga-2">
                <v-btn
                  icon="mdi-minus"
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  :disabled="item.quantidade <= 0"
                  @click="adjustQuantity('materiais', item, -1)"
                ></v-btn>
                <span class="font-weight-bold text-body-1 px-2" :class="item.quantidade <= 0 ? 'text-error' : ''">
                  {{ item.quantidade }}
                </span>
                <v-btn
                  icon="mdi-plus"
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  @click="adjustQuantity('materiais', item, 1)"
                ></v-btn>
              </div>
            </template>

            <template v-slot:item.disponivel="{ item }">
              <v-chip
                size="small"
                :color="isResourceAvailable(item) ? 'success' : 'error'"
                variant="flat"
                class="cursor-pointer"
                @click="toggleAvailability('materiais', item)"
              >
                <v-icon start size="16">
                  {{ isResourceAvailable(item) ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                </v-icon>
                {{ isResourceAvailable(item) ? 'Disponível' : 'Em Falta / Esgotado' }}
                <v-tooltip activator="parent" location="top">
                  Clique para alternar a disponibilidade
                </v-tooltip>
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn icon variant="text" size="small" color="primary" @click="openMaterialDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Material</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('material', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Material</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhum material cadastrado ainda. Clique em "Novo Material" para adicionar itens como pó descolorante, esmaltes, etc.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ABA 3: EQUIPAMENTOS -->
        <v-window-item value="equipamentos">
          <v-data-table
            :headers="recursoHeaders"
            :items="equipamentos"
            :loading="loading"
            hover
            class="bg-surface"
          >
            <template v-slot:item.nome="{ item }">
              <div class="font-weight-bold text-primary">{{ item.nome }}</div>
            </template>

            <template v-slot:item.quantidade="{ item }">
              <div class="d-flex align-center ga-2">
                <v-btn
                  icon="mdi-minus"
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  :disabled="item.quantidade <= 0"
                  @click="adjustQuantity('equipamentos', item, -1)"
                ></v-btn>
                <span class="font-weight-bold text-body-1 px-2" :class="item.quantidade <= 0 ? 'text-error' : ''">
                  {{ item.quantidade }}
                </span>
                <v-btn
                  icon="mdi-plus"
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  @click="adjustQuantity('equipamentos', item, 1)"
                ></v-btn>
              </div>
            </template>

            <template v-slot:item.disponivel="{ item }">
              <v-chip
                size="small"
                :color="isResourceAvailable(item) ? 'success' : 'error'"
                variant="flat"
                class="cursor-pointer"
                @click="toggleAvailability('equipamentos', item)"
              >
                <v-icon start size="16">
                  {{ isResourceAvailable(item) ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                </v-icon>
                {{ isResourceAvailable(item) ? 'Operacional' : 'Indisponível' }}
                <v-tooltip activator="parent" location="top">
                  Clique para alternar a disponibilidade
                </v-tooltip>
              </v-chip>
            </template>

            <template v-slot:item.acoes="{ item }">
              <div class="d-flex justify-end">
                <v-btn icon variant="text" size="small" color="primary" @click="openEquipamentoDialog(item)">
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">Editar Equipamento</v-tooltip>
                </v-btn>
                <v-btn icon variant="text" size="small" color="error" @click="confirmDelete('equipamento', item)">
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">Excluir Equipamento</v-tooltip>
                </v-btn>
              </div>
            </template>

            <template v-slot:no-data>
              <v-alert type="info" variant="tonal" class="ma-4">
                Nenhum equipamento cadastrado ainda. Clique em "Novo Equipamento" para adicionar secadores, pranchas, pincéis, etc.
              </v-alert>
            </template>
          </v-data-table>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- MODAL: CRIAR / EDITAR SERVIÇO -->
    <v-dialog v-model="servicoDialog" max-width="680px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-content-cut</v-icon>
          <span class="text-h5">{{ servicoForm.id ? 'Editar Serviço' : 'Novo Serviço' }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" @click="servicoDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="servicoFormRef" v-model="servicoValid" @submit.prevent="saveServico">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="servicoForm.nome"
                  label="Nome do Serviço *"
                  :rules="[v => !!v || 'O nome do serviço é obrigatório']"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-content-cut"
                  placeholder="Ex: Mechas, Manicure, Corte"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="6" sm="3">
                <v-text-field
                  v-model.number="servicoForm.duracao_minutos"
                  label="Duração (min) *"
                  type="number"
                  min="5"
                  step="5"
                  :rules="[v => (v && v > 0) || 'Informe a duração']"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-clock-outline"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="6" sm="3">
                <v-text-field
                  v-model.number="servicoForm.preco"
                  label="Preço (R$)"
                  type="number"
                  min="0"
                  step="0.01"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-currency-brl"
                  placeholder="0,00"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="servicoForm.descricao"
                  label="Descrição e Detalhes de Execução"
                  variant="outlined"
                  color="primary"
                  rows="2"
                  prepend-inner-icon="mdi-text-box-outline"
                  placeholder="Descreva etapas ou observações importantes deste procedimento..."
                ></v-textarea>
              </v-col>

              <!-- Seleção de Materiais com status de estoque embutido -->
              <v-col cols="12">
                <div class="d-flex justify-space-between align-center mb-1">
                  <span class="text-subtitle-2 text-primary font-weight-bold">
                    Materiais Necessários para Execução
                  </span>
                  <v-btn
                    size="x-small"
                    color="primary"
                    variant="text"
                    prepend-icon="mdi-plus"
                    @click="openMaterialDialog()"
                  >
                    Cadastrar Material
                  </v-btn>
                </div>
                <v-autocomplete
                  v-model="servicoForm.materiais_ids"
                  :items="materiais"
                  item-title="nome"
                  item-value="id"
                  label="Selecione os materiais (ex: pó descolorante, esmalte)"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-bottle-tonic-plus-outline"
                  multiple
                  chips
                  closable-chips
                  clearable
                >
                  <template v-slot:chip="{ props, item }">
                    <v-chip
                      v-bind="props"
                      :color="isResourceAvailable(item.raw) ? 'success' : 'error'"
                      :variant="isResourceAvailable(item.raw) ? 'tonal' : 'flat'"
                    >
                      {{ item.raw.nome }} ({{ item.raw.quantidade }})
                    </v-chip>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :subtitle="item.raw.descricao || 'Sem descrição'">
                      <template v-slot:append>
                        <v-chip
                          size="x-small"
                          :color="isResourceAvailable(item.raw) ? 'success' : 'error'"
                          variant="flat"
                        >
                          {{ isResourceAvailable(item.raw) ? `Estoque: ${item.raw.quantidade}` : 'Em falta' }}
                        </v-chip>
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <!-- Seleção de Equipamentos com status de disponibilidade embutido -->
              <v-col cols="12">
                <div class="d-flex justify-space-between align-center mb-1">
                  <span class="text-subtitle-2 text-primary font-weight-bold">
                    Equipamentos Necessários para Execução
                  </span>
                  <v-btn
                    size="x-small"
                    color="primary"
                    variant="text"
                    prepend-icon="mdi-plus"
                    @click="openEquipamentoDialog()"
                  >
                    Cadastrar Equipamento
                  </v-btn>
                </div>
                <v-autocomplete
                  v-model="servicoForm.equipamentos_ids"
                  :items="equipamentos"
                  item-title="nome"
                  item-value="id"
                  label="Selecione os equipamentos (ex: secador, pincel, cabine)"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-hair-dryer-outline"
                  multiple
                  chips
                  closable-chips
                  clearable
                >
                  <template v-slot:chip="{ props, item }">
                    <v-chip
                      v-bind="props"
                      :color="isResourceAvailable(item.raw) ? 'primary' : 'error'"
                      :variant="isResourceAvailable(item.raw) ? 'tonal' : 'flat'"
                    >
                      {{ item.raw.nome }} ({{ item.raw.quantidade }})
                    </v-chip>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :subtitle="item.raw.descricao || 'Sem descrição'">
                      <template v-slot:append>
                        <v-chip
                          size="x-small"
                          :color="isResourceAvailable(item.raw) ? 'success' : 'error'"
                          variant="flat"
                        >
                          {{ isResourceAvailable(item.raw) ? `Disp: ${item.raw.quantidade}` : 'Indisponível' }}
                        </v-chip>
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <!-- Alerta Inteligente em Tempo Real sobre itens em falta -->
              <v-col cols="12" v-if="recursosFaltantesNoFormulario.length > 0">
                <v-alert
                  type="warning"
                  variant="tonal"
                  border="start"
                  prominent
                  icon="mdi-alert-outline"
                >
                  <div class="font-weight-bold">Atenção ao Estoque!</div>
                  <div class="text-body-2 mt-1">
                    Os seguintes itens selecionados para este serviço estão <strong>em falta ou indisponíveis</strong> no momento:
                    <strong>{{ recursosFaltantesNoFormulario.join(', ') }}</strong>.
                  </div>
                </v-alert>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" size="large" @click="servicoDialog = false">
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            size="large"
            :disabled="!servicoValid"
            :loading="saving"
            @click="saveServico"
          >
            Salvar Serviço
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- MODAL: CRIAR / EDITAR MATERIAL -->
    <v-dialog v-model="materialDialog" max-width="500px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <v-icon start>mdi-bottle-tonic-plus-outline</v-icon>
          <span class="text-h5">{{ materialForm.id ? 'Editar Material' : 'Novo Material' }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" @click="materialDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="materialFormRef" v-model="materialValid" @submit.prevent="saveMaterial">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="materialForm.nome"
                  label="Nome do Material *"
                  :rules="[v => !!v || 'O nome do material é obrigatório']"
                  variant="outlined"
                  color="primary"
                  placeholder="Ex: Pó Descolorante, Água Oxigenada, Esmalte Gel"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="materialForm.quantidade"
                  label="Quantidade em Estoque *"
                  type="number"
                  min="0"
                  variant="outlined"
                  color="primary"
                  @update:model-value="val => materialForm.disponivel = val > 0"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" class="d-flex align-center">
                <v-switch
                  v-model="materialForm.disponivel"
                  color="success"
                  :label="materialForm.disponivel ? 'Disponível' : 'Em falta'"
                  hide-details
                  inset
                ></v-switch>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="materialForm.descricao"
                  label="Descrição / Marca / Observações"
                  variant="outlined"
                  color="primary"
                  rows="2"
                  placeholder="Ex: Pote 500g, usar luvas..."
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="materialDialog = false">Cancelar</v-btn>
          <v-btn color="primary" variant="flat" :disabled="!materialValid" :loading="saving" @click="saveMaterial">
            Salvar Material
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- MODAL: CRIAR / EDITAR EQUIPAMENTO -->
    <v-dialog v-model="equipamentoDialog" max-width="500px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-accent text-white pa-4 d-flex align-center">
          <v-icon start>mdi-hair-dryer-outline</v-icon>
          <span class="text-h5">{{ equipamentoForm.id ? 'Editar Equipamento' : 'Novo Equipamento' }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" @click="equipamentoDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="equipamentoFormRef" v-model="equipamentoValid" @submit.prevent="saveEquipamento">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="equipamentoForm.nome"
                  label="Nome do Equipamento *"
                  :rules="[v => !!v || 'O nome do equipamento é obrigatório']"
                  variant="outlined"
                  color="primary"
                  placeholder="Ex: Secador Taiff, Pincel de Mechas, Cabine LED"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="equipamentoForm.quantidade"
                  label="Quantidade *"
                  type="number"
                  min="0"
                  variant="outlined"
                  color="primary"
                  @update:model-value="val => equipamentoForm.disponivel = val > 0"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" class="d-flex align-center">
                <v-switch
                  v-model="equipamentoForm.disponivel"
                  color="success"
                  :label="equipamentoForm.disponivel ? 'Operacional' : 'Indisponível'"
                  hide-details
                  inset
                ></v-switch>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="equipamentoForm.descricao"
                  label="Descrição / Especificações"
                  variant="outlined"
                  color="primary"
                  rows="2"
                  placeholder="Ex: 2200W, gaveta 2..."
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="equipamentoDialog = false">Cancelar</v-btn>
          <v-btn color="primary" variant="flat" :disabled="!equipamentoValid" :loading="saving" @click="saveEquipamento">
            Salvar Equipamento
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- MODAL DE CONFIRMAÇÃO DE EXCLUSÃO -->
    <v-dialog v-model="deleteDialog" max-width="450px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-error text-white pa-4">Confirmar Exclusão</v-card-title>
        <v-card-text class="pa-6">
          Tem certeza que deseja excluir <strong>{{ deleteTarget.nome }}</strong>? Esta ação não pode ser desfeita.
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="error" variant="flat" :loading="saving" @click="executeDelete">Sim, Excluir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar de Feedback -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" location="top right">
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
import { ref, computed, onMounted } from 'vue'

const apiBase = 'http://127.0.0.1:5000/api'

// Aba ativa e estados gerais
const activeTab = ref('servicos')
const loading = ref(false)
const saving = ref(false)

// Listas de dados vindas do Backend
const servicos = ref([])
const materiais = ref([])
const equipamentos = ref([])

// Cabeçalhos das tabelas
const servicoHeaders = [
  { title: 'Procedimento / Descrição', key: 'nome', align: 'start', sortable: true },
  { title: 'Duração', key: 'duracao_minutos', sortable: true, width: '130px' },
  { title: 'Valor', key: 'preco', sortable: true, width: '120px' },
  { title: 'Materiais & Equipamentos Necessários', key: 'recursos', sortable: false },
  { title: 'Disponibilidade', key: 'status_estoque', sortable: false, width: '180px' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'end', width: '110px' },
]

const recursoHeaders = [
  { title: 'Nome', key: 'nome', align: 'start', sortable: true },
  { title: 'Descrição / Detalhes', key: 'descricao', sortable: false },
  { title: 'Quantidade', key: 'quantidade', sortable: true, width: '160px' },
  { title: 'Status no Estoque', key: 'disponivel', sortable: true, width: '200px' },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'end', width: '110px' },
]

// Estados dos Modais e Formulários
const servicoDialog = ref(false)
const servicoValid = ref(false)
const servicoFormRef = ref(null)
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

const materialDialog = ref(false)
const materialValid = ref(false)
const materialFormRef = ref(null)
const defaultMaterial = {
  id: null,
  nome: '',
  descricao: '',
  quantidade: 1,
  disponivel: true,
}
const materialForm = ref({ ...defaultMaterial })

const equipamentoDialog = ref(false)
const equipamentoValid = ref(false)
const equipamentoFormRef = ref(null)
const defaultEquipamento = {
  id: null,
  nome: '',
  descricao: '',
  quantidade: 1,
  disponivel: true,
}
const equipamentoForm = ref({ ...defaultEquipamento })

// Exclusão
const deleteDialog = ref(false)
const deleteTarget = ref({ type: '', id: null, nome: '' })

// Notificações (Snackbar)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const showMessage = (text, color = 'success') => {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

// Funções auxiliares de formatação e verificação
const isResourceAvailable = (item) => {
  return Boolean(item && item.disponivel && item.quantidade > 0)
}

const formatCurrency = (val) => {
  if (val === null || val === undefined || val === '') return 'A consultar'
  return Number(val).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const formatDuration = (mins) => {
  if (!mins) return '30 min'
  if (mins < 60) return `${mins} min`
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return m > 0 ? `${h}h ${m}min` : `${h}h`
}

// Indicadores computados (KPIs)
const servicosComFalta = computed(() => {
  return servicos.value.filter(s => !s.recursos_disponiveis).length
})

const materiaisEmFalta = computed(() => {
  return materiais.value.filter(m => !isResourceAvailable(m)).length
})

const equipamentosIndisponiveis = computed(() => {
  return equipamentos.value.filter(e => !isResourceAvailable(e)).length
})

// Verifica em tempo real no formulário do Serviço se algum recurso escolhido está em falta
const recursosFaltantesNoFormulario = computed(() => {
  const faltantes = []
  for (const id of servicoForm.value.materiais_ids || []) {
    const mat = materiais.value.find(m => m.id === id)
    if (mat && !isResourceAvailable(mat)) {
      faltantes.push(`${mat.nome} (Material)`)
    }
  }
  for (const id of servicoForm.value.equipamentos_ids || []) {
    const eq = equipamentos.value.find(e => e.id === id)
    if (eq && !isResourceAvailable(eq)) {
      faltantes.push(`${eq.nome} (Equipamento)`)
    }
  }
  return faltantes
})

// Carregamento de dados da API
const fetchAllData = async () => {
  loading.value = true
  try {
    const [resServ, resMat, resEq] = await Promise.all([
      fetch(`${apiBase}/servicos`),
      fetch(`${apiBase}/materiais`),
      fetch(`${apiBase}/equipamentos`),
    ])

    if (resServ.ok) servicos.value = await resServ.json()
    if (resMat.ok) materiais.value = await resMat.json()
    if (resEq.ok) equipamentos.value = await resEq.json()
  } catch (error) {
    showMessage('Erro de conexão com o servidor Flask', 'error')
  } finally {
    loading.value = false
  }
}

// Ações de Serviços
const openServicoDialog = (item = null) => {
  if (item) {
    servicoForm.value = {
      id: item.id,
      nome: item.nome,
      descricao: item.descricao || '',
      duracao_minutos: item.duracao_minutos || 30,
      preco: item.preco,
      materiais_ids: (item.materiais || []).map(m => m.id),
      equipamentos_ids: (item.equipamentos || []).map(e => e.id),
    }
  } else {
    servicoForm.value = { ...defaultServico, materiais_ids: [], equipamentos_ids: [] }
  }
  servicoDialog.value = true
}

const saveServico = async () => {
  if (!servicoFormRef.value) return
  const { valid } = await servicoFormRef.value.validate()
  if (!valid) return

  saving.value = true
  const isEdit = Boolean(servicoForm.value.id)
  const url = isEdit ? `${apiBase}/servicos/${servicoForm.value.id}` : `${apiBase}/servicos`
  const method = isEdit ? 'PUT' : 'POST'

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(servicoForm.value),
    })

    if (res.ok) {
      showMessage(`Serviço ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      servicoDialog.value = false
      await fetchAllData()
    } else {
      const err = await res.json()
      showMessage(err.erro || 'Erro ao salvar serviço', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão ao salvar serviço', 'error')
  } finally {
    saving.value = false
  }
}

// Ações de Materiais
const openMaterialDialog = (item = null) => {
  if (item) {
    materialForm.value = { ...item }
  } else {
    materialForm.value = { ...defaultMaterial }
  }
  materialDialog.value = true
}

const saveMaterial = async () => {
  if (!materialFormRef.value) return
  const { valid } = await materialFormRef.value.validate()
  if (!valid) return

  saving.value = true
  const isEdit = Boolean(materialForm.value.id)
  const url = isEdit ? `${apiBase}/materiais/${materialForm.value.id}` : `${apiBase}/materiais`
  const method = isEdit ? 'PUT' : 'POST'

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(materialForm.value),
    })

    if (res.ok) {
      const data = await res.json()
      showMessage(`Material ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      materialDialog.value = false
      await fetchAllData()
      // se o modal de serviço estiver aberto e for um novo material, já adiciona na seleção
      if (servicoDialog.value && !isEdit && data.id) {
        servicoForm.value.materiais_ids.push(data.id)
      }
    } else {
      const err = await res.json()
      showMessage(err.erro || 'Erro ao salvar material', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão ao salvar material', 'error')
  } finally {
    saving.value = false
  }
}

// Ações de Equipamentos
const openEquipamentoDialog = (item = null) => {
  if (item) {
    equipamentoForm.value = { ...item }
  } else {
    equipamentoForm.value = { ...defaultEquipamento }
  }
  equipamentoDialog.value = true
}

const saveEquipamento = async () => {
  if (!equipamentoFormRef.value) return
  const { valid } = await equipamentoFormRef.value.validate()
  if (!valid) return

  saving.value = true
  const isEdit = Boolean(equipamentoForm.value.id)
  const url = isEdit ? `${apiBase}/equipamentos/${equipamentoForm.value.id}` : `${apiBase}/equipamentos`
  const method = isEdit ? 'PUT' : 'POST'

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(equipamentoForm.value),
    })

    if (res.ok) {
      const data = await res.json()
      showMessage(`Equipamento ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso!`)
      equipamentoDialog.value = false
      await fetchAllData()
      // se o modal de serviço estiver aberto e for um novo equipamento, já adiciona na seleção
      if (servicoDialog.value && !isEdit && data.id) {
        servicoForm.value.equipamentos_ids.push(data.id)
      }
    } else {
      const err = await res.json()
      showMessage(err.erro || 'Erro ao salvar equipamento', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão ao salvar equipamento', 'error')
  } finally {
    saving.value = false
  }
}

// Ajuste rápido de quantidade (+ / -) e disponibilidade direto na tabela
const adjustQuantity = async (endpoint, item, delta) => {
  const novaQtd = Math.max(0, (item.quantidade || 0) + delta)
  const novoDisponivel = novaQtd > 0 ? item.disponivel : false

  try {
    const res = await fetch(`${apiBase}/${endpoint}/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        quantidade: novaQtd,
        disponivel: novoDisponivel,
      }),
    })
    if (res.ok) {
      await fetchAllData()
    }
  } catch (error) {
    showMessage('Erro ao atualizar quantidade', 'error')
  }
}

const toggleAvailability = async (endpoint, item) => {
  const novoStatus = !item.disponivel
  const novaQtd = novoStatus && item.quantidade === 0 ? 1 : item.quantidade

  try {
    const res = await fetch(`${apiBase}/${endpoint}/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        disponivel: novoStatus,
        quantidade: novaQtd,
      }),
    })
    if (res.ok) {
      await fetchAllData()
      showMessage('Disponibilidade atualizada!')
    }
  } catch (error) {
    showMessage('Erro ao alternar disponibilidade', 'error')
  }
}

// Exclusão unificada
const confirmDelete = (type, item) => {
  deleteTarget.value = { type, id: item.id, nome: item.nome }
  deleteDialog.value = true
}

const executeDelete = async () => {
  saving.value = true
  const endpointsMap = {
    servico: 'servicos',
    material: 'materiais',
    equipamento: 'equipamentos',
  }
  const endpoint = endpointsMap[deleteTarget.value.type]

  try {
    const res = await fetch(`${apiBase}/${endpoint}/${deleteTarget.value.id}`, {
      method: 'DELETE',
    })
    if (res.ok) {
      showMessage('Registro excluído com sucesso!')
      deleteDialog.value = false
      await fetchAllData()
    } else {
      showMessage('Erro ao excluir registro', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão ao excluir', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchAllData()
})
</script>

<style scoped>
.v-btn {
  text-transform: none;
  letter-spacing: 0.4px;
}
.cursor-pointer {
  cursor: pointer;
}
</style>

