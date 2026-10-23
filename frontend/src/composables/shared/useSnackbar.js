/**
 * Composable compartilhado para gerenciamento de mensagens de feedback (v-snackbar).
 */
import { ref } from 'vue'

export function useSnackbar() {
  const snackbar = ref(false)
  const snackbarText = ref('')
  const snackbarColor = ref('success')

  // exibe uma notificação temporária na tela com a cor informada
  function showMessage(text, color = 'success') {
    snackbarText.value = text
    snackbarColor.value = color
    snackbar.value = true
  }

  return {
    snackbar,
    snackbarText,
    snackbarColor,
    showMessage,
    mostrarMensagem: showMessage,
  }
}

