# CHAMADINHA - Reconhecimento Facial

Protótipo para controle de presença por foto, usando IA para identificar rostos, corrigir nomes digitados e um banco de dados que aprende com o tempo.

## Funcionalidades

- Detecta rostos na foto usando `insightface`.
- Sugere nomes com base no histórico e corrige nomes semelhantes com `thefuzz`.
- Mantém um arquivo `banco_rostos.pkl` com a "memória" dos rostos.
- Por enquanto, está gerando um relatório em texto (.txt) com a lista de presentes. Na próxima implementação, criar um relatório em CSV ou, se preferir, em Google Sheets (vai depender dos usuários).

---

## Estrutura do Projeto

```
banco_rostos.pkl        # banco de dados local (pickle)
app.py                  # código da aplicação via Streamlit
Relatorios/             # a ser criado (não implementado ainda)
README.md               # este arquivo Markdown explicativo do projeto
requirements.txt        # dependências do projeto necessárias para rodar no streamlit
```

---

## Como usar:

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Rode a aplicação:

```bash
streamlit run app.py
```

3. No navegador: faça upload da foto da turma e siga as instruções para confirmar/corrigir nomes.
4. Ao final, baixe o relatório `.txt` com a lista de presença.

---

## Observações importantes

- Por padrão, o `app.py` salva `banco_rostos.pkl` **localmente**. Se preferir, você pode salvar no Google Drive (sincronizando a pasta do projeto), usar o GitHub para versionamento (fazendo commits) e hospedar no Streamlit Cloud para que os usuários possam acessar o app.

> **Atenção:** O `banco_rostos.pkl` mantém a "memória" dos rostos da IA, por isso não apague esse arquivo.

- Algumas versões do Streamlit podem não suportar `st.toast`; o app foi ajustado para usar `st.success` para garantir compatibilidade.

---

- Quanto mais você usar, melhor o sistema aprende (mais exemplos = melhores sugestões).