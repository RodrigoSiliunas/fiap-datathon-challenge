from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 🔹 Carregar o modelo salvo (.pkl)
with open("./modelo_recomendacao.pkl", 'rb') as f:
    modelo_carregado = pickle.load(f)

df_train_final = modelo_carregado["df_train_final"]
df_items = modelo_carregado["df_items"]
similar_noticias = modelo_carregado["similar_noticias"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API de Recomendação de Notícias está rodando!"})

@app.route("/predict", methods=["GET"])
def predict():
    """
    Retorna recomendações de notícias.
    Exemplo de chamada:
    - `/predict?user_id=user123&top_n=5`
    - `/predict?top_n=5` (Sem user_id → retorna recomendações populares)
    """
    user_id = request.args.get("user_id", default=None, type=str)
    top_n = request.args.get("top_n", default=5, type=int)

    recomendacoes = recomendar_noticias(user_id, top_n)
    return jsonify(recomendacoes)

def recomendar_noticias(user_id, top_n=5):
    """
    Retorna as recomendações de notícias para um usuário.
    - Se o usuário tiver histórico, recomenda notícias similares.
    - Se for cold-start, recomenda as mais populares.
    """

    # 🔹 Verificar se o usuário tem histórico
    user_history_df = df_train_final[df_train_final['userId'] == user_id]

    if user_history_df.empty:
        # 🚀 COLD START - Recomendar notícias populares
        df_items['engagement_score'] = (
            df_items['popularity_score'] * 0.8 +
            df_items['recency_days'].apply(lambda x: -0.2 * x if pd.notna(x) else 0)
        )
        recomendacoes = df_items.sort_values('engagement_score', ascending=False).head(top_n)
    else:
        # ✅ Usuário com histórico - Buscar notícias similares
        noticias_lidas = user_history_df['page'].unique().tolist()
        noticias_similares = []

        for noticia in noticias_lidas:
            if noticia in similar_noticias:
                noticias_similares.extend(similar_noticias[noticia])

        # 🔹 Filtrar notícias que o usuário ainda não leu
        df_candidate_news = df_items[df_items['page'].isin(noticias_similares) & ~df_items['page'].isin(noticias_lidas)]

        if df_candidate_news.empty:
            # 🚀 Se nenhuma notícia similar estiver disponível, retorna populares
            recomendacoes = df_items.sort_values('popularity_score', ascending=False).head(top_n)
        else:
            # ✅ Criar score de recomendação
            df_candidate_news['candidate_score'] = (
                df_candidate_news['popularity_score'] * 0.5 +
                df_candidate_news['recency_days'].apply(lambda x: -0.2 * x if pd.notna(x) else 0)
            )
            recomendacoes = df_candidate_news.sort_values('candidate_score', ascending=False).head(top_n)

    return recomendacoes[['page', 'title', 'caption', 'url', 'recency_days']].to_dict(orient="records")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
