from scraper.extractors.football_player_wikipedia_extractor import FootballPlayerWikipediaExtractor


FOOTBALL_PLAYERS__EXTRACTOR_TYPE = 'football_players'

EXTRACTOR_REGISTRY = {
    FOOTBALL_PLAYERS__EXTRACTOR_TYPE: FootballPlayerWikipediaExtractor
}
