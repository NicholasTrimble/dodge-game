import asyncio, random, pygame
pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Block")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)
bigfont = pygame.font.SysFont(None, 36)

player = pygame.Rect(WIDTH//2-20, HEIGHT-40, 40, 20)
blocks = []
speed = 11
running = True
game_over = False
SCORE = 0

async def main():
    global running, game_over, blocks, player, SCORE
    spawn_timer = 0

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r and game_over:
                    player = pygame.Rect(WIDTH//2-20, HEIGHT-40, 40, 20)
                    blocks = []
                    game_over = False
                    SCORE = 0
                if e.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]: player.x -= 5
            if keys[pygame.K_RIGHT]: player.x += 5
            player.x = max(0, min(WIDTH-player.width, player.x))

        if not game_over:
            spawn_timer += 2
            if spawn_timer > 30:
                spawn_timer = 0
                blocks.append(pygame.Rect(random.randint(0, WIDTH-20), -20, 20, 20))
            for b in blocks: b.y += speed
            for b in blocks:
                if b.colliderect(player):
                    game_over = True
                    break
            # count blocks that pass the bottom as points
            still_there = []
            for b in blocks:
                if b.top > HEIGHT:
                    SCORE += 1
                else:
                    still_there.append(b)
            blocks = still_there

        screen.fill((30,30,30))
        pygame.draw.rect(screen,(50,200,50),player)
        for b in blocks: pygame.draw.rect(screen,(200,50,50),b)
        info = f"Score: {SCORE}   (R restart)"
        screen.blit(font.render(info,1,(230,230,230)),(8,8))

        if game_over:
            screen.blit(bigfont.render("Game Over!",1,(255,80,80)),(WIDTH//2-bigfont.size("Game Over!")[0]//2, HEIGHT//2-20))
            screen.blit(font.render(f"Final score: {SCORE}   Press R",1,(240,240,240)),(WIDTH//2-font.size(f"Final score: {SCORE}   Press R")[0]//2, HEIGHT//2+20))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
