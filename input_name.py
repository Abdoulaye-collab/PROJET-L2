import pygame

def input_names(screen):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 35)
    clock = pygame.time.Clock()
    input_box_player = pygame.Rect(300, 200, 300, 50)
    input_box_ai = pygame.Rect(300, 300, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_player = color_inactive
    color_ai = color_inactive
    active_player = False
    active_ai = False
    text_player = ''
    text_ai = 'IA'
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_player.collidepoint(event.pos):
                    active_player = True
                    active_ai = False
                elif input_box_ai.collidepoint(event.pos):
                    active_ai = True
                    active_player = False
                else:
                    active_player = active_ai = False
                color_player = color_active if active_player else color_inactive
                color_ai = color_active if active_ai else color_inactive
            if event.type == pygame.KEYDOWN:
                if active_player:
                    if event.key == pygame.K_RETURN:
                        active_player = False
                        color_player = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_player = text_player[:-1]
                    else:
                        text_player += event.unicode
                elif active_ai:
                    if event.key == pygame.K_RETURN:
                        active_ai = False
                        color_ai = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_ai = text_ai[:-1]
                    else:
                        text_ai += event.unicode
                if event.key == pygame.K_RETURN and text_player.strip() != '':
                    done = True

        screen.fill((0, 105, 148))
        instr_surf = font.render("Entrez le nom du joueur et de l'IA puis ENTER", True, (255,255,255))
        screen.blit(instr_surf, (50,100))
        pygame.draw.rect(screen, color_player, input_box_player, 2)
        pygame.draw.rect(screen, color_ai, input_box_ai, 2)
        screen.blit(font.render(text_player, True, (255,255,255)), (input_box_player.x+5, input_box_player.y+5))
        screen.blit(font.render(text_ai, True, (255,255,255)), (input_box_ai.x+5, input_box_ai.y+5))

        pygame.display.flip()
        clock.tick(30)

    return text_player.strip(), text_ai.strip() or "IA"
