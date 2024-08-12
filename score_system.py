from static_objects.minecraft import MINECRAFT

class ScoreSystem:
    __score = 0
    def add_to_score(self, apple)->None:
        self.__score += 1
    def on_finish(self)->None:
        MINECRAFT.postToChat(f"Game end with score: {self.__score}")

SCORE_SYSTEM = ScoreSystem()