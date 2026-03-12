import pygame
import random
import asyncio # Isso aqui é o que destrava a tela preta

async def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    relogio = pygame.time.Clock()

    # VARIÁVEIS
    nave_x, nave_y = 400, 550
    pontos = 0
    tiros, inimigos = [], []
    jogo_ativo = True

    while jogo_ativo:
        tela.fill((0, 0, 0)) # Fundo preto
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: jogo_ativo = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    tiros.append([nave_x + 15, nave_y])

        # Movimento
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and nave_x > 0: nave_x -= 8
        if keys[pygame.K_RIGHT] and nave_x < 770: nave_x += 8

        # Inimigos
        if len(inimigos) < 5:
            inimigos.append([random.randint(0, 770), 0])

        for i in inimigos[:]:
            i[1] += 5
            pygame.draw.rect(tela, (255, 0, 0), (i[0], i[1], 30, 30))
            if i[1] > 600: inimigos.remove(i)

        for t in tiros[:]:
            t[1] -= 10
            pygame.draw.rect(tela, (255, 255, 0), (t[0], t[1], 5, 10))
            if t[1] < 0: tiros.remove(t)

        # Desenho Nave
        pygame.draw.polygon(tela, (0, 255, 0), [(nave_x, nave_y+30), (nave_x+15, nave_y), (nave_x+30, nave_y+30)])

        pygame.display.flip()
        await asyncio.sleep(0) # ESSENCIAL: Isso avisa o navegador para rodar o jogo
        relogio.tick(60)

asyncio.run(main())
