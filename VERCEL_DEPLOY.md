# Deploy no Vercel - Instruções

## Passos para configurar:

### 1. Variável de Ambiente
No painel do Vercel, você precisa adicionar a variável de ambiente:

1. Vá em **Settings** → **Environment Variables**
2. Adicione:
   - **Nome**: `TMDB_API_KEY`
   - **Valor**: sua chave da API do TMDB
   - **Environments**: Production, Preview, Development (selecione todos)

### 2. Build Settings (configuração automática via vercel.json)
O arquivo `vercel.json` já está configurado, mas verifique se está assim:
- **Framework Preset**: Other
- **Build Command**: (deixe vazio)
- **Output Directory**: (deixe vazio)
- **Install Command**: `pip install -r requirements.txt`

### 3. Redeploy
Após adicionar a variável de ambiente:
1. Vá em **Deployments**
2. Clique nos três pontos do último deployment
3. Selecione **Redeploy**

### Troubleshooting

Se continuar dando erro "Oops something wrong":

1. **Verifique os logs**:
   - No Vercel, vá em **Deployments** → clique no deployment → **Functions**
   - Veja os logs de erro da função

2. **Teste a API Key**:
   - Certifique-se que a API key do TMDB está correta
   - Teste em: https://api.themoviedb.org/3/genre/movie/list?api_key=SUA_KEY

3. **Verifique CORS**:
   - Se necessário, pode precisar adicionar headers CORS

### Obtendo a API Key do TMDB
1. Acesse: https://www.themoviedb.org/settings/api
2. Faça login ou crie uma conta
3. Request uma API key (é grátis)
4. Cole a key nas variáveis de ambiente do Vercel
