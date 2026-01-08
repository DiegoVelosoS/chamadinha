# CHAMADINHA - Reconhecimento Facial ✅

Protótipo para controle de presença por foto, usando IA para identificar rostos, corrigir nomes digitados e um banco de dados que aprende com o tempo.

## 🔍 Funcionalidades

- Detecta rostos na foto usando **insightface**.
- Sugere nomes com base no histórico e corrige nomes semelhantes com **thefuzz**.
- Mantém um arquivo `banco_rostos.pkl` com a "memória" dos rostos (não apague este arquivo).
- Gera relatório em texto (.txt) com a lista de presentes.

---

## 🗂️ Estrutura do Projeto (exemplo)

```
banco_rostos.pkl        # banco de dados local (pickle)
app.py                  # aplicação Streamlit
Relatorios/             # (a implementar)
Readme.txt              # aviso/ponte para README.md
README.md               # este arquivo (Markdown)
requirements.txt        # dependências do projeto
```

---

## ⚙️ Como usar (rápido)

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

## 📌 Observações importantes

- Por padrão, o `app.py` salva `banco_rostos.pkl` **localmente**. Se preferir salvar no Google Drive, monte o Drive antes de iniciar o app ou ajuste o valor de `DB_FILE` no `app.py` para o caminho desejado.

> **Atenção:** não apague `banco_rostos.pkl` se quiser que a IA mantenha sua "memória" dos rostos.

- Algumas versões do Streamlit podem não suportar `st.toast`; o app foi ajustado para usar `st.success` para garantir compatibilidade.
- Se o projeto mencionar ferramentas não utilizadas no código (ex.: `DeepFace`), revise para evitar confusão.

---

## 💡 Dica

- Quanto mais você usar, melhor o sistema aprende (mais exemplos = melhores sugestões).

---

Se quiser, posso também gerar um `requirements.txt` minimal com as versões testadas ou criar um pequeno script de setup para facilitar a instalação.