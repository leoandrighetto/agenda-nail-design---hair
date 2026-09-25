// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const rosadosTheme = {
  dark: false,
  colors: {
    background: '#FCF9F8',
    surface: '#FFFFFF',
    primary: '#C8A19C',
    secondary: '#A6907E',
    accent: '#CAB19D',
    info: '#C9BEB4',
    error: '#B00020',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'rosadosTheme',
    themes: {
      rosadosTheme,
    },
  },
})
