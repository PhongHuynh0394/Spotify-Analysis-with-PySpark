import lyricsgenius as lg


class GeniusScrapper(lg.Genius):
    def __init__(self, token):
        super().__init__(token)
