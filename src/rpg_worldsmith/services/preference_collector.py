from typing import Dict


class PreferenceCollector:
    QUESTIONS = [
        (
            "estilo_genero",
            "🎭 Estilo e Gênero do Universo: fantástico, distópico, futurista, histórico...?",
        ),
        (
            "tom_narrativo",
            "🎭 Deseja algo épico e grandioso, sombrio, político, leve e divertido...?",
        ),
        (
            "sociedade",
            "🌍 Tipo de Sociedade: império, anarquia, tribal, corporativista, fragmentado em reinos...?",
        ),
        (
            "tecnologia",
            "🧭 Nível Tecnológico: idade da pedra, medieval, renascença, industrial, futurista, pós-apocalíptico...?",
        ),
        (
            "elementos",
            "✨ Elementos marcantes: magia, IA, religião dominante, tecnologia avançada, criaturas fantásticas...?",
        ),
        (
            "temas",
            "⚔️ Temas: luta de classes, conspiração, resistência, conflitos religiosos, corrupção governamental, resistência a opressão, viagens e exploração, crise ambiental...?",
        ),
        (
            "personagens",
            "🧑‍🤝‍🧑 Tipo de Personagens: rebeldes, soldados, exploradores, membros de uma orgem, investigadores, exilados, nobres...?",
        ),
        ("objetivo_grupo", "👊 Objetivo do grupo: proteger, vingar, destruir...?"),
        ("tom", "🔮 Tom geral: realista, simbólico, heróico, sombrio, aventuroso...?"),
    ]

    def collect_preferences(self) -> Dict[str, str]:
        prefs: Dict[str, str] = {}
        confirm = "n"
        print("🧠 Iniciando a criação do mundo...\n")
        print("🔍 Responda às perguntas abaixo para definir as preferências do seu mundo:\n")
        while confirm != "s":
            for key, question in self.QUESTIONS:
                response = input(f"{question}\n> ").strip()
                if response:
                    prefs[key] = response
                    print("\n")
                else:
                    print("Resposta não pode ser vazia. Tente novamente.\n")
                    continue

            if len(prefs) == len(self.QUESTIONS):
                print("\n🔍 Resumo das preferências coletadas: \n")
                for key, value in prefs.items():
                    print(f"- {key.replace("_", " ").title()}: {value}")
                confirm = input("\nVocê confirma essas preferências? (s/n): ").strip().lower()
                if confirm != "s":
                    print("\nVamos tentar novamente...\n")
                    prefs.clear()
            else:
                print(
                    "\nParece que algumas perguntas não foram respondidas. Vamos tentar novamente...\n"
                )
                prefs.clear()
                confirm = "n"
        if confirm == "s":
            print("\n✅ Preferências coletadas com sucesso!\n")
        return prefs
