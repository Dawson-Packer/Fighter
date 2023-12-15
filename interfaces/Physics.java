package interfaces;

import interfaces.config.PlayerSettings;

@FunctionalInterface
public interface Physics {

    public PlayerSettings.player_status process_physics();

}
