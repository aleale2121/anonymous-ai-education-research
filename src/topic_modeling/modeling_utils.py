from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic

def build_topic_model(
    embedding_model,
    vectorizer_model,
    representation_model,
    n_neighbors=15,
    n_components=5,
    min_dist=0.00,
    min_cluster_size=25,
    min_samples=10,
    random_state=42
):
    umap_model = UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components,
        min_dist=min_dist,
        metric="cosine",
        random_state=random_state
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method="eom"
    )

    topic_model = BERTopic(
        embedding_model=embedding_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        calculate_probabilities=False,
        verbose=True
    )

    return topic_model