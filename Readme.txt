Chamadinha
Sistema de reconhecimento facial para automatizar a lista de presença em aulas através de fotos da turma.

/content/drive/MyDrive/.../Chamadinha/
│
├── banco_rostos.pkl        # O "Cérebro" do sistema (NÃO APAGAR)
├── Chamadinha.ipynb        # O código fonte (Notebook)
└── Relatorios/             # (Gerados após cada execução)
    └── Chamada_DD-MM-AAAA_Turma.txt


🚀 O que ele faz
Identifica rostos na foto (usando IA RetinaFace).

Aprende com o tempo: Sugere nomes automaticamente baseados em aulas anteriores.

Salva tudo no seu Google Drive (não perde os dados).

Gera Relatório em texto com a lista de presentes.


⚙️ Como Usar (Passo a Passo)
Instalação (Célula 1): Execute uma vez para baixar as bibliotecas.

Conexão (Célula 2): Conecte ao Google Drive para carregar o banco de dados.

Upload (Célula 3 e 4): Envie a foto da turma.

Chamada (Célula 5):

O sistema vai destacar um rosto.

Se reconhecer, pergutará: "É o Fulano?" (Responda s ou n).

Se não, digite o nome.

Relatório (Célula 6): Digite o nome da turma para gerar a lista final.


⚠️ Importante
O arquivo banco_rostos.pkl criado no seu Drive contém a "memória" da IA. Não apague esse arquivo, ou o sistema terá que aprender todos os rostos do zero novamente.