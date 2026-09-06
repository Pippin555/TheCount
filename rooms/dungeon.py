# def dungeon_handler(verb: str, noun: str, location: str) -> str:
#     """ ... """
#
#     _ = location
#
#     match verb:
#         case "UP":
#             return GameHandler.enter("workroom")
#         case "HELP":
#             if noun is None:
#                 return "Problem with the pit?, try HELP PIT"
#             if noun == 'PIT':
#                 return "remember the bed"
#         case "TIE":
#             if noun == "SHEET":
#                 return "To what"
#
#         case "TO":
#             if noun == "RINGS":
#                 item = game.drop_inventory("sheet")
#                 if item is None:
#                     return "I do not have a sheet"
#                 rooms = game.rooms()
#                 room = rooms.get(game.location, None)
#                 obj: set = room['free_objects']
#                 obj.add(item)
#                 return "tied to rings"
#
#     return GameHandler.general(verb, noun, location)
