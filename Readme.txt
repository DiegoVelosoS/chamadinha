## CHAMADINHA - Reconhecimento Facial
Protótipo para controle de presença por foto, usando IA para identificar rostos, corrigir nomes digitados e um banco de dados que aprende com o tempo.

Funcionalidade:
- Detecta rostos na foto (insightface).
- Sugere nomes com base no histórico; corrige nomes similares usando `thefuzz`.
- Mantém um arquivo `banco_rostos.pkl` com a "memória" dos rostos (não apague este arquivo).
- Gera relatório em texto com a lista de presentes.

Estrutura (exemplo):
    banco_rostos.pkl        # banco de dados local (pickle)
    app.py                  # aplicação Streamlit
    Relatorios/             # (a implementar)

Como usar (resumo):
1. Instale dependências (ver `requirements.txt`).
2. Rode: `streamlit run app.py`.
3. Faça upload da foto da turma.
4. Para cada rosto, confirme ou corrija o nome (o sistema sugere nomes baseado no histórico).
5. Baixe o relatório final em .txt.

Observações:
- O `app.py` salva o `banco_rostos.pkl` localmente por padrão; se você quiser salvar no Google Drive, monte o Drive antes de iniciar o app ou ajuste `DB_FILE` para o caminho do Drive.
- O protótipo melhora sua performance com o uso contínuo (mais exemplos = melhores sugestões).
- Se o projeto mencionar ferramentas não utilizadas no código (ex.: DeepFace), revise para evitar confusão..