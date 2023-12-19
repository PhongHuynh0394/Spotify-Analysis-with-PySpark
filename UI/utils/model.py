from sklearn.neighbors import NearestNeighbors

class SongRecommendationSystem:
    def __init__(self, client, options):
        self.client = client
        self.options = options
        self.knn_model = NearestNeighbors(metric='cosine')

    def fit(self, table_name):   
        matrix_table = self._get_table(table_name).values
        self.knn_model.fit(matrix_table)
        
    def _get_table(self, table_name):
        sql = f"select * from {table_name}"
        return self.client.query(sql, self.options)
        
    def recommend_songs(self, track_name: str, table_name='home.searchs', num_recommendations=5):
        song_library = self._get_table(table_name).reset_index(drop=True)
        
        if track_name not in song_library['track_name'].values:
            print(f'Track "{track_name}" not found in the dataset.')
            return None
            
        features_matrix = self._get_table('home.model')
        track_index = song_library.index[song_library['track_name'] == track_name].tolist()[0]
        _, indices = self.knn_model.kneighbors([features_matrix.iloc[track_index]], n_neighbors=num_recommendations + 1)
        return song_library.loc[indices[0][1:], :]


