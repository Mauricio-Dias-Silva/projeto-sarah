import os
import google.generativeai as genai

class AssistenteSocialIA:
    """
    Agente Assistente Social para o Projeto Sarah (PI 3).
    Forma pareceres e sugere acolhimentos prioritários para mães/beneficiárias.
    """
    
    SYSTEM_PROMPT = """
    Você é a 'Sarah', a Inteligência Artificial e Assistente Social Chefe do 'Projeto Sarah' (uma ONG voltada para acolhimento de gestantes e mães em situação de vulnerabilidade).
    Sua missão é fazer a triagem a partir dos dados do formulário da beneficiária e retornar um Parecer Social Ágil.
    
    Aja de forma muito empática e técnica. O texto será lido por voluntários e coordenadores da ONG.
    Classifique a prioridade de atendimento (Baixa, Média, Alta, Crítica) dependendo da 'Situação da Gravidez', 'Histórico Médico' e das 'Necessidades'.
    Proponha no final 3 ações imediatas para a ONG executar (ex: Montar Kit Enxoval Urgente, Encaminhar para Nutricionista, etc).
    
    Retorne o texto OBRIGATORIAMENTE em formato HTML (usando tags <strong>, <ul>, <li>, <p> e classes utilitárias do Bootstrap se apropriado, como text-danger, text-warning). 
    Não use ```html. Direto nas tags. Foco na objetividade.
    """

    def __init__(self):
        try:
            api_key = os.environ.get("AURA_GEMINI_KEY", "AIzaSyCQD0JuVaf7wMB_jNAUY9zH4QLNKTQgLFg")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                'gemini-2.5-flash-lite',
                system_instruction=self.SYSTEM_PROMPT
            )
        except Exception as e:
            print(f"[SarahAI] Erro: {e}")
            self.model = None

    def gerar_triagem(self, nome, gravida, medico, necessidades) -> str:
        if not self.model:
            return "<p class='text-danger'>Sistema Neural de Triagem Inativo.</p>"

        prompt = (
            f"Faça a triagem social da seguinte beneficiária:\n\n"
            f"- Nome Cadastrado: {nome}\n"
            f"- Situação da Gestação/Gravidez: {gravida}\n"
            f"- Histórico Médico Reportado: {medico}\n"
            f"- Necessidades Solicitadas: {necessidades}\n\n"
            "Gere o parecer técnico imediato focando na ação da ONG."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.replace('```html', '').replace('```', '').strip()
        except Exception as e:
            return f"<p class='text-danger'>Erro no modelo: {e}</p>"
