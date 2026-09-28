import asyncio
import pickle

# Global game state containing flattened package
game_state = {}

# Increment for how many players are connected
connected_players = 0

# Async means multiple clients can be run and they are run in "parallel" (just fast linear)
async def handle_client(reader, writer):
    # Increment connected players when new connection
    global connected_players
    connected_players += 1
    player_id = connected_players

    # Send player ID to the client before loop start
    writer.write(pickle.dumps(player_id))
    print("Client connected")
    await writer.drain()

    # Main loop for a connected player
    while True:
        # Try to fetch 2048 bytes of data from the player
        try:
            data = await reader.read(2048)
        except ConnectionResetError:
            # If there is no connection go to disconnect player
            break

        # If empty data break the loop and disconnect player
        if data == b'':
            break

        # Get the player state from their client
        new_player_state = pickle.loads(data)
        # Change the game_state to match users client
        game_state[player_id] = new_player_state

        # Write the global game state to send back to client
        writer.write(pickle.dumps(game_state))

        # Wait for it to send
        await writer.drain()

    # Disconnect player code
    connected_players -= 1
    del game_state[player_id] # Delete the player
    writer.close() # Close the clients writer

# Main server code
async def main():
    # Start a server that has the handle_client as default function when new connection
    server = await asyncio.start_server(handle_client, '0.0.0.0', 6967)
    # Let the server run forever
    await server.serve_forever()

asyncio.run(main())
