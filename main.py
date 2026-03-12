import pygame
import random
import os

# Inicialização
pygame.init()
try:
    pygame.mixer.init()
except:
    pass

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Shooter Anderson - Versão Definitiva")
relogio = pygame.time.Clock()

# --- SONS ---
def carregar_s(n):
    if os.path.exists(n):
        try: return pygame.mixer.Sound(n)
        except: return None
    return None

som_laser = carregar_s("laser.wav")
som_explosao = carregar_s("explosao.wav")

if os.path.exists("musica.mp3"):
    try:
        pygame.mixer.music.load("musica.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
    except: pass

# VARIÁVEIS GLOBAIS
nave_x, nave_y = 400, 550
vidas_atual = 3
pontos = 0
especial = 0
jogo_estado = "JOGANDO"
nome_entrada = ""
ranking_lista = []

# POWER-UPS E LISTAS
tiro_duplo_timer = 0
escudo_timer = 0
tiros, inimigos, powers, tiros_boss = [], [], [], []
estrelas = [[random.randint(0, 800), random.randint(0, 600)] for _ in range(40)]

# BOSS E CENÁRIO
boss_ativo = False
esperando_meta = True
boss_v_max, boss_v_atual = 30, 30
boss_x, boss_y, boss_dir = 350, -150, 1
timer_b, meta_boss = 0, 200
fundo_cor = (0, 0, 0)
inimigo_cor = (255, 0, 0)
boss_cor = (255, 128, 0)

def principal():
    global nave_x, vidas_atual, pontos, especial, jogo_estado, nome_entrada, ranking_lista, tiro_duplo_timer, escudo_timer, tiros, inimigos, powers, tiros_boss, boss_ativo, esperando_meta, boss_v_max, boss_v_atual, boss_x, boss_y, boss_dir, timer_b, meta_boss, fundo_cor, inimigo_cor, boss_cor
    
    while True:
        tela.fill(fundo_cor)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: return
            if ev.type == pygame.KEYDOWN:
                if jogo_estado == "JOGANDO":
                    if ev.key == pygame.K_SPACE:
                        if tiro_duplo_timer > 0:
                            tiros.append({"x": nave_x, "y": nave_y, "esp": False})
                            tiros.append({"x": nave_x + 24, "y": nave_y, "esp": False})
                        else:
                            tiros.append({"x": nave_x + 12, "y": nave_y, "esp": False})
                        if som_laser: som_laser.play()
                    if ev.key == pygame.K_x and especial >= 100:
                        tiros.append({"x": nave_x - 10, "y": nave_y - 20, "esp": True})
                        especial = 0
                        if som_laser: som_laser.play()
                
                elif jogo_estado == "DIGITANDO":
                    if ev.key == pygame.K_RETURN and len(nome_entrada) == 3:
                        ranking_lista.append({"nome": nome_entrada, "pts": pontos})
                        ranking_lista = sorted(ranking_lista, key=lambda k: k['pts'], reverse=True)
                        jogo_estado = "RANKING"
                    elif ev.key == pygame.K_BACKSPACE: nome_entrada = nome_entrada[:-1]
                    elif len(nome_entrada) < 3 and ev.unicode.isalpha(): nome_entrada += ev.unicode.upper()
                
                elif jogo_estado == "RANKING" and ev.key == pygame.K_c:
                    # Reset para nova partida
                    vidas_atual, pontos, meta_boss, boss_ativo, jogo_estado, especial = 3, 0, 200, False, "JOGANDO", 0
                    esperando_meta, fundo_cor, inimigo_cor, nome_entrada = True, (0,0,0), (255,0,0), ""
                    tiros.clear(); inimigos.clear(); tiros_boss.clear(); powers.clear()

        if jogo_estado == "JOGANDO":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and nave_x > 0: nave_x -= 8
            if keys[pygame.K_RIGHT] and nave_x < 770: nave_x += 8
            if tiro_duplo_timer > 0: tiro_duplo_timer -= 1
            if escudo_timer > 0: escudo_timer -= 1
            if especial < 100: especial += 0.5

            for e in estrelas:
                e[1] += 3
                if e[1] > 600: e[1] = 0
                pygame.draw.circle(tela, (150, 150, 150), e, 1)

            # LÓGICA DO BOSS
            if pontos >= meta_boss and esperando_meta:
                boss_ativo, esperando_meta = True, False
                boss_v_atual = boss_v_max
                boss_y, boss_cor = -100, (random.randint(100, 255), random.randint(50, 200), random.randint(0, 255))
                inimigos.clear()

            if boss_ativo:
                if boss_y < 60: boss_y += 2
                boss_x += 5 * boss_dir
                if boss_x > 680 or boss_x < 20: boss_dir *= -1
                pygame.draw.rect(tela, boss_cor, (boss_x, boss_y, 120, 90))
                timer_b += 1
                if timer_b > 40:
                    tiros_boss.append({"x": boss_x + 55, "y": boss_y + 90})
                    timer_b = 0
            else:
                if len(inimigos) < 8:
                    inimigos.append([random.randint(10, 760), -40, random.randint(4, 7)])

            # Power-ups movimento
            for p in powers[:]:
                p["y"] += 4
                cor_p = (255, 255, 0) if p["tipo"] == "duplo" else (0, 200, 255)
                pygame.draw.circle(tela, cor_p, (p["x"], p["y"]), 15)
                if abs(p["x"] - (nave_x+15)) < 35 and abs(p["y"] - (nave_y+15)) < 35:
                    if p["tipo"] == "duplo": tiro_duplo_timer = 500
                    else: escudo_timer = 300
                    powers.remove(p)
                elif p["y"] > 600: powers.remove(p)

            # Tiros Boss
            for tb in tiros_boss[:]:
                tb["y"] += 8
                pygame.draw.rect(tela, (255, 255, 255), (tb["x"], tb["y"], 10, 10))
                if tb["y"]+10 > nave_y and tb["x"] < nave_x+30 and tb["x"]+10 > nave_x:
                    if escudo_timer <= 0: vidas_atual -= 1
                    tiros_boss.remove(tb)
                    if som_explosao: som_explosao.play()
                elif tb["y"] > 600: tiros_boss.remove(tb)

            # Inimigos Pequenos
            for i in inimigos[:]:
                i[1] += i[2]
                pygame.draw.rect(tela, inimigo_cor, (i[0], i[1], 30, 30))
                if i[1]+30 > nave_y and i[0] < nave_x+30 and i[0]+30 > nave_x:
                    if escudo_timer <= 0: vidas_atual -= 1
                    inimigos.remove(i)
                    if som_explosao: som_explosao.play()
                elif i[1] > 600: inimigos.remove(i)

            # Tiros Jogador e Colisões
            for t in tiros[:]:
                t["y"] -= 12
                c = (0, 255, 255) if t["esp"] else (255, 255, 0)
                w, h = (50, 25) if t["esp"] else (6, 12)
                pygame.draw.rect(tela, c, (t["x"], t["y"], w, h))
                if boss_ativo and t["y"] < boss_y+90 and t["x"] < boss_x+120 and t["x"]+w > boss_x:
                    boss_v_atual -= 5 if t["esp"] else 1
                    if not t["esp"]: tiros.remove(t)
                    if som_explosao: som_explosao.play()
                    if boss_v_atual <= 0:
                        boss_ativo, pontos, esperando_meta = False, pontos + 500, True
                        meta_boss = pontos + 200
                        boss_v_max += 15
                        fundo_cor = (random.randint(0, 40), random.randint(0, 40), random.randint(0, 40))
                        inimigo_cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                        tiros_boss.clear()
                else:
                    for i in inimigos[:]:
                        if t["y"] < i[1]+30 and t["x"] < i[0]+30 and t["x"]+w > i[0]:
                            if random.random() < 0.12:
                                powers.append({"x": i[0], "y": i[1], "tipo": random.choice(["duplo", "escudo"])})
                            inimigos.remove(i)
                            if not t["esp"]: tiros.remove(t)
                            pontos += 10
                            if som_explosao: som_explosao.play()
                            break
                if t["y"] < -50 and t in tiros: tiros.remove(t)

            # Interface
            if escudo_timer > 0: pygame.draw.circle(tela, (0, 150, 255), (nave_x+15, nave_y+15), 45, 2)
            pygame.draw.polygon(tela, (0, 255, 0), [(nave_x, nave_y+30), (nave_x+15, nave_y), (nave_x+30, nave_y+30)])
            f = pygame.font.SysFont("Arial", 20, True)
            tela.blit(f.render(f"PONTOS: {pontos}", 1, (255,255,255)), (20, 10))
            pygame.draw.rect(tela, (0, 150, 255), (120, 45, especial, 12))
            pygame.draw.rect(tela, (0, 255, 0), (120, 75, max(0, (vidas_atual/3)*100), 12))
            if boss_ativo:
                larg_b = max(0, (boss_v_atual / boss_v_max) * 200)
                pygame.draw.rect(tela, (50, 50, 50), (350, 15, 200, 15)); pygame.draw.rect(tela, boss_cor, (350, 15, larg_b, 15))

            if vidas_atual <= 0: jogo_estado = "DIGITANDO"

        elif jogo_estado == "DIGITANDO":
            f_g = pygame.font.SysFont("Arial", 40, True)
            tela.blit(f_g.render("FIM DE JOGO!", 1, (255,0,0)), (280, 150))
            tela.blit(f_g.render(f"NOME: {nome_entrada}", 1, (255,255,255)), (280, 250))
            tela.blit(f_g.render("DIGITE 3 LETRAS E ENTER", 1, (100,100,100)), (200, 400))

        elif jogo_estado == "RANKING":
            f_r = pygame.font.SysFont("Arial", 35, True)
            tela.blit(f_r.render("TOP 10 RECORDES", 1, (255, 255, 0)), (250, 50))
            for idx, item in enumerate(ranking_lista[:10]):
                txt = f"{idx+1}º {item['nome']} - {item['pts']} pts"
                tela.blit(f_r.render(txt, 1, (255, 255, 255)), (250, 110 + (idx * 35)))
            tela.blit(f_r.render("APERTE C PARA VOLTAR", 1, (0, 255, 0)), (220, 520))
        
        pygame.display.flip()
        relogio.tick(60)

principal()
pygame.quit()