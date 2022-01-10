from os.path import join, dirname

from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.log import LOG
from ovos_utils.parse import fuzzy_match
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media
from youtube_archivist import YoutubeMonitor


class WorldMovieCentralSkill(OVOSCommonPlaybackSkill):

    def __init__(self):
        super().__init__("WorldMovieCentral")
        self.supported_media = [MediaType.MOVIE, MediaType.GENERIC]
        self.skill_icon = join(dirname(__file__), "ui", "worldmoviecentral_icon.jpg")
        self.archive = YoutubeMonitor(db_name="WorldMovieCentral",
                                      blacklisted_kwords=["trailer", "teaser", "movie scene",
                                                          "movie clip", "behind the scenes", "movie analysis",
                                                          "Movie Preview", "soundtrack", " OST", "opening theme"],
                                      min_duration=30 * 60,
                                      logger=LOG)

    def initialize(self):
        url = "https://www.youtube.com/channel/UCNbnH_iXdGphKO-AGe-GbLA"
        bootstrap = "https://raw.githubusercontent.com/OpenJarbas/streamindex/main/WorldMovieCentral.json"
        self.archive.bootstrap_from_url(bootstrap)
        self.archive.monitor(url)
        self.archive.setDaemon(True)
        self.archive.start()

    # matching
    def match_skill(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "movie") or media_type == MediaType.MOVIE:
            score += 10
        if self.voc_match(phrase, "worldmovie"):
            score += 50
        if self.voc_match(phrase, "central"):
            score += 10
        return score

    def normalize_title(self, title):
        title = title.lower().strip()
        title = self.remove_voc(title, "worldmovie")
        title = self.remove_voc(title, "central")
        title = self.remove_voc(title, "movie")
        title = title.replace("|", "").replace('"', "") \
            .replace(':', "").replace('”', "").replace('“', "") \
            .strip()
        return " ".join(
            [w for w in title.split(" ") if w])  # remove extra spaces

    def calc_score(self, phrase, match, base_score=0):
        score = base_score
        score += 100 * fuzzy_match(phrase.lower(), match["title"].lower())
        return min(100, score)

    def get_playlist(self, score=50, num_entries=250):
        pl = self.featured_media()[:num_entries]
        return {
            "match_confidence": score,
            "media_type": MediaType.MOVIE,
            "playlist": pl,
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "title": "World Movie Central (Movie Playlist)",
            "author": "World Movie Central"
        }

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = self.match_skill(phrase, media_type)
        if self.voc_match(phrase, "worldmoviecentral"):
            yield self.get_playlist(base_score)
        if media_type == MediaType.MOVIE:
            # only search db if user explicitly requested movies
            phrase = self.normalize_title(phrase)
            for url, video in self.archive.db.items():
                yield {
                    "title": video["title"],
                    "author": "WorldMovie Central",
                    "match_confidence": self.calc_score(phrase, video, base_score),
                    "media_type": MediaType.MOVIE,
                    "uri": "youtube//" + url,
                    "playback": PlaybackType.VIDEO,
                    "skill_icon": self.skill_icon,
                    "skill_id": self.skill_id,
                    "image": video["thumbnail"]
                }

    @ocp_featured_media()
    def featured_media(self):
        return [{
            "title": video["title"],
            "image": video["thumbnail"],
            "match_confidence": 70,
            "media_type": MediaType.MOVIE,
            "uri": "youtube//" + video["url"],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "bg_image": video["thumbnail"],
            "skill_id": self.skill_id
        } for video in self.archive.sorted_entries()]


def create_skill():
    return WorldMovieCentralSkill()
