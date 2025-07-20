from pathlib import Path
import json
import re
from typing import Dict

from openai import OpenAI
from unidecode import unidecode

from rpg_worldsmith.config import settings


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]", "", unidecode(name).lower().replace(" ", "-"))


class WorldGenerator:
    def __init__(self, preferences: Dict[str, str]):
        self.preferences = preferences
        self.output_dir: Path = settings.DATA_PATH
        self.client = OpenAI(api_key=settings.OPEN_API_KEY)
        self.response_text = ""
        self.markdown = ""
        self.metadata: Dict[str, str] = {}

    def format_prompt(self) -> str:
        return f"""
        Você é um arquiteto de mundos narrativos e temáticos para jogos de RPG de mesa.
        Seu objetivo é criar universos ricos e únicos — fantásticos, distópicos, futuristas,
        históricos ou realistas — com base nos gostos e ideologias dos jogadores.
        Você é um mestre na construção de mundos com regras próprias, ecossistemas vivos e
        conflitos envolventes. Sua especialidade é adaptar o tipo de universo (como distópias
        políticas, reinos de magia, sociedades pós-apocalípticas ou ambientações históricas)
        aos desejos dos jogadores. Você considera fatores como geopolítica, tecnologia,
        classes sociais, cultura e história para criar um ambiente que instigue a imaginação
        e ofereça desafios narrativos profundos. Sua missão é garantir que cada mundo gerado
        seja único, jogável e relevante para os personagens que irão habitá-lo.

        Crie um mundo fictício baseado nas seguintes preferências fornecidas por jogadores de RPG:

        Estilo e Gênero: {self.preferences.get("estilo_genero")}
        Tom Narrativo: {self.preferences.get("tom_narrativo")}
        Estrutura da Sociedade: {self.preferences.get("sociedade")}
        Nível Tecnológico: {self.preferences.get("tecnologia")}
        Elementos Marcantes: {self.preferences.get("elementos")}
        Temas Centrais: {self.preferences.get("temas")}
        Personagens: {self.preferences.get("personagens")}
        Objetivo do Grupo: {self.preferences.get("objetivo_grupo")}
        Tom Geral: {self.preferences.get("tom")}

        Formate a resposta com:
        - Um resumo narrativo rico em detalhes em Markdown (cerca de 400 palavras).
        - Uma estrutura JSON separada com campos: nome_mundo, estilo, tom_narrativo, estrutura_social,
          nivel_tecnologico, elementos_chave, faccoes, temas, tipo_personagens, objetivo_personagens, atmosfera.
        """

    def call_openai(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                temperature=0.9,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um mestre de RPG que cria mundos ricos e coerentes.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            if (
                not response.choices
                or not response.choices[0].message
                or not response.choices[0].message.content
            ):
                raise ValueError("Resposta da API OpenAI está vazia ou malformada.")

            self.response_text = response.choices[0].message.content.strip()
            return self.response_text
        except Exception as e:
            raise RuntimeError(f"Erro ao chamar a API OpenAI: {e}")

    def parse_response(self) -> tuple[str, Dict[str, str]]:
        match = re.search(r"```json(.*?)```", self.response_text, re.DOTALL)
        self.markdown = self.response_text.split("```json")[0].strip()

        if match:
            try:
                self.metadata = json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                raise ValueError("Falha ao decodificar JSON do mundo gerado pela IA.")
        else:
            raise ValueError("Bloco JSON não encontrado na resposta da IA.")

        return self.markdown, self.metadata

    def save_markdown(self) -> Path:
        """
        Save the generated markdown summary to a file in the output directory.

        The file is named 'resumo.md' and is stored in a subdirectory named after the world,
        which is derived from the world name in the metadata.
        If the world name is not provided, it defaults to 'mundo_sem_nome'.
        The directory structure is created if it does not exist.

        Returns:
            Path: The path to the saved markdown file.
        """
        try:
            world_name = slugify(self.metadata.get("nome_mundo", "mundo_sem_nome"))
            world_path = self.output_dir / world_name
            world_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Erro ao criar diretório do mundo: {e}")

        if not self.markdown:
            raise ValueError("O resumo em Markdown está vazio. Verifique a resposta da IA.")

        try:
            markdown_path = world_path / "resumo.md"
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(self.markdown)
            return markdown_path
        except Exception as e:
            raise RuntimeError(f"Erro ao salvar o arquivo Markdown: {e}")

    def save_json(self) -> Path:
        world_name = slugify(self.metadata.get("nome_mundo", "mundo_sem_nome"))
        world_path = self.output_dir / world_name

        json_path = world_path / "metadados.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        return json_path

    def generate(self) -> Dict[str, str]:
        prompt = self.format_prompt()
        self.call_openai(prompt)
        self.parse_response()
        self.save_markdown()
        self.save_json()
        return self.metadata
