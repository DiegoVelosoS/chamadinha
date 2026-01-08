import streamlit as st
import cv2
import numpy as np
import pickle
import os
import insightface
from insightface.app import FaceAnalysis
from thefuzz import process
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Chamadinha AI", layout="centered")
st.title("Chamadinha - Reconhecimento Facial")

st.markdown("""
**Protótipo para chamadas usando apenas uma foto.**
O sistema é um protótipo para teste da IA que identifica os alunos e corrige os nomes automaticamente.
Ele também **"aprende os rostos"**: quanto mais você usa, menos precisa digitar nas próximas aulas.
É só enviar a foto e baixar a lista.
""")

# --- CAMINHOS E ARQUIVOS ---
DB_FILE = 'banco_rostos.pkl'

# --- FUNÇÕES DE CARREGAMENTO (CACHED) ---
@st.cache_resource
def carregar_modelo():
    # Inicializa o InsightFace (RetinaFace + ArcFace)
    # providers=['CPUExecutionProvider'] garante compatibilidade sem GPU
    model = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    model.prepare(ctx_id=0, det_size=(640, 640))
    return model

@st.cache_data
def carregar_banco_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'rb') as f:
            return pickle.load(f)
    return []

def salvar_banco_dados(dados):
    with open(DB_FILE, 'wb') as f:
        pickle.dump(dados, f)

# --- LÓGICA DE RECONHECIMENTO ---
def buscar_melhor_match(novo_embedding, banco_dados, threshold=1.1):
    melhor_nome = None
    menor_distancia = float('inf')
    
    for pessoa in banco_dados:
        distancia = np.linalg.norm(novo_embedding - pessoa['embedding'])
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_nome = pessoa['nome']
            
    if menor_distancia < threshold:
        return melhor_nome, menor_distancia
    return None, 0.0

def verificar_nome_parecido(nome_digitado, banco_dados):
    nomes_conhecidos = list(set([p['nome'] for p in banco_dados]))
    if not nomes_conhecidos:
        return None
    match, score = process.extractOne(nome_digitado, nomes_conhecidos)
    if score > 85 and match != nome_digitado:
        return match
    return None

# --- INICIALIZAÇÃO DE ESTADO ---
if 'banco_dados' not in st.session_state:
    st.session_state['banco_dados'] = carregar_banco_dados()

# CRIA UM CONTADOR PARA O UPLOAD
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0

if 'processamento_iniciado' not in st.session_state:
    st.session_state['processamento_iniciado'] = False
    st.session_state['rostos_detectados'] = []
    st.session_state['imagem_original'] = None
    st.session_state['indice_atual'] = 0
    st.session_state['chamada_final'] = []

# --- INTERFACE PRINCIPAL ---

# 1. Sidebar para Infos
with st.sidebar:
    st.header("Status do Banco")
    qtd_alunos = len(st.session_state['banco_dados'])
    st.write(f"Alunos na memória: **{qtd_alunos}**")
    if st.button("Limpar Memória (Reset)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.session_state['banco_dados'] = []
        st.rerun()

# 2. Configurações da Chamada (NOVO)
st.subheader("Dados da Aula")
col_data, col_turma = st.columns(2)
with col_data:
    data_atual = st.date_input("Data", value=date.today())
with col_turma:
    turma_nome = st.text_input("Turma / Horário", placeholder="Ex: Turma das 20h")

st.divider()

# 3. Upload da Imagem
# ADICIONA A KEY DINÂMICA
uploaded_file = st.file_uploader("Faça upload da foto da turma", type=['jpg', 'png', 'jpeg'], key=f"uploader_{st.session_state['uploader_key']}")

if uploaded_file is not None:
    # Processar a imagem apenas se mudou ou se é a primeira vez
    if not st.session_state['processamento_iniciado']:
        with st.spinner('Detectando rostos...'):
            # Converter arquivo para formato OpenCV
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Para exibir no Streamlit
            
            # Detectar
            app = carregar_modelo()
            rostos = app.get(img)
            
            # Ordenar rostos da esquerda para a direita (facilita a chamada)
            rostos.sort(key=lambda x: x.bbox[0])
            
            # Salvar no estado
            st.session_state['imagem_original'] = img_rgb
            st.session_state['rostos_detectados'] = rostos
            st.session_state['processamento_iniciado'] = True
            st.rerun()

# 4. Fluxo de Chamada (Um por um)
if st.session_state['processamento_iniciado']:
    idx = st.session_state['indice_atual']
    total_rostos = len(st.session_state['rostos_detectados'])
    imagem = st.session_state['imagem_original']
    
    # Se ainda tem rostos para processar
    if idx < total_rostos:
        rosto_atual = st.session_state['rostos_detectados'][idx]
        
        # Barra de progresso
        st.progress((idx) / total_rostos, text=f"Identificando aluno {idx+1} de {total_rostos}")
        
        col1, col2 = st.columns([1, 2])
        
        # Coluna 1: O Rosto Recortado
        with col1:
            bbox = rosto_atual.bbox.astype(int)
            x1, y1, x2, y2 = max(0, bbox[0]), max(0, bbox[1]), min(imagem.shape[1], bbox[2]), min(imagem.shape[0], bbox[3])
            face_crop = imagem[y1:y2, x1:x2]
            st.image(face_crop, caption="Quem é?", width=150)
            
        # Coluna 2: A Pergunta
        with col2:
            # Tenta identificar
            sugestao, dist = buscar_melhor_match(rosto_atual.embedding, st.session_state['banco_dados'])
            
            # Formulário para lidar com a interação
            with st.form(key=f"form_face_{idx}"):
                nome_final = ""
                
                # CASO A: Sugestão existe
                if sugestao:
                    st.info(f"Parece ser: **{sugestao}**")
                    confirmacao = st.radio("Está correto?", ["Sim", "Não"], horizontal=True)
                    novo_nome_input = st.text_input("Se não, quem é?", placeholder="Digite o nome correto...")
                
                # CASO B: Não conhece
                else:
                    st.warning("Não reconhecido.")
                    confirmacao = "Não" # Força entrada manual
                    novo_nome_input = st.text_input("Nome do Aluno:", placeholder="Ex: Gabriel")

                submit_btn = st.form_submit_button("Confirmar")
                
                if submit_btn:
                    # Lógica de decisão do nome
                    if sugestao and confirmacao == "Sim":
                        nome_final = sugestao
                    else:
                        if not novo_nome_input:
                            nome_final = "Desconhecido"
                        else:
                            # Verifica Typos
                            typo_match = verificar_nome_parecido(novo_nome_input, st.session_state['banco_dados'])
                            if typo_match:
                                st.toast(f"Corrigido de '{novo_nome_input}' para '{typo_match}'")
                                nome_final = typo_match
                            else:
                                nome_final = novo_nome_input
                    
                    # Salvar presença
                    st.session_state['chamada_final'].append(nome_final)
                    
                    # Aprender (Salvar no banco se não for desconhecido)
                    if nome_final != "Desconhecido":
                        novo_registro = {'nome': nome_final, 'embedding': rosto_atual.embedding}
                        st.session_state['banco_dados'].append(novo_registro)
                        salvar_banco_dados(st.session_state['banco_dados'])
                    
                    # Passar para o próximo
                    st.session_state['indice_atual'] += 1
                    st.rerun()

    # 5. Fim do Processo - Relatório
    else:
        st.success("Chamada Finalizada com Sucesso!")
        # EFEITO DE BALÕES REMOVIDO AQUI
        
        lista_presentes = st.session_state['chamada_final']
        
        # Exibir Imagem Completa Marcada
        img_final = imagem.copy()
        for i, rosto in enumerate(st.session_state['rostos_detectados']):
            bbox = rosto.bbox.astype(int)
            nome = lista_presentes[i]
            cv2.rectangle(img_final, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(img_final, nome, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
        st.image(img_final, caption="Turma Identificada", use_column_width=True)
        
        # EXIBIÇÃO FORMATADA DA LISTA
        st.markdown("---")
        st.subheader(f"Resumo: {turma_nome} ({data_atual})")
        st.markdown(f"**Total de Presentes:** {len(lista_presentes)}")
        
        st.write("### Nomes:")
        # Exibe em formato de lista limpa
        for nome_aluno in lista_presentes:
            st.markdown(f"- {nome_aluno}")
            
        st.markdown("---")
        
        # Preparar texto para download
        texto_cabecalho = f"DATA: {data_atual}\nTURMA: {turma_nome}\nTOTAL: {len(lista_presentes)}\n\n"
        texto_nomes = "LISTA DE PRESENÇA:\n" + "\n".join(lista_presentes)
        texto_completo = texto_cabecalho + texto_nomes
        
        st.download_button("Baixar Relatório .txt", texto_completo, file_name=f"chamada_{data_atual}.txt")
        
        # Botão para Reiniciar
 if st.button("Começar Nova Chamada"):
            # AUMENTA O CONTADOR PARA FORÇAR LIMPEZA DO UPLOAD
            st.session_state['uploader_key'] += 1
            
            keys_to_reset = ['processamento_iniciado', 'rostos_detectados', 'imagem_original', 'indice_atual', 'chamada_final']
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
