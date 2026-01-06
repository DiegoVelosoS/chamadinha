CHAMADINHA - Reconhecimento Facial para Controle de Presença
Este projeto é uma ferramenta de Visão Computacional desenvolvida para automatizar a chamada e controle de presença em aulas através de fotos coletivas da turma.

O sistema utiliza Inteligência Artificial "State-of-the-Art" (SOTA) para detectar rostos, aprender identidades e gerar relatórios automáticos, mantendo um banco de dados que é salvo noGoogle Drive.

FUNCIONALIDADES
Detecção de Alta Precisão: Utiliza o modelo RetinaFace (via biblioteca InsightFace) para detectar rostos mesmo em condições difíceis (rostos pequenos, de perfil ou parcialmente cobertos).

Aprendizado Contínuo (Human-in-the-Loop):

O sistema sugere quem é o aluno com base na memória.

O usuário valida ("Sim/Não") ou insere o nome correto.

Novos rostos e validações são salvos para melhorar a precisão nas próximas aulas.

Correção Inteligente de Nomes: Se você digitar "Rafa" e o banco já tiver "Rafael", o sistema percebe a semelhança e sugere a correção (evitando duplicatas).

Banco de Dados Persistente: Todos os rostos aprendidos são salvos em um arquivo .pkl no Google Drive, garantindo que o sistema fique mais inteligente a cada uso.

Relatórios Automáticos: Ao final, gera um arquivo .txt com a data, turma e lista de presentes.

TECNOLOGIAS UTILIZADAS
Linguagem: Python
InsightFace: RetinaFace: como Framework principal para detecção; e
             ArcFace: para Reconhecimento facial.
OpenCV: Manipulação e processamento de imagens.
TheFuzz: Processamento de linguagem natural para correção de erros de digitação e fuzzy matching de nomes. Aqui é para corrigir nomes repetidos ou errados.
Pickle: Serialização de objetos para salvar o banco de dados de vetores faciais e nomes. Assim, o usuário pode acelerar o processo de registro de chamadas.

ESTRUTURA DE ARQUIVOS
O código cria e gerencia automaticamente a seguinte estrutura no seu Google Drive:

Plaintext
/content/drive/MyDrive/.../Chamadinha/
│
├── banco_rostos.pkl        # O "Cérebro" do sistema (NÃO APAGAR)
├── Chamadinha.ipynb        # O código fonte (Notebook)
└── Relatorios/             # (Gerados após cada execução)
    └── Chamada_DD-MM-AAAA_Turma.txt
Nota: O arquivo banco_rostos.pkl contém as "assinaturas matemáticas" (embeddings) dos rostos. Se ele for deletado, o sistema esquecerá todos os alunos e terá que aprender do zero.

COMO USAR
1. Abra o link do Streamlit.
2. Siga o passo-a-passo.

LÓGICA DO ALGORÍTMO
Detecção: A imagem é varrida para encontrar as coordenadas (x, y) de cada rosto.
Embedding: Cada rosto é transformado em um vetor numérico de 512 dimensões (uma identidade única).
Comparação (Distância Euclidiana): O vetor do rosto atual é comparado matematicamente com todos os vetores salvos no banco.
Se a "distância" for menor que 1.1, o sistema considera um "Match".
Fuzzy Matching (Texto): Ao inserir um nome manual, o algoritmo Levenshtein calcula a porcentagem de semelhança com nomes existentes (ex: Gabirel é 95% similar a Gabriel) para sugerir correções.

Dev Diego Veloso - 06/01/2026 como exercício pessoal