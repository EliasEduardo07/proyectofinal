elif page == "Algoritmo Apriori":
    st.header("Análisis de Asociación con el Algoritmo Apriori")

    # Cargar los datos
    try:
        data = pd.read_csv('store_data.csv', header=None)

        # Preparar los datos para el algoritmo Apriori
        transactions = []
        for i in range(0, len(data)):
            transactions.append([str(data.values[i, j]) for j in range(0, len(data.columns)) if str(data.values[i, j]) != 'nan'])

        # Campos para introducir el soporte mínimo, la confianza y la elevación
        min_support = st.slider('Soporte mínimo', min_value=0.01, max_value=0.5, value=0.01, step=0.01)
        min_confidence = st.slider('Confianza mínima', min_value=0.0, max_value=1.0, value=0.1, step=0.1)
        min_lift = st.slider('Elevación mínima', min_value=1.0, max_value=10.0, value=1.0, step=0.1)

        if st.button('Ejecutar algoritmo Apriori'):
            # Ejecutar el algoritmo Apriori
            rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)

            # Mostrar los resultados
            results = list(rules)
            for i in results:
                st.write('Regla: ' + str(i[0]) + ' -> Soporte: ' + str(i[1]))

            # Crear un gráfico de red para visualizar las reglas
            G = nx.DiGraph()

            for result in results:
                for item in result.ordered_statistics:
                    G.add_edge(str(item.items_base), str(item.items_add), weight=result.support, label="{0:.3f}".format(result.support))

            pos = nx.spring_layout(G)
            plt.figure(figsize=(10, 10))
            nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
                    node_size=500, node_color='pink', alpha=0.9,
                    labels={node: node for node in G.nodes()})
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))
            plt.axis('off')
            st.pyplot()

    except FileNotFoundError:
        st.error("El archivo 'store_data.csv' no se encontró en el directorio actual.")
