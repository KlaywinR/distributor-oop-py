
class ReviewMixin:
    def rate_service(self, stars):
        descriptions = {
            5: "Atendimento Excelente",
            4: "Atendimento Bom",
            3: "Bem Razoável",
            2: "Atendimento Ruim",
            1: "Péssimo"
        }
        
        if stars not in descriptions:
            return "Avaliação Inválida, ultilize a escala de 1 a 5 para a avaliação do atendimento."
        
        self._reviews.append(stars)
        return f"Obrigado, a sua avaliação foi: {stars} estrelas ({descriptions[stars]})"