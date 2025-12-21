def calculate_score(off_data=None, **kwargs):
    """
    # O uso de off_data=None torna o argumento opcional na posição, 
    # e **kwargs captura qualquer outro dado enviado (como nova_group ou ingredients_tags).
    """
    # Se off_data não for passado, tenta extrair de kwargs ou cria um dict vazio
    # Garante que temos um dicionário para trabalhar, mesmo que venha via kwargs
    data = off_data if off_data is not None else kwargs.get('off_data', {})
    score = 50  # Pontuação base neutra

    # 1. Labels/Certificações (Prioridade Alta: Essencial)
    # Importante para validar greenwashing e peso alto no score. [cite: 17-12-2025]
    labels = data.get('labels_tags', [])
    certificacoes_vips = ['en:organic', 'en:fair-trade',
                          'en:eu-organic', 'en:rainforest-alliance']
    for label in labels:
        if any(vip in label for vip in certificacoes_vips):
            score += 15  # Bônus alto para certificações oficiais

    # 2. Análise de Ingredientes (Prioridade Alta: Vegan/Palm Oil)
    # Indica análise automática; palm-oil tem peso negativo. [cite: 17-12-2025]
    analysis = data.get('ingredients_analysis_tags', [])
    if 'en:palm-oil-free' in analysis:
        score += 10
    if 'en:palm-oil' in analysis:
        score -= 20  # Peso negativo forte para óleo de palma
    if 'en:vegan' in analysis:
        score += 10

    # 3. Nível de Processamento (Prioridade Média: NOVA Group)
    # Produtos ultra-processados (4) têm maior pegada ambiental. [cite: 17-12-2025]
    nova = kwargs.get('nova_group') or data.get('nova_group')
    if nova:
        try:
            val = int(nova)
            if val == 1:
                score += 10
            if val == 4:
                score -= 15  # Peso negativo para ultra-processados
        except (ValueError, TypeError):
            pass

    # 4. Aditivos (Prioridade Média)
    # A quantidade indica o nível de processamento. [cite: 17-12-2025]
    additives = data.get('additives_tags', [])
    score -= (len(additives) * 2)

    # Garante que o score fique entre 0 e 100
    return max(0, min(100, score))
