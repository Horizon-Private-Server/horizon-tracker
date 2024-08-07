
# Horizon DL WebSocket Interface

## Connecting and Authentication

Connecting to the WebSocket requires an access token. This access token is persistent until
a user logs out (which forcibly changes the token).

When connecting to the Horizon Stats API, the following URL is used:
`wss://stats.rac-horizon.com/ws/session?token=<token>`
> Because the WebSocket will use SSL, everything after the domain will be encrypted, including the session token.

The connection is maintained and follows the standard WebSocket protocol, including for heartbeats.

## Message ID Space

| Address Space | Usage                                                |
|---------------|------------------------------------------------------|
| 0-9           | Menu signals (e.g., OnLogin, GameStart and GameEnd). |
| 10-49         | Multiplayer standard messages.                       |
| 50-99         | Multiplayer custom messages                          |
| 100-149       | Survival messages.                                   |
| 150-199       | Reserved future PvE messages.                        |
| 200-299       | Response Signals.                                    |
| 300-399       | Reserved Response Signals.                           |
| 400-599       | Error Responses.                                     |

# Transmit

### On Login

Login requests are sent when a user accepts the license agreement at the main menu.

> This is not used for tracking online status, only to tie users with an account.

```json
{
  "type": 0,
  "account": <str:name>
}
```

### Lobby Join

Used to signify when a player joins a lobby.

```json
{
  "type": 1
}
```

### Lobby Leave

Used to signify when a player leaves a lobby.

```json
{
  "type": 2
}
```

### Game Start

Used to signify when a game starts.
Sent by each DZO player in the game.
The only difference in this message is the team each player is on.

```json
{
  "type": 3,
  "id": <uuid:game_id>,
  "team": <int:color_index>,
  "settings": {
    "mode": <str:game_mode>,
    "map": <str:map>,
    "weapons": [0, 1, 0, 1, 0, 1, 0, 0],
    "rules": {
      ...
    },
    "custom_rules": {
      ...
    }
  }
}
```

### Game End
```json
{
  "type": 4,
  "id": <uuid:game_id>
}
```

### Events

#### Kill Event

###### Source Types

Sources are the methods by which a player kills another player.

| Type           | ID  |
|----------------|-----|
| DUAL_VIPERS    | 0   |
| DUAL_VIPERS_2  | 1   |
| MAGMA_CANNON   | 2   |
| MAGMA_CANNON_2 | 3   |
| ARBITER        | 4   |
| ARBITER_2      | 5   |
| B6             | 6   |
| B6_2           | 7   |
| FUSION         | 8   |
| FUSION_2       | 9   |
| MINES          | 10  |
| MINES_2        | 11  |
| HOLOSHIELD     | 12  |
| HOLOSHIELD_2   | 13  |
| FLAIL          | 14  |
| FLAIL_2        | 15  |
| WRENCH         | 16  |
| VEHICLE_SHOT   | 17  |
| ROADKILL       | 18  |

###### Condition Types

Conditions are special circumstances in which a player is killed.

| Type                  | ID  |
|-----------------------|-----|
| NONE                  | 0   |
| CQ_DEFENSIVE_KILL     | 1   |
| CQ_SNIPER_KILL        | 2   |
| CQ_WRENCH_KILL        | 3   |
| CQ_MULTIKILL          | 4   |
| CQ_ROADKILL           | 5   |
| CTF_DEFENSIVE_KILL?   | 6   |
| JUGG_TAKEDOWN         | 7   |
| CTF_FLAG_CARRIER_KILL | 8   |

```json
{
  "type": 10,
  "victim": <str:player_name>,
  "source": <int:source_type>,
  "condition": <int:condition_type>
}
```

#### Suicide

```json
{
  "type": 11
}
```

#### Flag Captured
```json
{
  "type": 12
}
```

#### Flag Saved
```json
{
  "type": 13
}
```

#### Node Captured
```json
{
  "type": 14
}
```

#### Juggernaut Start
```json
{
  "type": 15,
  "timestamp": <str:ISO8601_standard_UTC_timestamp>
}
```

#### Juggernaut End
```json
{
  "type": 16,
  "timestamp": <str:ISO8601_standard_UTC_timestamp>
}
```

#### Enter Hill
```json
{
  "type": 17,
  "timestamp": <str:ISO8601_standard_UTC_timestamp>
}
```

#### Exit Hill
```json
{
  "type": 18,
  "timestamp": <str:ISO8601_standard_UTC_timestamp>
}
```

### Client-sent Unlock

Unlock is a custom hook intended to allow a client to self-unlock an achievement if it cannot be
done on the server-side.

```json
    "type": 20,
    "name": <str:achievement_name>
```

# Receive

### All Players' Status

| Player Status         | ID  |
|-----------------------|-----|
| IN MENUS              | 0   |
| IN LOBBY              | 1   |
| IN GAME               | 2   |

Sent to a new session on open.
This describes the current state of all online players.

```json
{
  "type": 200,
  "count": <int:players_count>,
  "players": [
    {
      "name": <str:name>,
      "status": <int:player_status>
    },
    ...
  ]
}
```

### Player Online

Sent to all active sessions when a new player opens the DZO client and starts a session.
It can be assumed that the player's status will be `IN MENUS (0)`.

```json
{
  "type": 201,
  "message": <str:message>
}
```

### Player Offline

Sent to all active sessions when a player's session is closed.

```json
{
  "type": 202,
  "message": <str:message>
}
```

### Player Status Update

Sent to all active sessions when a player's status changes.

```json
{
  "type": 203,
  "name": <str:name>,
  "status": <int:player_status>
}
```

### Server-sent Unlock

Whenever the server determines that you have unlocked an achievement, it will send it to the client.

###### Achievement Values

| Value   | ID  |
|---------|-----|
| BRONZE  | 0   |
| SILVER  | 1   |
| GOLD    | 2   |
| DIAMOND | 3   |

```json
    "type": 210,
    "name": <str:achievement_name>,
    "earned": <int:amount_earned>,
    "required": <int:amount_required>,
    "value": <int:achievement_value>
```

### Progress Updates

After certain event, the server may end updates indicating the progress on an achievement.

```json
{
  "type": 211,
  "name": <str:achievement_name>,
  "earned": <int:amount_earned>,
  "required": <int:amount_required>,
  "value": <int:achievement_value>
}
```

### Level Up

Sent after the server determines you've earned enough experience points to level up.
This response will also send the following useful stats: `total` - The player's total XP, `current` - The XP required for a player to reach their current level, `required` - The total XP required to reach the next level.

> __NOTE:__ For simplicity: `current` `<=` `total` `<` `required`.

```json
{
  "type": 212,
  "level": <int:new_level>,
  "total": <int:total_xp>,
  "current": <int:current_xp_required_for_level>,
  "required": <int:xp_required_for_next_level>
}
```

### Notification

Message reserved for notifications.

```json
{
  "type": 212,
  "message": <str:message>
}
```

### MOTD

Message reserved for the MOTD.

```json
{
  "type": 213,
  "message": <str:motd>
}
```

# Errors

All errors will be in the following format.

```json
{
  "error": <int:error_id>
}
```

### `400` - Not in a game.
Returned if a WebSocket Message between 10-199 is not received in-between a GameStart (`3`) and GameEnd (`4`) message.

### `404` - Message Type not defined 
Returned if a WebSocket Message uses an ID that is not defined in the spec.

### `410` - Person Un-killable
A WS410 message is returned whem the killer does not have the ability to kill the victim (e.g., friendly fire).
