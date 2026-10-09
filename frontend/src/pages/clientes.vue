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
import { ref, computed, onMounted } from 'vue'
import { fetchNominatimAddress } from '../services/nominatimService'

const apiBase = 'http://127.0.0.1:5000/api'

// Estado
const clientes = ref([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)
const valid = ref(false)
const form = ref(null)

// Estado Nominatim (Endereço)
const addressSearch = ref('')
const addressSuggestions = ref([])
const addressLoading = ref(false)
let addressTimeout = null

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const headers = [
  { title: 'Nome', key: 'nome', align: 'start', sortable: true },
  { title: 'Telefone', key: 'telefone', sortable: false },
  { title: 'Endereço', key: 'endereco', sortable: false },
  { title: 'E-mail', key: 'email', sortable: false },
  { title: 'Ações', key: 'acoes', sortable: false, align: 'end', width: '120px' },
]

const defaultItem = {
  id: null,
  nome: '',
  telefone: '',
  cpf: '',
  email: '',
  endereco: '',
}

const editedItem = ref(Object.assign({}, defaultItem))

const formTitle = computed(() => {
  return editedItem.value.id ? 'Editar Cliente' : 'Novo Cliente'
})

// Máscaras de formatação
const formatPhone = (val) => {
  if (!val) return ''
  let v = val.replace(/\D/g, '')
  if (v.length > 11) v = v.substring(0, 11)
  
  if (v.length <= 2) {
    return v.length > 0 ? `(${v}` : v
  } else if (v.length <= 7) {
    return `(${v.substring(0, 2)}) ${v.substring(2)}`
  } else {
    return `(${v.substring(0, 2)}) ${v.substring(2, 7)}-${v.substring(7)}`
  }
}

const formatCPF = (val) => {
  if (!val) return ''
  let v = val.replace(/\D/g, '')
  if (v.length > 11) v = v.substring(0, 11)
  
  if (v.length <= 3) {
    return v
  } else if (v.length <= 6) {
    return `${v.substring(0, 3)}.${v.substring(3)}`
  } else if (v.length <= 9) {
    return `${v.substring(0, 3)}.${v.substring(3, 6)}.${v.substring(6)}`
  } else {
    return `${v.substring(0, 3)}.${v.substring(3, 6)}.${v.substring(6, 9)}-${v.substring(9)}`
  }
}

// Regras de Validação
const nameRules = [
  v => !!v || 'Nome é obrigatório',
  v => /^[a-zA-ZÀ-ÿ\s]+$/.test(v) || 'Nome deve conter apenas letras e espaços'
]

const phoneRules = [
  v => !!v || 'Telefone é obrigatório',
  v => (v && v.replace(/\D/g, '').length === 11) || 'Telefone deve ter 11 dígitos'
]

const cpfRules = [
  v => !v || v.replace(/\D/g, '').length === 11 || 'CPF deve ter 11 dígitos'
]

const emailRules = [
  v => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'E-mail inválido'
]

// Busca Inteligente de Endereço (Nominatim OpenStreetMap via Service)
const fetchAddressSuggestions = (query) => {
  if (!query || query.length < 4) {
    addressSuggestions.value = []
    return
  }
  
  if (addressTimeout) clearTimeout(addressTimeout)
  
  addressTimeout = setTimeout(async () => {
    addressLoading.value = true
    try {
      addressSuggestions.value = await fetchNominatimAddress(query)
    } finally {
      addressLoading.value = false
    }
  }, 300) // Reduzido agressivamente para 300ms
}

// Métodos
const showMessage = (text, color = 'success') => {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

const fetchClientes = async () => {
  loading.value = true
  try {
    const res = await fetch(`${apiBase}/clientes`)
    if (res.ok) {
      const data = await res.json()
      clientes.value = data.map(c => ({
        ...c,
        telefone: formatPhone(c.telefone),
        cpf: formatCPF(c.cpf)
      }))
    } else {
      showMessage('Erro ao buscar clientes', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão ao servidor Flask', 'error')
  } finally {
    loading.value = false
  }
}

const openDialog = () => {
  editedItem.value = Object.assign({}, defaultItem)
  dialog.value = true
  if (form.value) form.value.resetValidation()
}

const editItem = (item) => {
  editedItem.value = Object.assign({}, item)
  // Certificar-se que a máscara está aplicada ao editar
  editedItem.value.telefone = formatPhone(editedItem.value.telefone)
  editedItem.value.cpf = formatCPF(editedItem.value.cpf)
  dialog.value = true
}

const deleteItem = (item) => {
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

const close = () => {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  if (form.value) form.value.resetValidation()
}

const closeDelete = () => {
  dialogDelete.value = false
  editedItem.value = Object.assign({}, defaultItem)
}

const deleteItemConfirm = async () => {
  saving.value = true
  try {
    const res = await fetch(`${apiBase}/clientes/${editedItem.value.id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      showMessage('Cliente excluído com sucesso')
      await fetchClientes()
    } else {
      showMessage('Erro ao excluir cliente', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão', 'error')
  } finally {
    saving.value = false
    closeDelete()
  }
}

const save = async () => {
  if (!form.value) return
  const { valid: isValid } = await form.value.validate()
  if (!isValid) return

  saving.value = true
  const method = editedItem.value.id ? 'PUT' : 'POST'
  const url = editedItem.value.id 
    ? `${apiBase}/clientes/${editedItem.value.id}` 
    : `${apiBase}/clientes`

  // Remover máscara para enviar apenas números ao backend e sanitizar o endereço (String)
  const addressVal = editedItem.value.endereco
  const payload = {
    ...editedItem.value,
    telefone: editedItem.value.telefone ? String(editedItem.value.telefone).replace(/\D/g, '') : '',
    cpf: editedItem.value.cpf ? String(editedItem.value.cpf).replace(/\D/g, '') : null,
    endereco: (typeof addressVal === 'object' && addressVal !== null) 
                ? (addressVal.formatted_address || addressVal.display_name || '')
                : (addressVal || '')
  }

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      showMessage(`Cliente ${editedItem.value.id ? 'atualizado' : 'cadastrado'} com sucesso`)
      close()
      await fetchClientes()
    } else {
      const err = await res.json()
      showMessage(err.erro || 'Erro ao salvar', 'error')
    }
  } catch (error) {
    showMessage('Erro de conexão', 'error')
  } finally {
    saving.value = false
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
