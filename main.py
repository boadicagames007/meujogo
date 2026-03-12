import pygame
import asyncio

async def main():
    pygame.init()
    # Criando a tela do Dandan Game Studio
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dandan Game Studio - ONLINE")
    
    nave_x = 400
    rodando = True

    while rodando:
        tela.fill((0, 0, 20)) # Fundo azul escuro espacial
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimento simples
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: nave_x -= 5
        if teclas[pygame.K_RIGHT]: nave_x += 5

        # Desenha a nave (um triângulo verde)
        pygame.draw.polygon(tela, (0, 255, 0), [(nave_x, 550), (nave_x+20, 520), (nave_x+40, 550)])
        
        pygame.display.flip()
        # O SEGREDO: Essa linha abaixo destrava o carregamento
        await asyncio.sleep(0) 

asyncio.run(main())
