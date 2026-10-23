<template>
  <v-container>
    <v-row class="mb-4 align-center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-primary">Minhas Clientes</h1>
        <p class="text-subtitle-1 text-grey-darken-1">Gerencie as clientes do salão</p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openDialog" size="large" elevation="2">
          Novo Cliente
        </v-btn>
      </v-col>
    </v-row>

    <!-- Tabela de Clientes -->
    <v-card elevation="2" rounded="lg">
      <v-data-table
        :headers="headers"
        :items="clientes"
        :loading="loading"
        hover
        class="bg-surface"
      >
        <template v-slot:item.acoes="{ item }">
          <div class="d-flex justify-end">
            <v-btn icon variant="text" size="small" color="primary" @click="editItem(item)">
              <v-icon>mdi-pencil</v-icon>
              <v-tooltip activator="parent" location="top">Editar</v-tooltip>
            </v-btn>
            <v-btn icon variant="text" size="small" color="error" @click="deleteItem(item)">
              <v-icon>mdi-delete</v-icon>
              <v-tooltip activator="parent" location="top">Excluir</v-tooltip>
            </v-btn>
          </div>
        </template>
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="ma-4">Nenhum cliente cadastrado ainda. Clique em "Novo Cliente" para começar.</v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Modal de Cadastro/Edição -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-primary text-white pa-4 d-flex align-center">
          <span class="text-h5">{{ formTitle }}</span>
          <v-spacer></v-spacer>
          <v-btn icon variant="text" @click="close">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="form" v-model="valid" @submit.prevent="save">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.nome"
                  label="Nome completo *"
                  :rules="nameRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  :model-value="editedItem.telefone"
                  @update:model-value="val => editedItem.telefone = formatPhone(val)"
                  label="Telefone *"
                  :rules="phoneRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-phone"
                  placeholder="(00) 00000-0000"
                  required
                  maxlength="15"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  :model-value="editedItem.cpf"
                  @update:model-value="val => editedItem.cpf = formatCPF(val)"
                  label="CPF"
                  :rules="cpfRules"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-card-account-details"
                  placeholder="000.000.000-00"
                  maxlength="14"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.email"
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
                  v-model="editedItem.endereco"
                  v-model:search="addressSearch"
                  :items="addressSuggestions"
                  :loading="addressLoading"
                  item-title="formatted_address"
                  item-value="formatted_address"
                  label="Endereço"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-map-marker"
                  hide-no-data
                  clearable
                  @update:search="fetchAddressSuggestions"
                ></v-combobox>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" size="large" @click="close">Cancelar</v-btn>
          <v-btn color="primary" variant="flat" size="large" @click="save" :disabled="!valid" :loading="saving">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog Confirmar Exclusão -->
    <v-dialog v-model="dialogDelete" max-width="450px" persistent>
      <v-card rounded="lg">
        <v-card-title class="bg-error text-white pa-4">Excluir Cliente</v-card-title>
        <v-card-text class="pa-6">
          Tem certeza que deseja excluir o cliente <strong>{{ editedItem.nome }}</strong>? Esta ação não pode ser desfeita.
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="closeDelete">Cancelar</v-btn>
          <v-btn color="error" variant="flat" @click="deleteItemConfirm" :loading="saving">Sim, Excluir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
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
import { ref, onMounted } from 'vue'
import { useClientes } from '@/composables/clientes/useClientes'
import { useAddressAutocomplete } from '@/composables/shared/useAddressAutocomplete'
import { useSnackbar } from '@/composables/shared/useSnackbar'
import { formatPhone, formatCPF } from '@/utils/shared/formatters'

// notificações e busca de endereço (composables compartilhados)
const { snackbar, snackbarText, snackbarColor, showMessage } = useSnackbar()
const {
  addressSearch,
  addressSuggestions,
  addressLoading,
  fetchAddressSuggestions,
  resetAddressSearch,
} = useAddressAutocomplete()

// estado reativo e regras de negócio de clientes
const {
  clientes,
  loading,
  saving,
  editedItem,
  formTitle,
  nameRules,
  phoneRules,
  cpfRules,
  emailRules,
  resetEditedItem,
  setEditedItem,
  fetchClientes,
  saveCliente,
  deleteCliente,
} = useClientes(showMessage)

// estados puramente visuais/UI locais dos modais e formulário
const dialog = ref(false)
const dialogDelete = ref(false)
const valid = ref(false)
const form = ref(null)

const headers = [
  { title: 'Nome', key: 'nome', align: 'start', sortable: true },
  { title: 'Telefone', key: 'telefone', sortable: false },
  { title: 'Endereço', key: 'endereco', sortable: false },
  { title: 'E-mail', key: 'email', sortable: false },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'end', width: '120px' },
]

// controle de abertura e fechamento dos modais
const openDialog = () => {
  resetEditedItem()
  resetAddressSearch()
  dialog.value = true
  if (form.value) form.value.resetValidation()
}

const editItem = (item) => {
  setEditedItem(item)
  resetAddressSearch()
  dialog.value = true
}

const deleteItem = (item) => {
  setEditedItem(item)
  dialogDelete.value = true
}

const close = () => {
  dialog.value = false
  resetEditedItem()
  resetAddressSearch()
  if (form.value) form.value.resetValidation()
}

const closeDelete = () => {
  dialogDelete.value = false
  resetEditedItem()
}

const deleteItemConfirm = async () => {
  await deleteCliente()
  closeDelete()
}

const save = async () => {
  if (!form.value) return
  const { valid: isValid } = await form.value.validate()
  if (!isValid) return

  const sucesso = await saveCliente()
  if (sucesso) {
    close()
  }
}

onMounted(() => {
  fetchClientes()
})
</script>

<style scoped>
/* Transições suaves para botões */
.v-btn {
  text-transform: none;
  letter-spacing: 0.5px;
}
</style>
