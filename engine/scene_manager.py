from content.scenes import SCENES
from engine.game_state import GameState


class SceneManager:
    def __init__(self):
        self.scenes = SCENES

    def current_scene(self, state: GameState):
        return self.scenes[state.current_scene]

    def try_advance(self, state: GameState, intent: str) -> tuple[bool, str]:
        """
        Intenta avanzar de escena según la intención detectada.
        Devuelve (hubo_cambio, nuevo_scene_id).
        """
        scene = self.current_scene(state)
        next_scene_id = scene.advance_conditions.get(intent)
        if next_scene_id:
            state.current_scene = next_scene_id
            new_scene = self.scenes[next_scene_id]
            if new_scene.is_ending:
                state.game_over = True
                state.ending_type = new_scene.ending_type
            return True, next_scene_id
        return False, state.current_scene

    def get_scene_intro(self, scene_id: str) -> str:
        return self.scenes[scene_id].description
