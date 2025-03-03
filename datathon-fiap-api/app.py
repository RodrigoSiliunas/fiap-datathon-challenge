from fastapi import FastAPI, Query
import pickle
import pandas as pd
from typing import List, Optional

# Criar a aplicação FastAPI
app = FastAPI()

# 🔹 Carregar o modelo salvo (.pkl)
with open("./modelo_recomendacao.pkl", 'rb') as f:
    modelo_carregado = pickle.load(f)

# 🔹 Recuperar os objetos do modelo salvo
df_train_final = modelo_carregado["df_train_final"]
df_items = modelo_carregado["df_items"]
similar_noticias = modelo_carregado["similar_noticias"]

@app.get("/")
def home():
    return {"message": "API de Recomendação de Notícias está rodando!"}

@app.get("/predict/")
def predict(user_id: Optional[str] = Query(None), top_n: int = 5) -> List[dict]:
    """
    Retorna as top-N recomendações.
    - Se `user_id` for informado, recomenda baseado no histórico.
    - Se `user_id` não for informado, retorna notícias mais populares.

    Exemplo de chamada:
    - `/predict/?user_id=user123&top_n=5`
    - `/predict/?top_n=5` (Sem user_id, retorna recomendações gerais)
    """
    return recomendar_noticias(user_id, df_train_final, df_items, similar_noticias, top_n).to_dict(orient="records")

def recomendar_noticias(
        user_id: Optional[str], df_train_final: pd.DataFrame, df_items: pd.DataFrame, similar_noticias: dict, top_n: int = 5) -> pd.DataFrame:
    """
    Retorna recomendações personalizadas para um usuário com base no histórico ou recomenda as mais populares se for cold-start.
    """

    # 🔹 Garantir que 'popularity_score' e 'recency_days' existem
    if 'popularity_score' not in df_items.columns:
        df_items['popularity_score'] = 0

    if 'recency_days' not in df_items.columns:
        df_items['recency_days'] = 0

    # 🔹 Se nenhum user_id for informado, recomendar notícias populares
    if user_id is None:
        df_items['engagement_score'] = (
            df_items['popularity_score'] * 0.8 +
            df_items['recency_days'].apply(lambda x: -0.2 * x if pd.notna(x) else 0)
        )
        return df_items.sort_values('engagement_score', ascending=False).head(top_n)[["page", "url", "title", "caption", "recency_days"]]

    # 🔹 Verificar se o usuário tem histórico
    user_history_df = df_train_final[df_train_final['userId'] == user_id]

    if user_history_df.empty:
        print(f"⚠️ Usuário {user_id} sem histórico, usando recomendação por popularidade.")

        df_items['engagement_score'] = (
            df_items['popularity_score'] * 0.8 +
            df_items['recency_days'].apply(lambda x: -0.2 * x if pd.notna(x) else 0)
        )
        return df_items.sort_values('engagement_score', ascending=False).head(top_n)[["page", "url", "title", "caption", "recency_days"]]

    else:
        print(f"✅ Usuário {user_id} encontrado! Buscando recomendações baseadas no histórico.")

        noticias_lidas = user_history_df['page'].unique().tolist()
        noticias_similares = []

        for noticia in noticias_lidas:
            if noticia in similar_noticias:
                noticias_similares.extend(similar_noticias[noticia])

        if not noticias_similares:
            print("⚠️ Nenhuma notícia similar encontrada! Retornando notícias populares.")
            return df_items.sort_values('popularity_score', ascending=False).head(top_n)[["page", "url", "title", "caption", "recency_days"]]

        df_candidate_news = df_items[df_items['page'].isin(noticias_similares) & ~df_items['page'].isin(noticias_lidas)]

        if df_candidate_news.empty:
            print("⚠️ Nenhuma notícia disponível para recomendação. Retornando populares.")
            return df_items.sort_values('popularity_score', ascending=False).head(top_n)[["page", "url", "title", "caption", "recency_days"]]

        df_candidate_news['candidate_score'] = (
            df_candidate_news['popularity_score'] * 0.5 +
            df_candidate_news['recency_days'].apply(lambda x: -0.2 * x if pd.notna(x) else 0)
        )

        return df_candidate_news \
            .sort_values('candidate_score', ascending=False).head(top_n)[["page", "url", "title", "caption", "recency_days"]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
