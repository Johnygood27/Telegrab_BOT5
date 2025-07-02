kills_text = self.small_font.render(f"Убийств: {gorilla.kills}", True, (255, 150, 150))
        screen.blit(kills_text, (150 + shake_offset_x, 110 + shake_offset_y))
        
        # Время игры и время суток
        time_text = self.font.render(f"Время: {time_passed:.1f} сек", True, WHITE)
        screen.blit(time_text, (WIDTH - 170 + shake_offset_x, 15 + shake_offset_y))
        
        time_names = ["Утро", "День", "Вечер", "Ночь"]
        time_info = self.small_font.render(f"Время суток: {time_names[time_manager.time_of_day]}", True, WHITE)
        screen.blit(time_info, (WIDTH - 170 + shake_offset_x, 45 + shake_offset_y))
        
        day_info = self.small_font.render(f"День: {time_manager.day_count}", True, WHITE)
        screen.blit(day_info, (WIDTH - 170 + shake_offset_x, 65 + shake_offset_y))
        
        # Погода
        weather_types = {
            "clear": "Ясно",
            "rain": "Дождь",
            "wind": "Ветер"
        }
        weather_info = self.small_font.render(f"Погода: {weather_types.get(environment.weather_type, 'Неизвестно')}", True, WHITE)
        screen.blit(weather_info, (WIDTH - 170 + shake_offset_x, 85 + shake_offset_y))
        
        # Режим ярости
        if gorilla.rage_mode:
            rage_text = self.font.render("РЕЖИМ ЯРОСТИ!", True, RED)
            screen.blit(rage_text, (WIDTH // 2 - rage_text.get_width() // 2 + shake_offset_x, 15 + shake_offset_y))
            rage_timer = self.small_font.render(f"Осталось: {gorilla.rage_timer // 60 + 1} сек", True, (255, 150, 150))
            screen.blit(rage_timer, (WIDTH // 2 - rage_timer.get_width() // 2 + shake_offset_x, 45 + shake_offset_y))
        
        # Неуязвимость
        if gorilla.invulnerable:
            invuln_text = self.small_font.render("Неуязвимость", True, (255, 215, 0))
            screen.blit(invuln_text, (WIDTH // 2 - invuln_text.get_width() // 2 + shake_offset_x, 
                                    15 + (0 if not gorilla.rage_mode else 75) + shake_offset_y))
        
        # Способности гориллы
        ability_names = {
            "pound": "Удар кулаком",
            "throw": "Захват",
            "roar": "Рёв",
            "leap": "Прыжок"
        }
        
        ability_bg = pygame.Surface((300, 30), pygame.SRCALPHA)
        ability_bg.fill((0, 0, 0, 120))
        screen.blit(ability_bg, (WIDTH // 2 - 150 + shake_offset_x, HEIGHT - 40 + shake_offset_y))
        
        ability_x = WIDTH // 2 - 140 + shake_offset_x
        for ability_name, ability in gorilla.abilities.items():
            if ability["unlocked"]:
                ability_rect = pygame.Rect(ability_x, HEIGHT - 35 + shake_offset_y, 60, 20)
                
                # Фон кнопки способности
                if ability["current_cooldown"] <= 0:
                    pygame.draw.rect(screen, (50, 150, 50), ability_rect, border_radius=3)
                else:
                    cooldown_percent = ability["current_cooldown"] / ability["cooldown"]
                    pygame.draw.rect(screen, (100, 100, 100), ability_rect, border_radius=3)
                    pygame.draw.rect(screen, (50, 150, 50), 
                                   (ability_rect.x, ability_rect.y, int(ability_rect.width * (1 - cooldown_percent)), ability_rect.height), 
                                   border_radius=3)
                
                # Текст способности
                ability_text = self.tiny_font.render(ability_names.get(ability_name, ability_name), True, WHITE)
                text_x = ability_rect.centerx - ability_text.get_width() // 2
                text_y = ability_rect.centery - ability_text.get_height() // 2
                screen.blit(ability_text, (text_x, text_y))
                
                # Если кулдаун, показываем оставшееся время
                if ability["current_cooldown"] > 0:
                    cooldown_text = self.tiny_font.render(f"{ability['current_cooldown'] // 60 + 1}", True, WHITE)
                    screen.blit(cooldown_text, (ability_rect.right - cooldown_text.get_width() - 3, 
                                              ability_rect.bottom - cooldown_text.get_height() - 2))
                    
                ability_x += 70
        
        # Отображение FPS
        if self.show_fps:
            fps = int(clock.get_fps())
            fps_color = (0, 255, 0) if fps > 40 else (255, 255, 0) if fps > 20 else (255, 0, 0)
            fps_text = self.small_font.render(f"FPS: {fps}", True, fps_color)
            screen.blit(fps_text, (WIDTH - 90 + shake_offset_x, HEIGHT - 30 + shake_offset_y))
        
        # Отображение уведомлений
        notification_y = 150 + shake_offset_y
        for notification in self.notifications:
            text = self.font.render(notification['text'], True, notification['color'])
            text.set_alpha(notification['alpha'])
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2 + shake_offset_x, notification_y))
            notification_y += 30
        
        # Отображение миникарты
        if self.show_minimap:
            # Фон миникарты
            minimap_bg = pygame.Surface((self.minimap_size, self.minimap_size), pygame.SRCALPHA)
            minimap_bg.fill((0, 0, 0, 150))
            screen.blit(minimap_bg, self.minimap_pos)
            
            # Рамка миникарты
            pygame.draw.rect(screen, (200, 200, 200, 100), 
                           (self.minimap_pos[0], self.minimap_pos[1], self.minimap_size, self.minimap_size), 
                           1)
            
            # Отображение людей на миникарте
            for human in humans:
                if human.health > 0:
                    # Выбираем цвет в зависимости от типа
                    if human.type == "warrior":
                        color = (200, 50, 50)
                    elif human.type == "archer":
                        color = (50, 200, 50)
                    else:  # civilian
                        color = (50, 150, 255)
                        
                    # Рисуем точку на миникарте
                    mini_x = self.minimap_pos[0] + int(human.x * self.minimap_scale)
                    mini_y = self.minimap_pos[1] + int(human.y * self.minimap_scale)
                    pygame.draw.circle(screen, color, (mini_x, mini_y), 1)
            
            # Отображение гориллы на миникарте
            gorilla_mini_x = self.minimap_pos[0] + int(gorilla.x * self.minimap_scale)
            gorilla_mini_y = self.minimap_pos[1] + int(gorilla.y * self.minimap_scale)
            gorilla_mini_size = 3
            if gorilla.rage_mode:
                gorilla_mini_size = 4
                pygame.draw.circle(screen, (255, 100, 0), (gorilla_mini_x, gorilla_mini_y), 5, 1)
                
            pygame.draw.circle(screen, (139, 69, 19), (gorilla_mini_x, gorilla_mini_y), gorilla_mini_size)
        
        # Отладочная информация
        if self.show_debug:
            debug_font = pygame.font.SysFont('Consolas', 14)
            humans_by_zone = [0, 0, 0, 0]
            humans_by_type = {"civilian": 0, "warrior": 0, "archer": 0}
            humans_by_state = {"idle": 0, "chase": 0, "flee": 0, "attack": 0, "ranged_attack": 0, "group": 0}
            
            for human in humans:
                if human.health <= 0:
                    continue
                    
                # Распределение по зонам детализации
                dist = math.hypot(human.x - gorilla.x, human.y - gorilla.y)
                if dist < DETAIL_LEVELS['full']:
                    humans_by_zone[0] += 1
                elif dist < DETAIL_LEVELS['medium']:
                    humans_by_zone[1] += 1
                elif dist < DETAIL_LEVELS['low']:
                    humans_by_zone[2] += 1
                else:
                    humans_by_zone[3] += 1
                
                # Распределение по типам
                humans_by_type[human.type] += 1
                
                # Распределение по состояниям
                humans_by_state[human.state] += 1
                
            debug_info = [
                f"Gorilla: ({int(gorilla.x)}, {int(gorilla.y)}), HP: {int(gorilla.health)}/{gorilla.max_health}, Lvl: {gorilla.level}",
                f"Exp: {gorilla.experience}/{gorilla.experience_to_level}, State: {gorilla.state}",
                f"Particles: {len(gorilla.particles.particles)}, Environment: {environment.weather_type}",
                f"Humans alive: {alive_humans}/{len(humans)}, By type: {humans_by_type}",
                f"Humans by detail: {humans_by_zone}",
                f"Humans by state: {humans_by_state}",
                f"Rage mode: {gorilla.rage_mode}, Invulnerable: {gorilla.invulnerable}"
            ]
            
            debug_bg = pygame.Surface((400, len(debug_info) * 20 + 10), pygame.SRCALPHA)
            debug_bg.fill((0, 0, 0, 120))
            screen.blit(debug_bg, (10, HEIGHT - len(debug_info) * 20 - 20))
            
            for i, info in enumerate(debug_info):
                debug_text = debug_font.render(info, True, (200, 200, 200))
                screen.blit(debug_text, (15, HEIGHT - len(debug_info) * 20 - 10 + i * 20))

    def draw_end_screen(self, screen, winner, simulation_duration, alive_humans, kills, time_manager):
        # Создаем затемненный фон
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Контейнер результатов
        container_width = 500
        container_height = 350
        container_x = WIDTH // 2 - container_width // 2
        container_y = HEIGHT // 2 - container_height // 2
        
        container = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
        container.fill((30, 30, 50, 180))
        screen.blit(container, (container_x, container_y))
        
        # Красивая рамка
        pygame.draw.rect(screen, (200, 200, 255, 200),
                       (container_x, container_y, container_width, container_height), 2, border_radius=10)
        
        # Декоративные элементы
        for i in range(5):
            pygame.draw.rect(screen, (100 + i*20, 100 + i*20, 150 + i*20, 50),
                           (container_x + 2 + i, container_y + 2 + i, container_width - 4 - i*2, container_height - 4 - i*2), 
                           1, border_radius=10-i)
        
        # Заголовок результатов
        title_color = GOLD if winner == "Горилла" else (100, 200, 255)
        result_text = self.title_font.render(f"Победитель: {winner}!", True, title_color)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, container_y + 30))
        
        # Подзаголовок
        subtitle = self.font.render("Результаты симуляции", True, WHITE)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, container_y + 70))
        
        # Статистика
        stats = [
            f"Время симуляции: {simulation_duration:.1f} сек",
            f"Прошло дней: {time_manager.day_count}",
            f"Выжило людей: {alive_humans} из {HUMAN_COUNT}",
            f"Убийств гориллы: {kills}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font.render(stat, True, WHITE)
            screen.blit(stat_text, (WIDTH // 2 - stat_text.get_width() // 2, container_y + 110 + i * 30))
        
        # Дополнительная информация
        if winner == "Горилла":
            extra_text = self.small_font.render("Горилла доказала своё превосходство!", True, (255, 220, 100))
        else:
            extra_text = self.small_font.render("Люди одержали победу совместными усилиями!", True, (100, 200, 255))
            
        screen.blit(extra_text, (WIDTH // 2 - extra_text.get_width() // 2, container_y + 230))
        
        # Инструкция для перезапуска
        restart_text = self.font.render("Нажмите R для перезапуска", True, (255, 255, 100))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, container_y + 280))
        
        # Дополнительная инструкция для выхода
        exit_text = self.small_font.render("ESC - выход", True, (200, 200, 200))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, container_y + 320))

def show_intro_screen(screen):
    # Фоновое изображение
    screen.blit(background_img, (0, 0))
    
    # Затемнение
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Анимация титульного текста
    title_font = pygame.font.SysFont('Arial', 48)
    title_text = title_font.render("1 ГОРИЛЛА vs 1000 ЛЮДЕЙ", True, (255, 220, 100))
    shadow_text = title_font.render("1 ГОРИЛЛА vs 1000 ЛЮДЕЙ", True, (0, 0, 0))
    
    # Эффект пульсации
    time_passed = pygame.time.get_ticks() / 1000
    pulse = 1.0 + math.sin(time_passed * 2) * 0.05
    pulsed_width = int(title_text.get_width() * pulse)
    pulsed_height = int(title_text.get_height() * pulse)
    pulsed_title = pygame.transform.scale(title_text, (pulsed_width, pulsed_height))
    
    # Тень текста
    screen.blit(shadow_text, (WIDTH // 2 - shadow_text.get_width() // 2 + 3, HEIGHT // 2 - 103))
    screen.blit(pulsed_title, (WIDTH // 2 - pulsed_width // 2, HEIGHT // 2 - 100))
    
    # Подзаголовок
    subtitle_font = pygame.font.SysFont('Arial', 24)
    subtitle = subtitle_font.render("Реалистичная Симуляция", True, (200, 200, 255))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 - 40))
    
    # Версия
    version_font = pygame.font.SysFont('Arial', 12)
    version_text = version_font.render("v2.0", True, (150, 150, 150))
    screen.blit(version_text, (WIDTH - version_text.get_width() - 10, HEIGHT - version_text.get_height() - 10))
    
    # Инструкции
    instructions = [
        "Реалистичная симуляция битвы гориллы против людей",
        "Горилла набирает опыт и разблокирует новые способности",
        "Люди используют разные тактики и типы (воины, лучники, гражданские)",
        "Реалистичные погодные эффекты и смена дня/ночи",
        "Динамическая окружающая среда с различными типами местности",
        "",
        "Управление:",
        "F - показать/скрыть FPS",
        "D - показать/скрыть отладочную информацию",
        "M - показать/скрыть миникарту",
        "H - показать/скрыть подсказки",
        "",
        "Нажмите любую клавишу для начала"
    ]
    
    font = pygame.font.SysFont('Arial', 18)
    for i, line in enumerate(instructions):
        if i == 6:  # Заголовок "Управление"
            instr_text = font.render(line, True, (255, 200, 100))
        elif i == 12:  # "Нажмите любую клавишу"
            instr_text = font.render(line, True, (200, 255, 100))
        else:
            instr_text = font.render(line, True, (200, 200, 200))
            
        screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2 + 20 + i * 25))
    
    # Анимированные частицы на фоне
    particle_system = ParticleSystem()
    for _ in range(20):
        particle_system.add(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)),
            random.uniform(1, 3),
            random.uniform(0.5, 1.5),
            random.randint(100, 200)
        )
    
    # Логотип гориллы
    gorilla_logo = pygame.transform.scale(gorilla_img, (160, 160))
    screen.blit(gorilla_logo, (WIDTH // 2 - 80, 50))
    
    pygame.display.flip()
    
    # Обработка ввода
    wait = True
    start_time = pygame.time.get_ticks()
    while wait:
        current_time = pygame.time.get_ticks()
        
        # Обновляем частицы
        particle_system.update()
        particle_system.draw(screen)
        
        # Обновляем дисплей
        if (current_time - start_time) % 50 == 0:  # Периодическое обновление для анимации
            pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pygame.time.wait(30)

def main():
    # Инициализация
    time_manager = TimeManager()
    environment = EnvironmentEffect()
    ui = GameUI()
    
    # Создаем пространственную хеш-таблицу для оптимизации поиска
    spatial_hash = SpatialHash(SPATIAL_HASH_CELL_SIZE)
    
    # Создаем препятствия на карте
    obstacles = []
    for _ in range(15):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        obstacle_type = random.choice(["rock", "tree"])
        size = random.randint(20, 40)
        obstacles.append(Obstacle(x, y, obstacle_type, size))
    
    # Создаем гориллу
    gorilla = Gorilla()
    
    # Создаем людей с различными типами на основе вероятностей
    humans = []
    for i in range(HUMAN_COUNT):
        human_type = random.choices(
            list(HUMAN_TYPES.keys()), 
            weights=[HUMAN_TYPES[t]['prob'] for t in HUMAN_TYPES.keys()]
        )[0]
        humans.append(Human(human_type))
    
    # Распределяем людей более равномерно по карте
    for i, human in enumerate(humans):
        sector_size = 150
        sectors_x = WIDTH // sector_size
        sectors_y = HEIGHT // sector_size
        sector_x = i % sectors_x
        sector_y = (i // sectors_x) % sectors_y
        human.x = sector_x * sector_size + random.randint(20, sector_size - 20)
        human.y = sector_y * sector_size + random.randint(20, sector_size - 20)
        
        # Проверка расстояния до гориллы
        dist_to_gorilla = math.hypot(human.x - gorilla.x, human.y - gorilla.y)
        if dist_to_gorilla < 100:
            angle = random.uniform(0, 2 * math.pi)
            human.x = gorilla.x + math.cos(angle) * 150
            human.y = gorilla.y + math.sin(angle) * 150
            
        # Проверка столкновений с препятствиями
        for obstacle in obstacles:
            dist_to_obstacle = math.hypot(human.x - obstacle.x, human.y - obstacle.y)
            if dist_to_obstacle < human.size + obstacle.radius:
                angle = random.uniform(0, 2 * math.pi)
                human.x = obstacle.x + math.cos(angle) * (human.size + obstacle.radius + 5)
                human.y = obstacle.y + math.sin(angle) * (human.size + obstacle.radius + 5)
        
        # Инициализируем частицы для каждого человека
        human.particles = ParticleSystem()
    
    # Инициализация переменных симуляции
    start_time = pygame.time.get_ticks()
    simulation_ended = False
    winner = None
    last_update_time = start_time

    # Показываем заставку
    show_intro_screen(screen)
    start_time = pygame.time.get_ticks()  # Сбрасываем время
    
    # Главный игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    ui.show_fps = not ui.show_fps
                elif event.key == pygame.K_d:
                    ui.show_debug = not ui.show_debug
                elif event.key == pygame.K_m:
                    ui.show_minimap = not ui.show_minimap
                elif event.key == pygame.K_h:
                    ui.show_hints = not ui.show_hints
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_r and simulation_ended:
                    # Перезапуск симуляции
                    IMAGE_CACHE.clear()
                    return main()
                    
        # Расчет времени между кадрами для стабильной физики
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_update_time) / 1000.0  # в секундах
        last_update_time = current_time
        
        # Обновление времени суток
        time_manager.update()
        
        # Обновление UI
        ui.update(time_manager, gorilla)

        # Отрисовка фона
        draw_background(screen, time_manager, environment)
        
        # Обновление и отрисовка эффектов окружения
        if not simulation_ended:
            environment.update()
        
        # Проверка окончания симуляции
        alive_humans = sum(1 for h in humans if h.health > 0)

        if not simulation_ended and (gorilla.health <= 0 or alive_humans == 0):
            simulation_ended = True
            end_time = pygame.time.get_ticks()
            simulation_duration = (end_time - start_time) / 1000

            winner = "Люди" if gorilla.health <= 0 else "Горилла"

            # Эффекты при завершении
            for _ in range(50):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT // 2)
                color = (200, 200, 255) if winner == "Люди" else (255, 200, 100)
                environment.particles.add(
                    x, y,
                    color,
                    random.uniform(3, 7),
                    random.uniform(1, 3),
                    100,
                    gravity=0.1,
                    type="spark"
                )

        # Игровая логика - обновляем только если симуляция не закончилась
        if not simulation_ended:
            # Очищаем пространственный хеш
            spatial_hash.clear()
            
            # Обновляем позиции людей в хеше
            for human in humans:
                if human.health > 0:
                    spatial_hash.insert(human)
                    
            # Определяем тип местности под гориллой для модификаторов скорости
            # Реализация определения типа местности будет добавлена позже
            gorilla.terrain_speed_mod = 1.0  # По умолчанию
            
            # Обновляем гориллу
            gorilla.move(humans, obstacles, spatial_hash)
            
            # Обновляем людей пакетами для оптимизации
            # При большом количестве людей обновляем только случайную выборку
            batch_size = 200
            if alive_humans > 500:
                batch = random.sample([h for h in humans if h.health > 0], batch_size)
                for human in batch:
                    human.move(gorilla, humans, obstacles, spatial_hash)
            else:
                # Если людей немного, обновляем всех
                for human in humans:
                    if human.health > 0:
                        human.move(gorilla, humans, obstacles, spatial_hash)

        # Отрисовка препятствий
        for obstacle in obstacles:
            obstacle.draw(screen, time_manager)

        # Отрисовка персонажей
        # Сначала рисуем дальних людей, потом ближних, потом гориллу (для правильного перекрытия)
        if not simulation_ended:
            humans_by_distance = []
            for human in humans:
                if human.health > 0:
                    dist = math.hypot(human.x - gorilla.x, human.y - gorilla.y)
                    humans_by_distance.append((human, dist))
            
            # Сортируем по расстоянию (дальние рисуются первыми)
            humans_by_distance.sort(key=lambda x: x[1], reverse=True)
            
            for human, _ in humans_by_distance:
                human.draw(screen, time_manager, gorilla)
        else:
            # В конце симуляции просто рисуем всех выживших
            for human in humans:
                if human.health > 0:
                    human.draw(screen, time_manager, gorilla)

        # Рисуем гориллу поверх людей
        gorilla.draw(screen)

        # Отрисовка интерфейса
        time_passed = (pygame.time.get_ticks() - start_time) / 1000
        ui.draw_hud(screen, gorilla, humans, time_passed, time_manager, environment)

        # Экран окончания симуляции
        if simulation_ended:
            ui.draw_end_screen(screen, winner, simulation_duration, alive_humans, gorilla.kills, time_manager)
            
        pygame.display.flip()

        # Адаптивный FPS в зависимости от количества объектов
        if alive_humans > 700:
            target_fps = 40
        elif alive_humans > 300:
            target_fps = 50
        else:
            target_fps = 60
            
        clock.tick(target_fps)

# Запуск игры
if __name__ == "__main__":
    main()
        elif self.state == "reposition":
            # Лучники перемещаются, чтобы занять удобную позицию для стрельбы
            optimal_dist = self.max_arrow_range * 0.7
            
            # Если слишком близко к горилле - отходим
            if dist < optimal_dist * 0.8:
                retreat_speed = self.speed * 1.3  # Быстрее отходим
                
                # Проверяем препятствия при отступлении
                retreat_dx = -dx / dist
                retreat_dy = -dy / dist
                
                # Проверяем, нет ли препятствий на пути отступления
                if obstacles:
                    for obstacle in obstacles:
                        if not obstacle.passable:
                            obstacle_dx = obstacle.x - self.x
                            obstacle_dy = obstacle.y - self.y
                            obstacle_dist = math.hypot(obstacle_dx, obstacle_dy)
                            
                            # Если препятствие близко и по пути отступления
                            if obstacle_dist < 50:
                                # Вычисляем угол между направлением отступления и препятствием
                                retreat_angle = math.atan2(retreat_dy, retreat_dx)
                                obstacle_angle = math.atan2(obstacle_dy, obstacle_dx)
                                angle_diff = abs((retreat_angle - obstacle_angle + math.pi) % (2*math.pi) - math.pi)
                                
                                if angle_diff < math.pi/4:  # Если препятствие примерно по пути отступления
                                    # Выбираем новое направление отступления
                                    new_angle = obstacle_angle + math.pi/2 if random.random() < 0.5 else obstacle_angle - math.pi/2
                                    retreat_dx = math.cos(new_angle)
                                    retreat_dy = math.sin(new_angle)
                
                # Применяем скорость с учетом типа местности
                self.x += retreat_dx * retreat_speed * self.terrain_speed_mod
                self.y += retreat_dy * retreat_speed * self.terrain_speed_mod
                
                # Лицом к горилле для готовности к стрельбе
                self.facing_angle = math.atan2(dy, dx)
            
            # Если хорошая дистанция - готовимся к стрельбе
            elif abs(dist - optimal_dist) < 20:
                if self.arrow_cooldown <= 20:
                    self.state = "ranged_attack"
            
            # Если слишком далеко - приближаемся
            else:
                approach_speed = self.speed * 0.7  # Медленнее подходим
                approach_dx = dx / dist
                approach_dy = dy / dist
                
                # Применяем скорость
                self.x += approach_dx * approach_speed * self.terrain_speed_mod
                self.y += approach_dy * approach_speed * self.terrain_speed_mod
                
                # Лицом к горилле
                self.facing_angle = math.atan2(dy, dx)
                
        elif self.state == "flee":
            # Бегство от гориллы
            if dist > 0:
                # Базовая скорость бегства
                flee_speed = self.speed * 1.2
                
                # Учитываем стамину при беге
                if not self.exhausted:
                    # Бег затрачивает стамину
                    self.stamina -= 0.2
                    if self.stamina <= 0:
                        self.exhausted = True
                        self.stamina = 0
                        flee_speed *= 0.6  # Медленнее бегаем при истощении
                else:
                    flee_speed *= 0.6
                
                # Направление бегства - от гориллы
                flee_dx = -dx / dist
                flee_dy = -dy / dist
                
                # Проверяем препятствия на пути
                if obstacles:
                    for obstacle in obstacles:
                        if not obstacle.passable:
                            obstacle_dx = obstacle.x - self.x
                            obstacle_dy = obstacle.y - self.y
                            obstacle_dist = math.hypot(obstacle_dx, obstacle_dy)
                            
                            if obstacle_dist < self.size + obstacle.radius + 20:
                                # Вычисляем угол между направлением бегства и препятствием
                                flee_angle = math.atan2(flee_dy, flee_dx)
                                obstacle_angle = math.atan2(obstacle_dy, obstacle_dx)
                                angle_diff = abs((flee_angle - obstacle_angle + math.pi) % (2*math.pi) - math.pi)
                                
                                # Если препятствие на пути бегства
                                if angle_diff < math.pi/3:
                                    # Изменяем направление
                                    avoidance_angle = obstacle_angle + math.pi/2 if random.random() < 0.5 else obstacle_angle - math.pi/2
                                    avoidance_strength = max(0, 1 - obstacle_dist / (self.size + obstacle.radius + 20))
                                    
                                    # Смешиваем направление бегства с направлением обхода препятствия
                                    flee_dx = flee_dx * (1 - avoidance_strength) + math.cos(avoidance_angle) * avoidance_strength
                                    flee_dy = flee_dy * (1 - avoidance_strength) + math.sin(avoidance_angle) * avoidance_strength
                                    
                                    # Нормализуем вектор
                                    flee_length = math.hypot(flee_dx, flee_dy)
                                    if flee_length > 0:
                                        flee_dx /= flee_length
                                        flee_dy /= flee_length
                
                # Учитываем скорость по типу местности
                self.x += flee_dx * flee_speed * self.terrain_speed_mod
                self.y += flee_dy * flee_speed * self.terrain_speed_mod
                
                # При бегстве смотрим в сторону движения
                self.facing_angle = math.atan2(flee_dy, flee_dx)
                
                # Паника - возможность споткнуться при бегстве
                if self.feared > 0 and random.random() < 0.005:
                    self.stunned = random.randint(10, 20)
                    if self.particles:
                        for _ in range(3):
                            self.particles.add(
                                self.x + random.uniform(-5, 5),
                                self.y + random.uniform(-5, 5),
                                (150, 150, 150),
                                random.uniform(1, 3),
                                random.uniform(0.5, 1.5),
                                15
                            )
                
                # Шанс перейти к группировке с другими людьми для безопасности
                if self.state_timer < 30 and random.random() < 0.1:
                    self.state = "group"
                    self.state_timer = random.randint(80, 150)
                    
        elif self.state == "idle":
            # Случайное передвижение на месте
            self.facing_angle += random.uniform(-0.05, 0.05)
            idle_speed = self.speed * 0.5
            
            # Медленно восстанавливаем мораль в безопасном состоянии
            self.morale = min(100, self.morale + 0.05)
            
            # Двигаемся в направлении взгляда
            self.x += math.cos(self.facing_angle) * idle_speed * self.terrain_speed_mod
            self.y += math.sin(self.facing_angle) * idle_speed * self.terrain_speed_mod
            
            # Случайная смена направления
            if random.random() < 0.01:
                self.facing_angle = random.uniform(0, 2 * math.pi)
                
            # Проверка столкновений с препятствиями
            if obstacles:
                for obstacle in obstacles:
                    if not obstacle.passable:
                        obstacle_dist = math.hypot(obstacle.x - self.x, obstacle.y - self.y)
                        if obstacle_dist < self.size + obstacle.radius:
                            # Отходим от препятствия
                            angle = math.atan2(self.y - obstacle.y, self.x - obstacle.x)
                            self.x += math.cos(angle) * 2
                            self.y += math.sin(angle) * 2
                            
                            # Меняем направление
                            self.facing_angle = angle
            
            # Замечаем гориллу и реагируем при приближении
            if dist < 150:
                react_chance = 0.1
                if gorilla.rage_mode:
                    react_chance = 0.3
                    
                if random.random() < react_chance:
                    if self.type == "archer" or self.morale < 50:
                        self.state = "flee"
                    else:
                        self.state = "chase"
                    self.state_timer = random.randint(60, 120)
                    
        elif self.state == "chase":
            # Преследование гориллы/поддержание оптимальной дистанции
            optimal_dist = 120
            
            # Воины стремятся подойти ближе
            if self.type == "warrior":
                optimal_dist = 60
            
            # Лучники предпочитают держаться на расстоянии
            elif self.type == "archer":
                optimal_dist = self.max_arrow_range * 0.7
            
            # Если слишком далеко - приближаемся
            if dist > optimal_dist * 1.2:
                chase_speed = self.speed * 0.9
                
                # Используем стамину при погоне
                if not self.exhausted:
                    self.stamina -= 0.1
                    if self.stamina <= 0:
                        self.exhausted = True
                        self.stamina = 0
                        chase_speed *= 0.7
                else:
                    chase_speed *= 0.7
                
                # Направление движения к горилле
                approach_dx = dx / dist
                approach_dy = dy / dist
                
                # Проверка препятствий
                if obstacles:
                    for obstacle in obstacles:
                        if not obstacle.passable:
                            obstacle_dx = obstacle.x - self.x
                            obstacle_dy = obstacle.y - self.y
                            obstacle_dist = math.hypot(obstacle_dx, obstacle_dy)
                            
                            if obstacle_dist < self.size + obstacle.radius + 20:
                                # Уклоняемся от препятствия
                                avoidance_strength = max(0, 1 - obstacle_dist / (self.size + obstacle.radius + 20))
                                dodge_angle = math.atan2(obstacle_dy, obstacle_dx)
                                dodge_angle += math.pi/2 if random.random() < 0.5 else -math.pi/2
                                
                                approach_dx = approach_dx * (1 - avoidance_strength) + math.cos(dodge_angle) * avoidance_strength
                                approach_dy = approach_dy * (1 - avoidance_strength) + math.sin(dodge_angle) * avoidance_strength
                                
                                approach_length = math.hypot(approach_dx, approach_dy)
                                if approach_length > 0:
                                    approach_dx /= approach_length
                                    approach_dy /= approach_length
                
                # Применяем движение
                self.x += approach_dx * chase_speed * self.terrain_speed_mod
                self.y += approach_dy * chase_speed * self.terrain_speed_mod
                
                # Лицом к горилле
                self.facing_angle = math.atan2(dy, dx)
                
            # Если слишком близко - отходим
            elif dist < optimal_dist * 0.8:
                retreat_speed = self.speed * 0.7
                
                # Направление от гориллы
                retreat_dx = -dx / dist
                retreat_dy = -dy / dist
                
                # Проверка препятствий (аналогично приближению)
                if obstacles:
                    for obstacle in obstacles:
                        if not obstacle.passable:
                            obstacle_dx = obstacle.x - self.x
                            obstacle_dy = obstacle.y - self.y
                            obstacle_dist = math.hypot(obstacle_dx, obstacle_dy)
                            
                            if obstacle_dist < self.size + obstacle.radius + 20:
                                avoidance_strength = max(0, 1 - obstacle_dist / (self.size + obstacle.radius + 20))
                                dodge_angle = math.atan2(obstacle_dy, obstacle_dx)
                                dodge_angle += math.pi/2 if random.random() < 0.5 else -math.pi/2
                                
                                retreat_dx = retreat_dx * (1 - avoidance_strength) + math.cos(dodge_angle) * avoidance_strength
                                retreat_dy = retreat_dy * (1 - avoidance_strength) + math.sin(dodge_angle) * avoidance_strength
                                
                                retreat_length = math.hypot(retreat_dx, retreat_dy)
                                if retreat_length > 0:
                                    retreat_dx /= retreat_length
                                    retreat_dy /= retreat_length
                
                # Движение
                self.x += retreat_dx * retreat_speed * self.terrain_speed_mod
                self.y += retreat_dy * retreat_speed * self.terrain_speed_mod
                
                # Смотрим на гориллу (отходим лицом к ней)
                self.facing_angle = math.atan2(dy, dx)
                
            else:
                # На оптимальной дистанции просто поворачиваемся к горилле
                self.facing_angle = math.atan2(dy, dx)
                
                # Если мы лучник на оптимальной дистанции - стреляем
                if self.type == "archer" and self.arrow_cooldown <= 0:
                    self.state = "ranged_attack"
                
                # Если мы воин или обычный человек, и горилла ослаблена - атакуем
                elif (self.type == "warrior" or random.random() < 0.2) and gorilla.health < gorilla.max_health * 0.3:
                    self.state = "attack"
                    self.state_timer = random.randint(30, 60)
        
        elif self.state == "group":
            # Группировка с другими людьми для безопасности
            nearby_count = 0
            group_center_x = 0
            group_center_y = 0
            
            # Ищем ближайших людей
            if spatial_hash:
                nearby_humans = spatial_hash.get_nearby(self.x, self.y, 1)
            else:
                nearby_humans = []
                sample_size = min(30, len(humans))
                for human in random.sample(humans, sample_size):
                    if human != self and human.health > 0:
                        human_dist = math.hypot(self.x - human.x, self.y - human.y)
                        if human_dist < 100:
                            nearby_humans.append(human)
            
            # Вычисляем центр группы
            for human in nearby_humans:
                if human != self and human.health > 0:
                    human_dist = math.hypot(self.x - human.x, self.y - human.y)
                    if human_dist < 100:
                        nearby_count += 1
                        group_center_x += human.x
                        group_center_y += human.y
            
            if nearby_count >= 2:
                # Движемся к центру группы
                group_center_x /= nearby_count
                group_center_y /= nearby_count
                
                group_dx = group_center_x - self.x
                group_dy = group_center_y - self.y
                group_dist = math.hypot(group_dx, group_dy)
                
                if group_dist > 30:  # Не подходим слишком близко к центру
                    group_dx /= group_dist
                    group_dy /= group_dist
                    
                    # Проверка препятствий
                    if obstacles:
                        for obstacle in obstacles:
                            if not obstacle.passable:
                                obstacle_dist = math.hypot(obstacle.x - self.x, obstacle.y - self.y)
                                if obstacle_dist < self.size + obstacle.radius + 15:
                                    # Обходим препятствие
                                    dodge_angle = math.atan2(self.y - obstacle.y, self.x - obstacle.x)
                                    avoidance_strength = max(0, 1 - obstacle_dist / (self.size + obstacle.radius + 15))
                                    
                                    group_dx = group_dx * (1 - avoidance_strength) + math.cos(dodge_angle) * avoidance_strength
                                    group_dy = group_dy * (1 - avoidance_strength) + math.sin(dodge_angle) * avoidance_strength
                                    
                                    group_length = math.hypot(group_dx, group_dy)
                                    if group_length > 0:
                                        group_dx /= group_length
                                        group_dy /= group_length
                    
                    # Двигаемся к группе
                    self.x += group_dx * self.speed * 0.8 * self.terrain_speed_mod
                    self.y += group_dy * self.speed * 0.8 * self.terrain_speed_mod
                    
                    # Смотрим в направлении движения
                    self.facing_angle = math.atan2(group_dy, group_dx)
                    
                # Восстанавливаем мораль в группе
                self.morale = min(100, self.morale + 0.1)
                
                # Поддерживаем группу, если видим гориллу
                if dist < 200 and random.random() < 0.01:
                    self.state_timer = random.randint(60, 120)
                    
                # Шанс перейти к координированной атаке
                if nearby_count >= 5 and dist < 150 and random.random() < 0.005:
                    # Если в группе есть воины, выше шанс атаки
                    warriors_in_group = sum(1 for h in nearby_humans if h.type == "warrior" and h.health > 0)
                    if warriors_in_group > 0 or random.random() < 0.3:
                        for human in nearby_humans:
                            if human.health > 0 and random.random() < 0.7:
                                human.state = "chase"
                                human.state_timer = random.randint(60, 120)
                                human.morale += 10  # Повышаем мораль для координированной атаки
            else:
                # Если не нашли группу, ищем людей или просто убегаем
                self.state = "idle"
                self.state_timer = random.randint(30, 60)
        
        # Обработка кулдаунов
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if hasattr(self, 'arrow_cooldown') and self.arrow_cooldown > 0:
            self.arrow_cooldown -= 1
            
        # Стратегическое мышление - периодический пересмотр тактики
        self.strategy_cooldown -= 1
        if self.strategy_cooldown <= 0:
            # Сложная логика принятия решений на основе общей ситуации
            self.strategy_cooldown = random.randint(100, 200)
            
            # Повышаем эффективность с опытом
            if self.level >= 3 and random.random() < 0.3:
                # Продвинутая тактика для опытных людей
                gorilla_health_percent = gorilla.health / gorilla.max_health
                
                if gorilla_health_percent < 0.3:
                    # Горилла слаба - повышаем шанс атаки
                    if random.random() < 0.6:
                        self.state = "chase"
                        self.state_timer = random.randint(60, 120)
                elif gorilla.rage_mode:
                    # Горилла в ярости - ищем безопасность в группе
                    if random.random() < 0.7:
                        self.state = "group" if random.random() < 0.6 else "flee"
                        self.state_timer = random.randint(80, 150)
        
        # Применяем ограничения по границам экрана
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))
        
        # Проверка столкновений с другими людьми для предотвращения скопления
        if spatial_hash:
            nearby_humans = spatial_hash.get_nearby(self.x, self.y, 1)
            for human in nearby_humans:
                if human != self and human.health > 0:
                    dist = math.hypot(self.x - human.x, self.y - human.y)
                    min_dist = self.size + human.size
                    if dist < min_dist:
                        # Отталкиваем друг от друга
                        push_strength = 0.5
                        push_dx = (self.x - human.x) / dist
                        push_dy = (self.y - human.y) / dist
                        self.x += push_dx * push_strength
                        self.y += push_dy * push_strength

# --- Оптимизированный игровой интерфейс ---
class GameUI:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 20)
        self.title_font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 16)
        self.tiny_font = pygame.font.SysFont('Arial', 12)
        self.show_fps = True
        self.show_debug = False
        self.show_hints = True
        self.show_minimap = True
        self.screen_shake = 0
        self.day_night_indicator_pos = (WIDTH - 100, 15)  # Позиция индикатора дня/ночи
        
        # Иконки
        self.human_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.human_icon, (0, 150, 255), (10, 10), 7)
        
        self.warrior_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.warrior_icon, (200, 50, 50), (10, 10), 7)
        
        self.archer_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.archer_icon, (50, 200, 50), (10, 10), 7)

        self.gorilla_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.gorilla_icon, (139, 69, 19), (10, 10), 9)
        
        # Уведомления
        self.notifications = []
        self.last_day = 1
        
        # Миникарта
        self.minimap_size = 150
        self.minimap_pos = (WIDTH - self.minimap_size - 10, HEIGHT - self.minimap_size - 10)
        self.minimap_scale = self.minimap_size / max(WIDTH, HEIGHT)
        
        # Состояние интерфейса
        self.show_ability_tooltips = False
        
    def add_notification(self, text, color=(255, 255, 255), duration=180):
        self.notifications.append({
            'text': text,
            'color': color,
            'duration': duration,
            'alpha': 255
        })
        
    def update(self, time_manager, gorilla):
        # Проверяем начало нового дня
        if time_manager.day_count > self.last_day:
            self.add_notification(f"День {time_manager.day_count}", (255, 220, 100), 240)
            self.last_day = time_manager.day_count
            
        # Обновляем уведомления
        i = 0
        while i < len(self.notifications):
            self.notifications[i]['duration'] -= 1
            
            # Затухание в конце
            if self.notifications[i]['duration'] < 60:
                self.notifications[i]['alpha'] = int(255 * self.notifications[i]['duration'] / 60)
                
            if self.notifications[i]['duration'] <= 0:
                self.notifications.pop(i)
            else:
                i += 1
                
        # Добавляем уведомления при особых событиях
        if gorilla.rage_mode and gorilla.rage_timer == 299:  # Только что активировался режим ярости
            self.add_notification("РЕЖИМ ЯРОСТИ АКТИВИРОВАН!", (255, 50, 0), 180)
            self.screen_shake = 30
            
        # Сообразно уровням гориллы
        if gorilla.level > 1 and gorilla.experience == 0:  # Только что повысился уровень
            self.add_notification(f"Горилла достигла уровня {gorilla.level}!", (255, 215, 0), 240)
            self.screen_shake = 20
            
            # Добавляем информацию о новых способностях
            for ability_name, ability in gorilla.abilities.items():
                if ability["level"] == gorilla.level:
                    ability_names = {
                        "pound": "Удар кулаком",
                        "throw": "Захват и бросок",
                        "roar": "Мощный рев",
                        "leap": "Прыжок"
                    }
                    self.add_notification(f"Разблокирована способность: {ability_names.get(ability_name, ability_name)}!", 
                                        (200, 255, 150), 300)
                    
        # Обновляем эффект тряски экрана
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def draw_hud(self, screen, gorilla, humans, time_passed, time_manager, environment):
        # Применяем эффект тряски экрана (если активен)
        shake_offset_x = 0
        shake_offset_y = 0
        if self.screen_shake > 0:
            shake_strength = min(10, self.screen_shake // 3)
            shake_offset_x = random.randint(-shake_strength, shake_strength)
            shake_offset_y = random.randint(-shake_strength, shake_strength)
        
        # Считаем живых людей по типам
        alive_civilians = sum(1 for h in humans if h.health > 0 and h.type == "civilian")
        alive_warriors = sum(1 for h in humans if h.health > 0 and h.type == "warrior")
        alive_archers = sum(1 for h in humans if h.health > 0 and h.type == "archer")
        alive_humans = alive_civilians + alive_warriors + alive_archers
        
        # Фон для HUD
        hud_bg = pygame.Surface((340, 130), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 150))
        screen.blit(hud_bg, (5 + shake_offset_x, 5 + shake_offset_y))
        pygame.draw.rect(screen, (200, 200, 200, 50), (5 + shake_offset_x, 5 + shake_offset_y, 340, 130), 1, border_radius=10)
        
        # Информация о людях
        screen.blit(self.human_icon, (15 + shake_offset_x, 15 + shake_offset_y))
        humans_text = self.font.render(f"Люди: {alive_humans}/{len(humans)}", True, WHITE)
        screen.blit(humans_text, (40 + shake_offset_x, 15 + shake_offset_y))
        
        # Детальная статистика по типам людей
        details_x = 40 + shake_offset_x
        details_y = 40 + shake_offset_y
        civilian_text = self.small_font.render(f"Гражданские: {alive_civilians}", True, (150, 150, 255))
        screen.blit(civilian_text, (details_x, details_y))
        
        warrior_text = self.small_font.render(f"Воины: {alive_warriors}", True, (255, 100, 100))
        screen.blit(warrior_text, (details_x, details_y + 20))
        
        archer_text = self.small_font.render(f"Лучники: {alive_archers}", True, (100, 255, 100))
        screen.blit(archer_text, (details_x, details_y + 40))
        
        # Информация о горилле
        screen.blit(self.gorilla_icon, (15 + shake_offset_x, 85 + shake_offset_y))
        gorilla_text = self.font.render(f"Горилла HP: {max(0, int(gorilla.health))}/{gorilla.max_health}", True, WHITE)
        screen.blit(gorilla_text, (40 + shake_offset_x, 85 + shake_offset_y))
        
        # Уровень и убийства гориллы
        level_text = self.small_font.render(f"Уровень: {gorilla.level}", True, (255, 215, 0))
        screen.blit(level_text, (40 + shake_offset_x, 110 + shake_offset_y))
        
        kills_text = self.small_font        self.attack_damage = type_info['damage']
        self.attack_cooldown = 0
        self.flash_effect = 0
        self.state = "idle"
        self.state_timer = 0
        self.stunned = 0  # Таймер оглушения
        self.feared = 0   # Таймер страха
        self.facing_angle = random.uniform(0, 2*math.pi)
        self.color_variation = random.randint(0, 10) / 10
        self.size_variation = random.uniform(0.8, 1.2)
        self.particles = None
        self.push_velocity_x = 0
        self.push_velocity_y = 0
        self.push_damping = 0.9
        self.terrain_speed_mod = 1.0
        
        # Параметры для брошенного человека
        self.thrown = False
        self.thrown_dx = 0
        self.thrown_dy = 0
        self.thrown_timer = 0
        
        # Для групповой тактики
        self.group = None
        self.group_role = None  # "leader", "follower", "flanker"
        self.target_position = None
        
        # Параметры выносливости и истощения
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen_rate = 0.05
        self.exhausted = False
        
        # Параметры опыта для людей (со временем становятся более эффективными)
        self.experience = 0
        self.level = 1
        
        # Эмоциональное состояние
        self.morale = 100  # От 0 до 100
        
        # Стратегическое мышление (со временем люди становятся умнее)
        self.strategy_cooldown = random.randint(100, 200)
        
        # Дополнительные параметры для лучников
        if self.type == "archer":
            self.arrow_cooldown = 0
            self.max_arrow_range = 200
        
        # Выбираем соответствующее изображение
        if self.type == "civilian":
            self.img = human_civilian_img
        elif self.type == "warrior":
            self.img = human_warrior_img
        else:  # archer
            self.img = human_archer_img

    def set_stunned(self, duration):
        self.stunned = max(self.stunned, duration)
        # Визуальный эффект оглушения
        for _ in range(5):
            self.particles.add(
                self.x, self.y - 10,
                (255, 255, 255),
                random.uniform(1, 3),
                random.uniform(0.5, 1.5),
                20,
                gravity=-0.05
            )

    def set_feared(self, duration):
        self.feared = max(self.feared, duration)
        self.morale = max(0, self.morale - 30)  # Снижаем мораль при страхе
        
    def set_thrown(self, dx, dy):
        self.thrown = True
        self.thrown_dx = dx
        self.thrown_dy = dy
        self.thrown_timer = 60  # Время полета
        
    def draw(self, screen, time_manager, gorilla):
        if self.health <= 0:
            return
            
        dist_to_gorilla = math.hypot(self.x - gorilla.x, self.y - gorilla.y)
        
        # Выбираем уровень детализации в зависимости от расстояния
        if dist_to_gorilla < DETAIL_LEVELS['full']:
            # Полная детализация (близко к горилле)
            
            # Факел ночью у некоторых людей
            if time_manager.is_night() and random.random() < 0.005:
                fire_x = self.x + math.cos(self.facing_angle + math.pi/4) * 15
                fire_y = self.y + math.sin(self.facing_angle + math.pi/4) * 15
                
                # Анимированный огонь
                fire_radius = random.uniform(3, 5)
                fire_surf = pygame.Surface((int(fire_radius*2), int(fire_radius*2)), pygame.SRCALPHA)
                
                for i in range(3):
                    flame_color = (255, 100 + random.randint(0, 100), random.randint(0, 50), 180 - i * 40)
                    shrink = i * 0.2
                    pygame.draw.circle(fire_surf, flame_color,
                                     (int(fire_radius), int(fire_radius)), 
                                     int(fire_radius * (1 - shrink)))
                    
                screen.blit(fire_surf, (int(fire_x - fire_radius), int(fire_y - fire_radius)))
                
                # Свет от факела (подсветка вокруг)
                glow_radius = 30 + math.sin(pygame.time.get_ticks() / 100) * a
                glow_surf = pygame.Surface((int(glow_radius*2), int(glow_radius*2)), pygame.SRCALPHA)
                for i in range(3):
                    glow_alpha = 60 - i * 20
                    pygame.draw.circle(glow_surf, (255, 200, 100, glow_alpha),
                                     (int(glow_radius), int(glow_radius)), 
                                     int(glow_radius * (1 - i * 0.2)))
                    
                screen.blit(glow_surf, (int(fire_x - glow_radius), int(fire_y - glow_radius)))
            
            # Тень человека
            shadow = pygame.Surface((self.size*2, self.size), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 80), (0, 0, self.size*2, self.size))
            screen.blit(shadow, (int(self.x - self.size), int(self.y + self.size * 0.8 + 2)))
            
            # Основное изображение
            img = self.img.copy()
            scaled_size = int(24 * self.size_variation)
            img = pygame.transform.scale(img, (scaled_size, scaled_size))
            
            # Вращаем изображение в зависимости от направления
            rotated_img = pygame.transform.rotate(img, -self.facing_angle * 180 / math.pi)
            
            # Визуальные эффекты для различных состояний
            if self.flash_effect > 0:
                flash_overlay = pygame.Surface(rotated_img.get_size(), pygame.SRCALPHA)
                flash_overlay.fill((255, 255, 255, self.flash_effect * 15))
                rotated_img.blit(flash_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                self.flash_effect -= 1
                
            if self.stunned > 0:
                # Звездочки над головой или другой эффект оглушения
                star_offset = math.sin(pygame.time.get_ticks() / 100) * 2
                star_size = 8
                star_pos = (int(self.x), int(self.y - scaled_size//2 - 10 + star_offset))
                
                # Рисуем звездочки (эффект оглушения)
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (star_pos[0] - 5, star_pos[1]), star_size//2)
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (star_pos[0] + 5, star_pos[1]), star_size//2)
                
            if self.feared > 0:
                # Визуальное представление страха (например, !!! над головой)
                fear_y_offset = math.sin(pygame.time.get_ticks() / 150) * 3
                fear_font = pygame.font.SysFont('Arial', 12)
                fear_text = fear_font.render("!", True, (255, 50, 50))
                screen.blit(fear_text, (int(self.x - 2), int(self.y - scaled_size//2 - 15 + fear_y_offset)))
                
            # Если человек брошен гориллой
            if self.thrown:
                # Эффект вращения
                rotated_img = pygame.transform.rotate(rotated_img, 
                                                    (pygame.time.get_ticks() % 360) * 0.5)
                
                # Эффект движения (размытие)
                motion_blur = pygame.Surface(rotated_img.get_size(), pygame.SRCALPHA)
                blur_alpha = min(150, self.thrown_timer * 3)
                motion_blur.fill((255, 255, 255, blur_alpha))
                rotated_img.blit(motion_blur, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Рисуем человека
            img_rect = rotated_img.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_img, img_rect.topleft)
            
            # Полоска здоровья
            health_width = int((self.health / self.max_health) * self.size * 2)
            health_bg = pygame.Rect(int(self.x - self.size), int(self.y - self.size - 8), self.size * 2, 3)
            health_bar = pygame.Rect(int(self.x - self.size), int(self.y - self.size - 8), health_width, 3)
            
            pygame.draw.rect(screen, (50, 50, 50), health_bg)
            if self.health > 70:
                health_color = GREEN
            elif self.health > 30:
                health_color = (255, 165, 0)
            else:
                health_color = RED
            pygame.draw.rect(screen, health_color, health_bar)
            
            # Визуальные индикаторы для разных типов людей
            if self.type == "warrior":
                # Мини-иконка меча для воина
                pygame.draw.rect(screen, (200, 200, 200), 
                               (int(self.x - self.size + 2), int(self.y - self.size - 12), 4, 2))
            elif self.type == "archer":
                # Мини-иконка лука для лучника
                pygame.draw.arc(screen, (139, 69, 19), 
                              (int(self.x + self.size - 6), int(self.y - self.size - 14), 4, 6),
                              -math.pi/2, math.pi/2, 1)
            
            # Если лучник стреляет, показываем стрелу
            if self.type == "archer" and self.arrow_cooldown > 0 and self.arrow_cooldown < 10:
                arrow_length = 15
                arrow_angle = math.atan2(gorilla.y - self.y, gorilla.x - self.x)
                arrow_end_x = self.x + math.cos(arrow_angle) * arrow_length
                arrow_end_y = self.y + math.sin(arrow_angle) * arrow_length
                
                # Рисуем стрелу
                pygame.draw.line(screen, (139, 69, 19), 
                               (int(self.x), int(self.y)),
                               (int(arrow_end_x), int(arrow_end_y)), 2)
                # Наконечник стрелы
                pygame.draw.circle(screen, (50, 50, 50), 
                                 (int(arrow_end_x), int(arrow_end_y)), 3)
            
        elif dist_to_gorilla < DETAIL_LEVELS['medium']:
            # Средняя детализация
            img = self.img.copy()
            scaled_size = int(20 * self.size_variation)
            img = pygame.transform.scale(img, (scaled_size, scaled_size))
            
            if self.flash_effect > 0:
                flash_overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                flash_overlay.fill((255, 255, 255, self.flash_effect * 15))
                img.blit(flash_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                self.flash_effect -= 1
                
            img_rect = img.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(img, img_rect.topleft)
            
            # Упрощенная полоска здоровья
            if self.health < self.max_health:
                health_width = int((self.health / self.max_health) * self.size * 2)
                health_bg = pygame.Rect(int(self.x - self.size), int(self.y - self.size - 5), self.size * 2, 2)
                health_bar = pygame.Rect(int(self.x - self.size), int(self.y - self.size - 5), health_width, 2)
                
                pygame.draw.rect(screen, (50, 50, 50), health_bg)
                if self.health > 70:
                    health_color = GREEN
                elif self.health > 30:
                    health_color = (255, 165, 0)
                else:
                    health_color = RED
                pygame.draw.rect(screen, health_color, health_bar)
            
        elif dist_to_gorilla < DETAIL_LEVELS['low']:
            # Низкая детализация
            if self.type == "warrior":
                color = (200, 100, 100)
            elif self.type == "archer":
                color = (100, 200, 100)
            else:  # civilian
                color = (100, 150, 200)
                
            # Применяем эффекты состояния
            if self.flash_effect > 0:
                color = (255, 255, 255)
                self.flash_effect -= 1
                
            if self.feared > 0:
                # Периодически меняем цвет при страхе
                if pygame.time.get_ticks() % 300 < 150:
                    color = (min(color[0] + 50, 255), 
                           max(color[1] - 50, 0), 
                           max(color[2] - 50, 0))
            
            # Рисуем упрощенную версию
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)),
                             int(10 * self.size_variation))
            
        else:
            # Минимальная детализация (очень далеко)
            base_color = HUMAN_TYPES[self.type]['color']
            alpha = 150 + math.sin(pygame.time.get_ticks() / 1000 + self.x * 0.01) * 50
            
            # Группируем близко стоящих людей для оптимизации
            pygame.draw.circle(screen, (*base_color, int(alpha)), 
                             (int(self.x), int(self.y)),
                             int(8 * self.size_variation))

    def push_back(self, from_x, from_y, force):
        dx = self.x - from_x
        dy = self.y - from_y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.push_velocity_x = dx * force
            self.push_velocity_y = dy * force

    def take_damage(self, amount):
        old_health = self.health
        self.health -= amount
        
        if old_health > self.health and self.health > 0:
            self.flash_effect = 8
            
            # При получении урона есть шанс запаниковать
            fear_chance = 0.3 * (1 - self.health / self.max_health)
            if random.random() < fear_chance:
                self.set_feared(random.randint(30, 90))
                
            # Снижаем мораль при получении урона
            self.morale -= amount * 0.5
            
            # Шанс перехода в состояние бегства при низком здоровье или низком морале
            if (self.health / self.max_health < 0.3 or self.morale < 30) and random.random() < 0.5:
                self.state = "flee"
                self.state_timer = random.randint(60, 120)

    def move(self, gorilla, humans, obstacles=None, spatial_hash=None):
        if self.health <= 0:
            return
            
        # Обработка эффектов оглушения и страха
        if self.stunned > 0:
            self.stunned -= 1
            # Когда оглушен, может только слегка покачиваться на месте
            if random.random() < 0.1:
                self.x += random.uniform(-1, 1)
                self.y += random.uniform(-1, 1)
            return
            
        # Обрабатываем импульс от толчков
        if abs(self.push_velocity_x) > 0.1 or abs(self.push_velocity_y) > 0.1:
            old_x, old_y = self.x, self.y
            self.x += self.push_velocity_x
            self.y += self.push_velocity_y
            
            # Проверка столкновений с препятствиями
            if obstacles:
                for obstacle in obstacles:
                    if not obstacle.passable:
                        dist = math.hypot(self.x - obstacle.x, self.y - obstacle.y)
                        if dist < self.size + obstacle.radius:
                            # Отскакиваем от препятствия
                            self.x, self.y = old_x, old_y
                            
                            # Меняем направление импульса
                            bounce_factor = 0.5  # Коэффициент упругости
                            obstacle_angle = math.atan2(self.y - obstacle.y, self.x - obstacle.x)
                            self.push_velocity_x = math.cos(obstacle_angle) * self.push_velocity_x * bounce_factor
                            self.push_velocity_y = math.sin(obstacle_angle) * self.push_velocity_y * bounce_factor
                            
                            # Небольшой урон при столкновении с препятствием на высокой скорости
                            impact_speed = math.hypot(self.push_velocity_x, self.push_velocity_y)
                            if impact_speed > 5:
                                self.health -= impact_speed * 0.5
                                
                                # Эффект удара
                                if self.particles:
                                    for _ in range(3):
                                        self.particles.add(
                                            self.x + random.uniform(-5, 5),
                                            self.y + random.uniform(-5, 5),
                                            (150, 150, 150),
                                            random.uniform(1, 3),
                                            random.uniform(0.5, 1.5),
                                            15
                                        )
                                        
                                if self.health <= 0:
                                    return
            
            self.push_velocity_x *= self.push_damping
            self.push_velocity_y *= self.push_damping
            
        # Обработка состояния брошенного человека
        if self.thrown:
            self.thrown_timer -= 1
            
            if self.thrown_timer <= 0:
                self.thrown = False
            else:
                # Проверяем столкновения с другими людьми в полете
                if spatial_hash:
                    nearby_humans = spatial_hash.get_nearby(self.x, self.y, 1)
                    for human in nearby_humans:
                        if human != self and human.health > 0:
                            dist = math.hypot(self.x - human.x, self.y - human.y)
                            if dist < self.size + human.size:
                                # Наносим урон человеку, в которого врезались
                                collision_damage = 30 * (self.thrown_timer / 60)  # Больше урона в начале полета
                                human.health -= collision_damage
                                human.take_damage(collision_damage)
                                
                                # Отталкиваем человека, в которого врезались
                                human.push_back(self.x - self.thrown_dx * 10, 
                                              self.y - self.thrown_dy * 10, 
                                              5 * (self.thrown_timer / 60))
                                
                                # Эффект столкновения
                                if self.particles:
                                    for _ in range(5):
                                        self.particles.add(
                                            (self.x + human.x) / 2 + random.uniform(-5, 5),
                                            (self.y + human.y) / 2 + random.uniform(-5, 5),
                                            (255, 200, 200),
                                            random.uniform(2, 4),
                                            random.uniform(1, 3),
                                            25,
                                            type="spark"
                                        )
            return  # Брошенный человек не выполняет других действий
            
        # Регенерация стамины
        if not self.exhausted:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen_rate)
        else:
            # Восстанавливаемся из состояния истощения
            if self.stamina > self.max_stamina * 0.3:
                self.exhausted = False
            else:
                self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen_rate * 0.5)
                
        # Обновление таймера состояния
        if self.state_timer > 0:
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Выбираем новое состояние на основе морали и типа
                rand = random.random()
                
                if self.morale < 30:  # Низкая мораль - высокий шанс бегства
                    if rand < 0.6:
                        self.state = "flee"
                    elif rand < 0.8:
                        self.state = "idle"
                    else:
                        self.state = "chase"
                elif self.morale < 70:  # Средняя мораль
                    if rand < 0.4:
                        self.state = "chase"
                    elif rand < 0.7:
                        self.state = "idle"
                    else:
                        self.state = "flee"
                else:  # Высокая мораль - высокий шанс атаки
                    if rand < 0.6:
                        self.state = "chase"
                    elif rand < 0.9:
                        self.state = "idle"
                    else:
                        self.state = "flee"
                        
                # Длительность нового состояния
                self.state_timer = random.randint(60, 180)
                
        # Пересчет расстояния до гориллы
        dx = gorilla.x - self.x
        dy = gorilla.y - self.y
        dist = math.hypot(dx, dy)
        
        # Состояния страха приоритетнее других
        if self.feared > 0:
            self.feared -= 1
            self.state = "flee"
            self.state_timer = max(self.state_timer, self.feared)
        
        # Логика атаки
        if dist < self.attack_range and not gorilla.invulnerable:
            if self.type == "warrior" or self.type == "civilian":
                # Ближний бой
                self.state = "attack"
            elif self.type == "archer" and dist > self.attack_range * 0.5:
                # Лучники предпочитают атаковать с расстояния
                self.state = "ranged_attack"
                
        # Лучники убегают, если горилла слишком близко
        elif self.type == "archer" and dist < self.attack_range * 1.5:
            self.state = "flee"
            
        # Люди боятся гориллы в ярости
        elif dist < 100 and gorilla.rage_mode and not (self.type == "warrior" and self.morale > 80):
            self.state = "flee"
            
        # Поворачиваемся в нужном направлении
        if dx != 0 or dy != 0:
            target_angle = math.atan2(dy, dx)
            angle_diff = (target_angle - self.facing_angle + math.pi) % (2 * math.pi) - math.pi
            self.facing_angle += angle_diff * 0.1
            
        # Выполняем действия в зависимости от состояния
        if self.state == "attack":
            if self.attack_cooldown <= 0:
                # Базовый урон
                damage = self.attack_damage
                
                # Увеличиваем урон с уровнем опыта
                damage *= (1 + self.level * 0.1)
                
                # Тип воина наносит больше урона
                if self.type == "warrior":
                    damage *= 1.5
                    
                # Применяем урон
                if not gorilla.invulnerable:
                    gorilla.health -= damage
                    
                    # Визуальный эффект удара
                    if dist < DETAIL_LEVELS['full'] and random.random() < 0.3 and gorilla.particles:
                        gorilla.particles.add(
                            gorilla.x + random.uniform(-10, 10),
                            gorilla.y + random.uniform(-10, 10),
                            (150, 150, 150),
                            random.uniform(2, 4),
                            random.uniform(1, 2),
                            10,
                            type="spark"
                        )
                    
                    # Кулдаун атаки зависит от типа
                    if self.type == "warrior":
                        self.attack_cooldown = 40
                    else:  # civilian
                        self.attack_cooldown = 50
                        
                    # Затраты стамины на атаку
                    self.stamina -= 5
                    if self.stamina <= 0:
                        self.exhausted = True
                        self.stamina = 0
                        self.state = "flee"
                        self.state_timer = random.randint(90, 150)
                        
                    # Получаем опыт за удачную атаку
                    self.experience += damage * 0.1
                    
                    # Проверяем повышение уровня
                    if self.experience >= 100 * self.level and self.level < 5:
                        self.level += 1
                        self.experience = 0
                        
                        # Улучшения с уровнем
                        self.attack_damage += 1
                        self.max_health += 20
                        self.health += 20
                        self.max_stamina += 10
                        self.stamina += 10
        
        elif self.state == "ranged_attack":
            # Только для лучников
            if self.type == "archer" and self.arrow_cooldown <= 0 and dist < self.max_arrow_range:
                # Стрельба из лука
                arrow_damage = self.attack_damage * 1.2
                
                # Увеличиваем урон с уровнем опыта
                arrow_damage *= (1 + self.level * 0.15)
                
                # Шанс попадания зависит от расстояния
                hit_chance = 0.8 - (dist / self.max_arrow_range) * 0.5
                
                if random.random() < hit_chance and not gorilla.invulnerable:
                    # Попали
                    gorilla.health -= arrow_damage
                    
                    # Визуальный эффект попадания
                    angle = math.atan2(gorilla.y - self.y, gorilla.x - self.x)
                    if gorilla.particles:
                        for _ in range(3):
                            gorilla.particles.add(
                                gorilla.x + random.uniform(-5, 5),
                                gorilla.y + random.uniform(-5, 5),
                                (150, 100, 50),
                                random.uniform(1, 3),
                                random.uniform(0.5, 1.5),
                                15,
                                angle=angle,
                                spread=0.3
                            )
                            
                    # Получаем опыт за попадание
                    self.experience += arrow_damage * 0.15
                
                # Стрела в любом случае выпущена
                self.arrow_cooldown = 70
                
                # Затраты стамины
                self.stamina -= 3
                if self.stamina <= 0:
                    self.exhausted = True
                    self.stamina = 0
                    self.state = "flee"
                    self.state_timer = random.randint(90, 150)
                    
                # После выстрела лучник отходит назад
                if random.random() < 0.7:
                    self.state = "reposition"
                    self.state_timer = random.randint(30, 50)
                    
                # Проверяем повышение уровня
                if self.experience >= 100 * self.level and self.level < 5:
                    self.level += 1
                    self.experience = 0
                    
                    # Улучшения с уровнем для лучника
                    self.attack_damage += 1
                    self.max_arrow_range += 20
                    self.max_health += 15
                    self.health += 15
                    self.max_stamina += 10
                    self.stamina += 10
                
        elif self.state == "reposition":
            # Лучники перемещаются, чтобы занять удобную позицию для стрельбыimport pygame
import random
import math
import os
import numpy as np
from collections import defaultdict

pygame.init()

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1 Горилла vs 1000 Людей - Симуляция Реализма")
clock = pygame.time.Clock()

HUMAN_COUNT = 1000
DETAIL_LEVELS = {
    'full': 0,
    'medium': 100,
    'low': 200,
    'minimal': 400
}

# Новые константы
TERRAIN_TYPES = {
    'grass': {'color': (34, 100, 34), 'speed_mod': 1.0},
    'mud': {'color': (90, 70, 30), 'speed_mod': 0.7},
    'rock': {'color': (120, 120, 120), 'speed_mod': 0.85},
    'water': {'color': (50, 100, 200), 'speed_mod': 0.5},
}

HUMAN_TYPES = {
    'civilian': {'speed': (1.8, 2.3), 'health': 80, 'damage': 1, 'color': (100, 100, 255), 'prob': 0.7},
    'warrior': {'speed': (2.0, 2.7), 'health': 120, 'damage': 3, 'color': (200, 100, 100), 'prob': 0.2},
    'archer': {'speed': (1.9, 2.5), 'health': 90, 'damage': 2, 'color': (100, 200, 100), 'prob': 0.1},
}

# --- Оптимизированные структуры данных ---
IMAGE_CACHE = {}
SPATIAL_HASH_CELL_SIZE = 50
STATIC_OBSTACLES = []  # Список препятствий

# --- ЗАГРУЗКА ИЗОБРАЖЕНИЙ ---
def load_image(name, size):
    cache_key = f"{name}_{size[0]}_{size[1]}"
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]
    if not os.path.exists('images'):
        os.makedirs('images')
    path = os.path.join('images', name)
    if not os.path.exists(path):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        if name.startswith("gorilla"):
            body_color = (50, 50, 50)
            face_color = (40, 40, 40)
            highlight = (70, 70, 70)
            pygame.draw.ellipse(surf, body_color, (10, 20, 60, 50))
            pygame.draw.circle(surf, face_color, (size[0]//2, size[1]//2-5), size[0]//3)
            pygame.draw.ellipse(surf, body_color, (5, 25, 20, 40))
            pygame.draw.ellipse(surf, body_color, (55, 25, 20, 40))
            pygame.draw.circle(surf, (255, 255, 255), (30, 30), 5)
            pygame.draw.circle(surf, (255, 255, 255), (50, 30), 5)
            pygame.draw.circle(surf, (0, 0, 0), (30, 30), 3)
            pygame.draw.circle(surf, (0, 0, 0), (50, 30), 3)
            pygame.draw.arc(surf, (120, 60, 60), (30, 40, 20, 10), 0, math.pi, 3)
            pygame.draw.ellipse(surf, highlight, (15, 15, 10, 5))
        elif name.startswith("human_"):
            # Определяем тип человека из имени
            h_type = name.split('_')[1].split('.')[0]  # Извлекаем тип из имени файла
            
            skin_colors = [(255, 210, 150), (240, 190, 130), (210, 160, 120), (165, 120, 90), (140, 95, 75)]
            hair_colors = [(20, 20, 20), (60, 40, 20), (120, 80, 40), (200, 150, 100), (160, 80, 50)]
            skin_color = random.choice(skin_colors)
            hair_color = random.choice(hair_colors)
            
            # Базовое тело для всех
            pygame.draw.circle(surf, skin_color, (size[0]//2, size[1]//2-2), size[0]//4)
            
            # Разные прически для разных типов людей
            if h_type == "civilian":
                pygame.draw.rect(surf, hair_color, (size[0]//2-7, size[1]//2-10, 14, 5))
                clothes_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            elif h_type == "warrior":
                # Воины с шлемами
                helmet_color = (150, 150, 150)
                pygame.draw.rect(surf, helmet_color, (size[0]//2-8, size[1]//2-10, 16, 8))
                pygame.draw.rect(surf, helmet_color, (size[0]//2-6, size[1]//2-15, 12, 5))
                clothes_color = (200, 50, 50)
            elif h_type == "archer":
                # Лучники с капюшонами
                hood_color = (0, 100, 0)
                pygame.draw.circle(surf, hood_color, (size[0]//2, size[1]//2-5), size[0]//3 + 1)
                pygame.draw.circle(surf, skin_color, (size[0]//2, size[1]//2-2), size[0]//4)
                clothes_color = (50, 150, 50)
            else:  # Для простых силуэтов
                clothes_color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            
            # Тело
            pygame.draw.ellipse(surf, clothes_color, (size[0]//2-5, size[1]//2+2, 10, 12))
            
            # Оружие для воинов и лучников
            if h_type == "warrior":
                weapon_color = (100, 100, 100)
                pygame.draw.rect(surf, weapon_color, (size[0]//2+8, size[1]//2-5, 2, 15))
            elif h_type == "archer":
                bow_color = (139, 69, 19)
                pygame.draw.arc(surf, bow_color, (size[0]//2+3, size[1]//2-10, 10, 20), -math.pi/2, math.pi/2, 2)
        elif name.startswith("human_simple"):
            color = (random.randint(150, 255), random.randint(150, 200), random.randint(100, 200))
            pygame.draw.circle(surf, color, (size[0]//2, size[1]//2), size[0]//2-2)
        elif name.startswith("obstacle"):
            obstacle_type = name.split('_')[1]
            if obstacle_type == "rock":
                # Создаем камень с рандомной формой
                rock_color = (80, 80, 80)
                rock_points = []
                for i in range(8):
                    angle = 2 * math.pi * i / 8
                    radius = size[0] // 2 * random.uniform(0.8, 1.0)
                    x = size[0] // 2 + radius * math.cos(angle)
                    y = size[1] // 2 + radius * math.sin(angle)
                    rock_points.append((x, y))
                pygame.draw.polygon(surf, rock_color, rock_points)
                # Добавляем детали
                for _ in range(3):
                    x = random.randint(size[0]//4, 3*size[0]//4)
                    y = random.randint(size[1]//4, 3*size[1]//4)
                    radius = random.randint(2, 5)
                    pygame.draw.circle(surf, (60, 60, 60), (x, y), radius)
            elif obstacle_type == "tree":
                # Ствол
                trunk_color = (80, 60, 30)
                pygame.draw.rect(surf, trunk_color, (size[0]//2-5, size[1]//2, 10, size[1]//2))
                # Крона
                leaf_color = (30, 100, 30)
                pygame.draw.circle(surf, leaf_color, (size[0]//2, size[1]//3), size[0]//3)
        elif name.startswith("jungle"):
            # Базовое небо с градиентом
            gradient_height = size[1] // 3
            for y in range(0, gradient_height, 2):
                alpha = 255 - int(y * 128 / gradient_height)
                sky_color = (100, 150 + y//8, 255, alpha)
                pygame.draw.line(surf, sky_color, (0, y), (size[0], y))
            
            # Заполняем карту типами местности
            # Основная трава
            pygame.draw.rect(surf, TERRAIN_TYPES['grass']['color'], 
                            (0, gradient_height, size[0], size[1] - gradient_height))
            
            # Добавляем области с грязью
            for _ in range(5):
                mud_size = random.randint(100, 200)
                mud_x = random.randint(0, size[0])
                mud_y = random.randint(gradient_height, size[1])
                
                # Создаем неправильную форму болота
                for i in range(20):
                    angle = random.uniform(0, 2*math.pi)
                    dist = random.uniform(0.5, 1.0) * mud_size
                    x = mud_x + math.cos(angle) * dist
                    y = mud_y + math.sin(angle) * dist
                    pygame.draw.circle(surf, TERRAIN_TYPES['mud']['color'], (int(x), int(y)), 
                                     random.randint(20, 40))
            
            # Добавляем скалистые участки
            for _ in range(3):
                rock_size = random.randint(80, 150)
                rock_x = random.randint(0, size[0])
                rock_y = random.randint(gradient_height, size[1])
                
                # Создаем неправильную форму скалы
                for i in range(15):
                    angle = random.uniform(0, 2*math.pi)
                    dist = random.uniform(0.5, 1.0) * rock_size
                    x = rock_x + math.cos(angle) * dist
                    y = rock_y + math.sin(angle) * dist
                    pygame.draw.circle(surf, TERRAIN_TYPES['rock']['color'], (int(x), int(y)), 
                                     random.randint(15, 30))
            
            # Добавляем водоемы
            for _ in range(2):
                water_size = random.randint(70, 150)
                water_x = random.randint(0, size[0])
                water_y = random.randint(gradient_height, size[1])
                
                # Создаем неправильную форму водоема
                for i in range(25):
                    angle = random.uniform(0, 2*math.pi)
                    dist = random.uniform(0.5, 1.0) * water_size
                    x = water_x + math.cos(angle) * dist
                    y = water_y + math.sin(angle) * dist
                    pygame.draw.circle(surf, TERRAIN_TYPES['water']['color'], (int(x), int(y)), 
                                     random.randint(20, 35))
            
            # Добавляем детали джунглей
            for _ in range(150):
                x = random.randint(0, size[0])
                y = random.randint(gradient_height, size[1])
                radius = random.randint(15, 50)
                green_shade = random.randint(60, 120)
                transparency = random.randint(100, 200)
                pygame.draw.circle(surf, (30, green_shade, 30, transparency), (x, y), radius)
    else:
        surf = pygame.image.load(path)
        
    surf = pygame.transform.scale(surf, size)
    pygame.image.save(surf, path)
    IMAGE_CACHE[cache_key] = surf
    return surf

# Загружаем все необходимые изображения
gorilla_img = load_image("gorilla.png", (80, 80))
human_civilian_img = load_image("human_civilian.png", (24, 24))
human_warrior_img = load_image("human_warrior.png", (24, 24))
human_archer_img = load_image("human_archer.png", (24, 24))
human_simple_img = load_image("human_simple.png", (10, 10))
background_img = load_image("jungle_background.png", (WIDTH, HEIGHT))
rock_img = load_image("obstacle_rock.png", (60, 60))
tree_img = load_image("obstacle_tree.png", (80, 120))

# --- Оптимизированный хэш пространства для быстрого поиска ближайших объектов ---
class SpatialHash:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = defaultdict(list)
        
    def _get_cell(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def _get_nearby_cells(self, x, y, radius=1):
        center_cell = self._get_cell(x, y)
        cells = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                cells.append((center_cell[0] + dx, center_cell[1] + dy))
        return cells
    
    def clear(self):
        self.grid.clear()
        
    def insert(self, obj):
        cell = self._get_cell(obj.x, obj.y)
        self.grid[cell].append(obj)
        
    def get_nearby(self, x, y, radius=1):
        nearby_objects = []
        for cell in self._get_nearby_cells(x, y, radius):
            nearby_objects.extend(self.grid[cell])
        return nearby_objects

# --- Оптимизированные частицы ---
class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 800  # Увеличено для большей визуальной реалистичности
        
    def add(self, x, y, color=(255,255,255), size=3, speed=2, lifetime=30, gravity=0, fade=True, type="circle", 
           angle=None, spread=2*math.pi):
        if len(self.particles) >= self.max_particles:
            self.particles.pop(0)
            
        if angle is None:
            angle = random.uniform(0, 2*math.pi)
        else:
            angle = angle + random.uniform(-spread/2, spread/2)
            
        self.particles.append({
            'x': x, 'y': y, 'color': color, 'size': size, 'initial_size': size,
            'speed': speed, 'angle': angle, 'lifetime': lifetime,
            'max_lifetime': lifetime, 'gravity': gravity, 'fade': fade, 'type': type,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'spin': random.uniform(-0.2, 0.2),  # Добавляем вращение для искр
            'current_angle': angle  # Текущий угол для рисования
        })

    def update(self):
        i = 0
        while i < len(self.particles):
            p = self.particles[i]
            p['x'] += p['vx']
            p['y'] += p['vy'] + p['gravity']
            p['gravity'] += 0.01
            
            # Физически правдоподобное замедление
            drag = 0.98
            p['vx'] *= drag
            p['vy'] *= drag
            
            p['lifetime'] -= 1
            p['current_angle'] += p['spin']  # Обновляем угол для рисования
            
            if p['fade']:
                # Более плавное затухание на основе синусоиды
                fade_factor = math.sin((p['lifetime'] / p['max_lifetime']) * math.pi / 2)
                p['size'] = max(0, p['initial_size'] * fade_factor)
                
            if p['lifetime'] <= 0:
                self.particles.pop(i)
            else:
                i += 1

    def draw(self, surf):
        for p in self.particles:
            if p['lifetime'] <= 0:
                continue
                
            alpha = int(255 * (p['lifetime']/p['max_lifetime'])) if p['fade'] else 255
            
            if p['type'] == "circle":
                s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], alpha), (int(p['size']), int(p['size'])), int(p['size']))
                surf.blit(s, (int(p['x']-p['size']), int(p['y']-p['size'])))
                
            elif p['type'] == "square":
                s = pygame.Surface((int(p['size']), int(p['size'])), pygame.SRCALPHA)
                s.fill((*p['color'], alpha))
                # Вращаем квадрат
                rotated = pygame.transform.rotate(s, math.degrees(p['current_angle']))
                surf.blit(rotated, (int(p['x'] - rotated.get_width()/2), 
                                 int(p['y'] - rotated.get_height()/2)))
                
            elif p['type'] == "spark":
                # Искры теперь рисуются с учетом угла движения
                length = max(3, p['size'] * 2)
                end_x = p['x'] - math.cos(p['current_angle']) * length
                end_y = p['y'] - math.sin(p['current_angle']) * length
                # Добавляем свечение
                for i in range(2):
                    thickness = max(1, int(p['size']) - i)
                    glow_alpha = alpha // (i+1)
                    pygame.draw.line(surf, (*p['color'], glow_alpha),
                                   (int(p['x']), int(p['y'])),
                                   (int(end_x), int(end_y)),
                                   thickness)

# --- Эффекты окружения ---
class EnvironmentEffect:
    def __init__(self):
        self.particles = ParticleSystem()
        self.light_rays = []
        self.ambient_particles = []
        self.rain_particles = []
        self.leaf_particles = []
        self.weather_type = "clear"  # "clear", "rain", "wind"
        self.weather_intensity = 0.0  # 0.0 - 1.0
        self.weather_change_timer = random.randint(1000, 3000)
        
        # Создаем световые лучи
        for _ in range(8):
            self.light_rays.append({
                'x': random.randint(0, WIDTH),
                'y': 0,
                'width': random.randint(20, 60),
                'height': random.randint(200, 400),
                'alpha': random.randint(20, 60),
                'speed': random.uniform(0.1, 0.5)
            })
            
        # Создаем частицы в воздухе (пыль, туман)
        for _ in range(100):
            self.ambient_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(0.5, 2),
                'speed': random.uniform(0.1, 0.5),
                'angle': random.uniform(0, 2*math.pi),
                'alpha': random.randint(50, 150)
            })
            
        # Подготавливаем частицы дождя и листьев (используются при определенной погоде)
        for _ in range(200):
            self.rain_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(-100, -10),
                'length': random.randint(5, 15),
                'speed': random.randint(10, 15),
                'active': False
            })
            
        for _ in range(30):
            self.leaf_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(2, 5),
                'speed': random.uniform(0.5, 2.0),
                'angle': random.uniform(0, 2*math.pi),
                'spin': random.uniform(-0.1, 0.1),
                'current_angle': random.uniform(0, 2*math.pi),
                'active': False
            })

    def change_weather(self):
        # Случайно выбираем новую погоду
        weather_types = ["clear", "rain", "wind"]
        weights = [0.6, 0.25, 0.15]  # Вероятности для каждого типа погоды
        self.weather_type = random.choices(weather_types, weights=weights)[0]
        
        # Устанавливаем интенсивность (нарастает и убывает плавно)
        self.weather_intensity = 0.0
        self.weather_change_timer = random.randint(1000, 3000)  # Время до следующей смены погоды
        
        # Активируем соответствующие эффекты
        if self.weather_type == "rain":
            for p in self.rain_particles:
                p['active'] = True
                p['x'] = random.randint(0, WIDTH)
                p['y'] = random.randint(-100, -10)
                
        elif self.weather_type == "wind":
            for p in self.leaf_particles:
                p['active'] = True
                # Запускаем листья с края экрана в направлении ветра
                p['x'] = -10 if random.random() < 0.5 else WIDTH + 10
                p['y'] = random.randint(0, HEIGHT)
                p['angle'] = 0 if p['x'] < 0 else math.pi  # Направление ветра слева или справа

    def update(self):
        self.particles.update()
        
        # Обновляем таймер погоды
        self.weather_change_timer -= 1
        if self.weather_change_timer <= 0:
            self.change_weather()
            
        # Плавно изменяем интенсивность погоды
        target_intensity = 1.0 if self.weather_type != "clear" else 0.0
        self.weather_intensity += (target_intensity - self.weather_intensity) * 0.01
        
        # Световые лучи
        for ray in self.light_rays:
            ray['x'] += math.sin(pygame.time.get_ticks() / 5000) * ray['speed']
            
        # Частицы в воздухе
        for p in self.ambient_particles:
            p['x'] += math.cos(p['angle']) * p['speed']
            p['y'] += math.sin(p['angle']) * p['speed']
            if p['x'] < 0: p['x'] = WIDTH
            elif p['x'] > WIDTH: p['x'] = 0
            if p['y'] < 0: p['y'] = HEIGHT
            elif p['y'] > HEIGHT: p['y'] = 0
            if random.random() < 0.005:
                p['angle'] = random.uniform(0, 2*math.pi)
                
        # Обновляем дождь, если активен
        if self.weather_type == "rain":
            for p in self.rain_particles:
                if p['active']:
                    p['y'] += p['speed']
                    # Легкий уклон капель от ветра
                    p['x'] += random.uniform(-0.5, 0.5)
                    
                    # Если капля достигла земли, перезапускаем ее сверху
                    if p['y'] > HEIGHT:
                        p['y'] = random.randint(-100, -10)
                        p['x'] = random.randint(0, WIDTH)
                        
                        # Создаем всплеск при падении
                        if random.random() < 0.3 * self.weather_intensity:
                            self.particles.add(
                                p['x'], HEIGHT,
                                (200, 200, 255),
                                random.uniform(1, 2),
                                random.uniform(0.5, 1.5),
                                random.randint(10, 20),
                                gravity=-0.05
                            )
        
        # Обновляем эффект ветра, если активен
        if self.weather_type == "wind":
            wind_direction = 0  # Направление ветра (0 - справа налево)
            wind_speed = 2.0 * self.weather_intensity
            
            for p in self.leaf_particles:
                if p['active']:
                    # Добавляем случайное движение для реалистичности
                    p['angle'] = wind_direction + random.uniform(-0.5, 0.5)
                    p['x'] += math.cos(p['angle']) * p['speed'] * wind_speed
                    p['y'] += math.sin(p['angle']) * p['speed'] * 0.5 + math.sin(pygame.time.get_ticks() / 500 + p['x'] * 0.01) * 0.5
                    
                    # Закручиваем лист
                    p['current_angle'] += p['spin']
                    
                    # Перезапускаем лист, если он вышел за границы
                    if (p['x'] < -20 and wind_direction < math.pi/2) or \
                       (p['x'] > WIDTH + 20 and wind_direction > math.pi/2) or \
                       p['y'] > HEIGHT + 20:
                        p['x'] = -10 if wind_direction < math.pi/2 else WIDTH + 10
                        p['y'] = random.randint(0, HEIGHT)

    def draw(self, surf, time_manager):
        # Рисуем световые лучи (только днем)
        if not time_manager.is_night():
            for ray in self.light_rays:
                light_surf = pygame.Surface((ray['width'], ray['height']), pygame.SRCALPHA)
                for i in range(0, ray['height'], 4):
                    alpha = ray['alpha'] * (1 - i / ray['height'])
                    pygame.draw.line(light_surf, (255, 255, 200, int(alpha)),
                                   (0, i), (ray['width'], i), 3)
                surf.blit(light_surf, (ray['x'], ray['y']))
        
        # Рисуем частицы в воздухе
        for i, p in enumerate(self.ambient_particles):
            if i % 2 == 0:
                alpha = int(p['alpha'] * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() / 1000)))
                pygame.draw.circle(surf, (255, 255, 255, alpha),
                                 (int(p['x']), int(p['y'])), int(p['size']))
        
        # Рисуем дождь
        if self.weather_type == "rain" and self.weather_intensity > 0.1:
            rain_alpha = int(150 * self.weather_intensity)
            for p in self.rain_particles:
                if p['active'] and 0 <= p['y'] <= HEIGHT:
                    # Рисуем каплю
                    pygame.draw.line(surf, (200, 200, 255, rain_alpha),
                                   (int(p['x']), int(p['y'])),
                                   (int(p['x'] - 1), int(p['y'] + p['length'])),
                                   1)
        
        # Рисуем листья
        if self.weather_type == "wind" and self.weather_intensity > 0.1:
            for p in self.leaf_particles:
                if p['active']:
                    # Рисуем лист как маленький овал с поворотом
                    leaf_surf = pygame.Surface((int(p['size'] * 3), int(p['size'])), pygame.SRCALPHA)
                    leaf_color = (50, 100 + random.randint(0, 50), 30, 200)
                    pygame.draw.ellipse(leaf_surf, leaf_color, (0, 0, int(p['size'] * 3), int(p['size'])))
                    
                    # Поворачиваем лист
                    rotated_leaf = pygame.transform.rotate(leaf_surf, math.degrees(p['current_angle']))
                    surf.blit(rotated_leaf, (int(p['x'] - rotated_leaf.get_width() // 2),
                                           int(p['y'] - rotated_leaf.get_height() // 2)))
                    
        # Рисуем дополнительные эффекты
        self.particles.draw(surf)
        
        # Добавляем туман при дожде
        if self.weather_type == "rain" and self.weather_intensity > 0.3:
            fog_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fog_color = (200, 200, 255, int(30 * self.weather_intensity))
            fog_surf.fill(fog_color)
            surf.blit(fog_surf, (0, 0))


# --- Время суток ---
class TimeManager:
    def __init__(self):
        self.time_of_day = 0
        self.transition_progress = 0
        self.cycle_duration = 60000  # Длительность полного цикла в мс
        self.phase_duration = self.cycle_duration / 4
        self.time_colors = [
            (200, 150, 100, 30),  # Рассвет
            (255, 255, 255, 20),  # День
            (255, 180, 80, 60),   # Закат
            (20, 20, 60, 130)     # Ночь
        ]
        self.day_count = 1  # Счетчик дней для прогрессии
        self.time_factor = 1.0  # Множитель скорости времени
        
    def update(self):
        ticks = pygame.time.get_ticks() * self.time_factor
        cycle_position = (ticks % self.cycle_duration) / self.cycle_duration
        
        # Обновляем текущую фазу дня
        old_time = self.time_of_day
        self.time_of_day = int(cycle_position * 4)
        self.transition_progress = (cycle_position * 4) % 1
        
        # Если перешли от ночи к утру, увеличиваем счетчик дней
        if old_time == 3 and self.time_of_day == 0:
            self.day_count += 1

    def get_overlay_color(self):
        next_phase = (self.time_of_day + 1) % 4
        current_color = self.time_colors[self.time_of_day]
        next_color = self.time_colors[next_phase]
        
        # Интерполируем цвета для плавного перехода
        r = int(current_color[0] * (1 - self.transition_progress) + next_color[0] * self.transition_progress)
        g = int(current_color[1] * (1 - self.transition_progress) + next_color[1] * self.transition_progress)
        b = int(current_color[2] * (1 - self.transition_progress) + next_color[2] * self.transition_progress)
        a = int(current_color[3] * (1 - self.transition_progress) + next_color[3] * self.transition_progress)
        
        return (r, g, b, a)

    def is_night(self):
        return self.time_of_day == 3 or (self.time_of_day == 2 and self.transition_progress > 0.7)
    
    def get_light_factor(self):
        # Возвращает коэффициент освещенности (1.0 - яркий день, 0.0 - темная ночь)
        if self.time_of_day == 1:  # День
            return 1.0
        elif self.time_of_day == 0:  # Рассвет
            return 0.6 + 0.4 * self.transition_progress
        elif self.time_of_day == 2:  # Закат
            return 0.6 * (1.0 - self.transition_progress)
        else:  # Ночь
            return 0.1

# --- Оптимизированная отрисовка фона ---
def draw_background(screen, time_manager, environment):
    # Отрисовка базового фона
    screen.blit(background_img, (0, 0))
    
    # Применяем цветовую накладку в зависимости от времени суток
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(time_manager.get_overlay_color())
    screen.blit(overlay, (0, 0))
    
    # Рисуем звезды ночью
    if time_manager.is_night():
        for _ in range(50):
            star_size = random.uniform(0.5, 2)
            star_brightness = random.randint(150, 255)
            star_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT // 3))
            
            # Мерцание звезд
            flicker = (math.sin(pygame.time.get_ticks() / 1000 + star_pos[0] * 0.01) * 50) + 200
            star_brightness = min(255, max(100, int(flicker)))
            
            pygame.draw.circle(screen, (star_brightness, star_brightness, star_brightness), 
                             star_pos, star_size)
            
            # Добавляем свечение для ярких звезд
            if star_size > 1.5:
                glow_size = star_size * 2
                glow_surf = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
                for i in range(3):
                    glow_alpha = max(0, 150 - i * 50)
                    pygame.draw.circle(glow_surf, (star_brightness, star_brightness, star_brightness, glow_alpha),
                                     (int(glow_size), int(glow_size)), glow_size - i)
                screen.blit(glow_surf, (int(star_pos[0] - glow_size), int(star_pos[1] - glow_size)))

    # Отрисовываем эффекты окружения (дождь, туман и т.д.)
    environment.draw(screen, time_manager)


# --- Класс препятствия ---
class Obstacle:
    def __init__(self, x, y, type_name, size=None):
        self.x = x
        self.y = y
        self.type = type_name
        
        if self.type == "rock":
            self.img = rock_img
            self.radius = 30 if size is None else size
            self.passable = False
        elif self.type == "tree":
            self.img = tree_img
            self.radius = 25 if size is None else size
            self.passable = False
        elif self.type == "bush":
            self.radius = 15 if size is None else size
            self.passable = True  # Через кусты можно проходить, но медленнее
        else:
            self.radius = 20 if size is None else size
            self.passable = False
            
        # Масштабируем изображение в соответствии с радиусом
        if hasattr(self, 'img'):
            aspect_ratio = self.img.get_height() / self.img.get_width()
            new_width = self.radius * 2
            new_height = int(new_width * aspect_ratio)
            self.img = pygame.transform.scale(self.img, (new_width, new_height))
        
    def draw(self, screen, time_manager=None):
        # Рисуем тень
        shadow_offset = 5
        shadow = pygame.Surface((self.radius*2, self.radius), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 100), (0, 0, self.radius*2, self.radius))
        screen.blit(shadow, (int(self.x - self.radius), int(self.y + self.radius*0.5 + shadow_offset)))
        
        # Рисуем препятствие
        if self.type == "rock":
            screen.blit(self.img, (int(self.x - self.radius), int(self.y - self.radius)))
        elif self.type == "tree":
            screen.blit(self.img, (int(self.x - self.radius), int(self.y - self.img.get_height() + self.radius)))
        elif self.type == "bush":
            # Рисуем куст как зеленый круг с деталями
            pygame.draw.circle(screen, (30, 100, 30), (int(self.x), int(self.y)), self.radius)
            # Добавляем детали куста
            for _ in range(5):
                detail_x = self.x + random.uniform(-self.radius*0.8, self.radius*0.8)
                detail_y = self.y + random.uniform(-self.radius*0.8, self.radius*0.8)
                detail_size = random.uniform(self.radius*0.3, self.radius*0.5)
                pygame.draw.circle(screen, (50, 120, 50), (int(detail_x), int(detail_y)), int(detail_size))


# --- Персонажи ---
class Gorilla:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 40
        self.base_speed = 3.0
        self.speed = self.base_speed
        self.health = 18000
        self.max_health = 18000
        self.stamina = 100
        self.max_stamina = 100
        self.attack_range = 80
        self.base_attack_damage = 40
        self.attack_damage = self.base_attack_damage
        self.attack_cooldown = 0
        self.target = None
        self.particles = ParticleSystem()
        self.rage_mode = False
        self.rage_timer = 0
        self.kills = 0
        self.shadow_offset = 0
        self.area_attack_cooldown = 0
        self.attack_type = "normal"  # normal, grab, pound
        self.grabbed_human = None
        self.grab_timer = 0
        self.pound_cooldown = 0
        self.stamina_regen_rate = 0.1
        self.experience = 0
        self.level = 1
        self.experience_to_level = 100
        self.terrain_speed_mod = 1.0
        
        # Новые атаки и способности, открываемые с уровнями
        self.abilities = {
            "pound": {"unlocked": False, "level": 3, "cooldown": 200, "current_cooldown": 0},
            "throw": {"unlocked": False, "level": 5, "cooldown": 150, "current_cooldown": 0},
            "roar": {"unlocked": False, "level": 7, "cooldown": 300, "current_cooldown": 0},
            "leap": {"unlocked": False, "level": 10, "cooldown": 250, "current_cooldown": 0}
        }
        
        # Состояние горилы
        self.state = "idle"
        self.state_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Для атаки прыжком
        self.leap_target_x = None
        self.leap_target_y = None
        self.leap_speed = 0
        self.leap_height = 0
        self.leap_progress = 0
        
        # Анимация
        self.animation_frame = 0
        self.animation_speed = 0.2
        
        # Обновление способностей при инициализации
        self.check_level_abilities()

    def draw(self, screen):
        # Тень с анимацией
        self.shadow_offset = 3 + math.sin(pygame.time.get_ticks() / 200) * 1.5
        
        # Если горилла в прыжке, тень отделяется от горилы
        if self.state == "leap":
            leap_shadow_offset = max(self.shadow_offset, 
                                   self.leap_height * math.sin(self.leap_progress * math.pi))
            shadow_x = int(self.x - self.size)
            shadow_y = int(self.y + self.size*0.5 + leap_shadow_offset)
            
            # Размер тени меняется в зависимости от высоты прыжка
            shadow_scale = max(0.5, 1.0 - 0.5 * math.sin(self.leap_progress * math.pi))
            shadow_width = int(self.size * 2 * shadow_scale)
            shadow_height = int(self.size * shadow_scale)
            
            shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 100), (0, 0, shadow_width, shadow_height))
            screen.blit(shadow, (int(shadow_x + (self.size - shadow_width/2)), shadow_y))
        else:
            # Обычная тень
            shadow = pygame.Surface((self.size*2, self.size), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 100), (0, 0, self.size*2, self.size))
            screen.blit(shadow, (int(self.x-self.size), int(self.y+self.size*0.5 + self.shadow_offset)))
        
        # Аура в режиме ярости или неуязвимости
        if self.rage_mode or self.invulnerable:
            aura_color = (255, 50, 0) if self.rage_mode else (220, 220, 50)
            for i in range(5):
                angle = pygame.time.get_ticks() / 500 + i * math.pi / 3
                radius = 50 + math.sin(pygame.time.get_ticks() / 300) * 10
                glow_x = self.x + math.cos(angle) * radius
                glow_y = self.y + math.sin(angle) * radius
                glow_size = 20 + math.sin(pygame.time.get_ticks() / 150) * 5
                glow_surface = pygame.Surface((int(glow_size*2), int(glow_size*2)), pygame.SRCALPHA)
                intensity = 200 + math.sin(pygame.time.get_ticks() / 200) * 55
                
                if self.rage_mode:
                    glow_color = (int(intensity), 0, 0, 150)
                else:
                    glow_color = (int(intensity), int(intensity), 0, 120)
                    
                pygame.draw.circle(glow_surface, glow_color,
                                 (int(glow_size), int(glow_size)), int(glow_size))
                screen.blit(glow_surface, (int(glow_x - glow_size), int(glow_y - glow_size)))
                
            if random.random() < 0.15:
                angle = random.uniform(0, 2*math.pi)
                distance = random.uniform(30, 60)
                particle_x = self.x + math.cos(angle) * distance
                particle_y = self.y + math.sin(angle) * distance
                
                self.particles.add(
                    particle_x, particle_y,
                    aura_color,
                    random.uniform(3, 8),
                    random.uniform(0.5, 2),
                    60,
                    gravity=-0.1
                )
            
            # Красноватый оттенок для гориллы в ярости
            if self.rage_mode:
                tinted_img = gorilla_img.copy()
                red_overlay = pygame.Surface(tinted_img.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 60))
                tinted_img.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                pulse = 1 + math.sin(pygame.time.get_ticks() / 150) * 0.1
                scaled_img = pygame.transform.scale(tinted_img,
                                                  (int(tinted_img.get_width() * pulse),
                                                   int(tinted_img.get_height() * pulse)))
                screen.blit(scaled_img, (int(self.x - scaled_img.get_width()//2),
                                       int(self.y - scaled_img.get_height()//2)))
            elif self.invulnerable:
                # Золотистое свечение при неуязвимости
                tinted_img = gorilla_img.copy()
                gold_overlay = pygame.Surface(tinted_img.get_size(), pygame.SRCALPHA)
                gold_overlay.fill((255, 215, 0, 60))
                tinted_img.blit(gold_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(tinted_img, (int(self.x - tinted_img.get_width()//2),
                                       int(self.y - tinted_img.get_height()//2)))
            else:
                screen.blit(gorilla_img, (int(self.x - gorilla_img.get_width()//2),
                                        int(self.y - gorilla_img.get_height()//2)))
        else:
            # Обычное отображение гориллы
            screen.blit(gorilla_img, (int(self.x - gorilla_img.get_width()//2),
                                    int(self.y - gorilla_img.get_height()//2)))
            
        # Если горилла держит человека
        if self.grabbed_human and self.grabbed_human.health > 0:
            # Располагаем человека рядом с гориллой
            offset_x = math.cos(pygame.time.get_ticks() / 200) * 10
            offset_y = math.sin(pygame.time.get_ticks() / 150) * 5
            self.grabbed_human.x = self.x + offset_x
            self.grabbed_human.y = self.y - 35 + offset_y
            
        # Полоска здоровья
        health_width = int((self.health / self.max_health) * self.size * 2.2)
        health_bg = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 25), self.size * 2.2, 8)
        health_bar = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 25), health_width, 8)
        
        pygame.draw.rect(screen, (50, 50, 50), health_bg, border_radius=4)
        if self.health / self.max_health > 0.6:
            health_color = GREEN
        elif self.health / self.max_health > 0.3:
            health_color = (255, 165, 0)
        else:
            health_color = RED
        pygame.draw.rect(screen, health_color, health_bar, border_radius=4)
        pygame.draw.rect(screen, BLACK, health_bg, 1, border_radius=4)
        
        # Полоска стамины
        stamina_width = int((self.stamina / self.max_stamina) * self.size * 2.2)
        stamina_bg = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 15), self.size * 2.2, 6)
        stamina_bar = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 15), stamina_width, 6)
        
        pygame.draw.rect(screen, (50, 50, 50), stamina_bg, border_radius=3)
        stamina_color = (50, 150, 255)
        pygame.draw.rect(screen, stamina_color, stamina_bar, border_radius=3)
        pygame.draw.rect(screen, BLACK, stamina_bg, 1, border_radius=3)
        
        # Полоска опыта
        if self.level < 10:  # Макс. уровень
            exp_percent = self.experience / self.experience_to_level
            exp_width = int(exp_percent * self.size * 2.2)
            exp_bg = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 35), self.size * 2.2, 4)
            exp_bar = pygame.Rect(int(self.x - self.size * 1.1), int(self.y - self.size - 35), exp_width, 4)
            
            pygame.draw.rect(screen, (50, 50, 50), exp_bg, border_radius=2)
            pygame.draw.rect(screen, (255, 215, 0), exp_bar, border_radius=2)
            pygame.draw.rect(screen, BLACK, exp_bg, 1, border_radius=2)
            
            # Текст уровня
            small_font = pygame.font.SysFont('Arial', 12)
            level_text = small_font.render(f"Ур. {self.level}", True, WHITE)
            screen.blit(level_text, (exp_bg.right - level_text.get_width() - 5, exp_bg.y - 15))
        
        # Текст здоровья
        small_font = pygame.font.SysFont('Arial', 12)
        health_text = small_font.render(f"{max(0, int(self.health))}/{self.max_health}", True, WHITE)
        screen.blit(health_text, (health_bg.centerx - health_text.get_width()//2, health_bg.y - 15))
        
        # Частицы
        self.particles.draw(screen)
        
        # Отображение активных способностей
        ability_font = pygame.font.SysFont('Arial', 10)
        ability_x = self.x - 80
        ability_y = self.y + 60
        
        for ability_name, ability in self.abilities.items():
            if ability["unlocked"]:
                if ability["current_cooldown"] > 0:
                    cooldown_percent = ability["current_cooldown"] / ability["cooldown"]
                    pygame.draw.rect(screen, (50, 50, 50), 
                                   (ability_x, ability_y, 20, 20), border_radius=3)
                    cooldown_height = int(20 * cooldown_percent)
                    pygame.draw.rect(screen, (100, 100, 100), 
                                   (ability_x, ability_y + 20 - cooldown_height, 20, cooldown_height), 
                                   border_radius=3)
                else:
                    pygame.draw.rect(screen, (200, 200, 50), 
                                   (ability_x, ability_y, 20, 20), border_radius=3)
                    
                # Первая буква способности
                ability_letter = ability_name[0].upper()
                text = ability_font.render(ability_letter, True, BLACK)
                screen.blit(text, (ability_x + 10 - text.get_width()//2, 
                                  ability_y + 10 - text.get_height()//2))
                ability_x += 25

    def check_level_abilities(self):
        # Проверяем и разблокируем способности в зависимости от уровня
        for ability_name, ability in self.abilities.items():
            if self.level >= ability["level"] and not ability["unlocked"]:
                ability["unlocked"] = True
                # Добавляем визуальный эффект при разблокировке
                for i in range(20):
                    angle = 2 * math.pi * i / 20
                    self.particles.add(
                        self.x + math.cos(angle) * 50,
                        self.y + math.sin(angle) * 50,
                        (255, 215, 0),
                        random.uniform(3, 6),
                        random.uniform(1, 3),
                        60,
                        type="spark",
                        angle=angle + math.pi,  # Частицы летят к горилле
                        spread=0.2
                    )

    def gain_experience(self, amount):
        self.experience += amount
        
        # Проверяем повышение уровня
        if self.experience >= self.experience_to_level and self.level < 10:
            old_level = self.level
            self.level += 1
            self.experience -= self.experience_to_level
            self.experience_to_level = int(self.experience_to_level * 1.5)  # Увеличиваем требуемый опыт
            
            # Улучшения при повышении уровня
            self.max_health += 2000
            self.health = min(self.health + 2000, self.max_health)
            self.base_attack_damage += 15
            self.attack_damage = self.base_attack_damage
            self.max_stamina += 20
            self.stamina = self.max_stamina
            self.stamina_regen_rate += 0.05
            
            # Проверяем новые способности
            self.check_level_abilities()
            
            # Визуальные эффекты для повышения уровня
            for i in range(2):
                for angle in range(0, 360, 10):
                    rad = math.radians(angle)
                    dist = 40 + i * 30
                    self.particles.add(
                        self.x + math.cos(rad) * dist,
                        self.y + math.sin(rad) * dist,
                        (255, 215, 0),
                        random.uniform(3, 7),
                        random.uniform(1, 4),
                        60,
                        type="spark"
                    )
            
            # Кратковременная неуязвимость при повышении уровня
            self.invulnerable = True
            self.invulnerable_timer = 90

    def move(self, humans, obstacles=None, spatial_hash=None):
        self.particles.update()
        
        # Обновляем таймеры и состояния
        if self.rage_mode:
            self.rage_timer -= 1
            if self.rage_timer <= 0:
                self.rage_mode = False
                self.speed = self.base_speed
                self.attack_damage = self.base_attack_damage
                for _ in range(10):
                    self.particles.add(
                        self.x + random.uniform(-30, 30),
                        self.y + random.uniform(-30, 30),
                        (255, 100, 0),
                        random.uniform(2, 6),
                        random.uniform(1, 3),
                        40,
                        type="spark"
                    )
                    
        # Регенерация стамины с течением времени
        if self.state != "leap":  # Не восстанавливаем во время прыжка
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen_rate)
            
        # Неуязвимость
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                
        # Обновляем кулдауны способностей
        for ability in self.abilities.values():
            if ability["current_cooldown"] > 0:
                ability["current_cooldown"] -= 1
        
        # Управление состояниями
        if self.state == "idle":
            # Поиск ближайшего человека, предпочитая тех, кто ближе к горилле
            if not self.target or self.target.health <= 0:
                min_dist = float('inf')
                if spatial_hash:
                    nearby_humans = spatial_hash.get_nearby(self.x, self.y, 2)
                    sample_size = min(200, len(nearby_humans))
                    for human in random.sample(nearby_humans, sample_size):
                        if human.health > 0:
                            dist = math.hypot(self.x - human.x, self.y - human.y)
                            if dist < min_dist:
                                min_dist = dist
                                self.target = human
                else:
                    sample_size = min(200, len(humans))
                    for human in random.sample(humans, sample_size):
                        if human.health > 0:
                            dist = math.hypot(self.x - human.x, self.y - human.y)
                            if dist < min_dist:
                                min_dist = dist
                                self.target = human
            
            if self.target and self.target.health > 0:
                # Движение к цели с учетом препятствий
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                dist = math.hypot(dx, dy)
                
                if dist > 0:
                    dx /= dist
                    dy /= dist
                    
                    # Проверяем препятствия на пути
                    if obstacles:
                        for obstacle in obstacles:
                            if not obstacle.passable:
                                obstacle_dist = math.hypot(obstacle.x - self.x, obstacle.y - self.y)
                                if obstacle_dist < self.size + obstacle.radius:
                                    # Рассчитываем вектор уклонения
                                    dodge_x = self.x - obstacle.x
                                    dodge_y = self.y - obstacle.y
                                    dodge_dist = math.hypot(dodge_x, dodge_y)
                                    if dodge_dist > 0:
                                        dodge_x /= dodge_dist
                                        dodge_y /= dodge_dist
                                        
                                        # Смешиваем вектор движения с вектором уклонения
                                        avoidance_weight = max(0, 1 - obstacle_dist / (self.size + obstacle.radius))
                                        dx = dx * (1 - avoidance_weight) + dodge_x * avoidance_weight
                                        dy = dy * (1 - avoidance_weight) + dodge_y * avoidance_weight
                                        
                                        # Нормализуем вектор
                                        new_dist = math.hypot(dx, dy)
                                        if new_dist > 0:
                                            dx /= new_dist
                                            dy /= new_dist
                    
                    # Применяем модификатор скорости от типа местности
                    effective_speed = self.speed * self.terrain_speed_mod
                    
                    # Двигаемся в направлении цели
                    self.x += dx * effective_speed
                    self.y += dy * effective_speed
                    
                    # Создаем частицы под ногами при движении
                    if random.random() < 0.08:
                        foot_x = self.x - dx * self.size * 0.7 + random.uniform(-10, 10)
                        foot_y = self.y - dy * self.size * 0.7 + random.uniform(-5, 5)
                        for _ in range(2):
                            dust_x = foot_x + random.uniform(-5, 5)
                            dust_y = foot_y + random.uniform(-3, 3)
                            self.particles.add(
                                dust_x, dust_y,
                                (160, 130, 80),
                                random.uniform(2, 5),
                                random.uniform(0.3, 1.0),
                                25,
                                gravity=-0.05
                            )
                
                # Атака
                if dist < self.attack_range and self.attack_cooldown <= 0:
                    # Выбираем тип атаки
                    if self.abilities["pound"]["unlocked"] and self.abilities["pound"]["current_cooldown"] <= 0 and random.random() < 0.15:
                        self.state = "pound"
                        self.state_timer = 60
                        self.abilities["pound"]["current_cooldown"] = self.abilities["pound"]["cooldown"]
                        self.invulnerable = True
                        self.invulnerable_timer = 60
                    elif self.abilities["throw"]["unlocked"] and self.abilities["throw"]["current_cooldown"] <= 0 and random.random() < 0.2:
                        self.state = "grab"
                        self.state_timer = 45
                        self.abilities["throw"]["current_cooldown"] = self.abilities["throw"]["cooldown"]
                        self.grabbed_human = self.target
                    elif random.random() < 0.8:  # Обычная атака
                        self.attack_type = "normal"
                        damage = self.attack_damage
                        is_critical = random.random() < 0.1
                        
                        if is_critical:
                            damage *= 2
                            for _ in range(7):
                                angle = random.uniform(0, 2*math.pi)
                                self.particles.add(
                                    self.target.x + math.cos(angle) * 10,
                                    self.target.y + math.sin(angle) * 10,
                                    (255, 255, 0),
                                    random.uniform(2, 4),
                                    random.uniform(1.5, 3),
                                    40,
                                    type="spark"
                                )
                                
                        self.target.health -= damage
                        self.target.take_damage(damage)
                        self.target.push_back(self.x, self.y, 5)
                        
                        # Брызги крови
                        impact_x = self.target.x
                        impact_y = self.target.y
                        for _ in range(5):
                            angle = random.uniform(0, 2*math.pi)
                            speed = random.uniform(1, 3)
                            self.particles.add(
                                impact_x,
                                impact_y,
                                RED,
                                random.uniform(1, 3),
                                speed,
                                30,
                                gravity=0.1
                            )
                            
                        self.attack_cooldown = 30
                        
                        # Если убили человека
                        if self.target.health <= 0:
                            self.kills += 1
                            self.gain_experience(10)  # Опыт за убийство
                            
                            for _ in range(8):
                                angle = random.uniform(0, 2*math.pi)
                                speed = random.uniform(1, 4)
                                self.particles.add(
                                    self.target.x + math.cos(angle) * 5,
                                    self.target.y + math.sin(angle) * 5,
                                    RED,
                                    random.uniform(2, 5),
                                    speed,
                                    40,
                                    gravity=0.1
                                )
                                
                            if self.kills % 30 == 0:
                                self.rage_mode = True
                                self.rage_timer = 300
                                self.speed = self.base_speed * 1.5
                                self.attack_damage = self.base_attack_damage * 1.8
                                
                                for _ in range(20):
                                    angle = random.uniform(0, 2*math.pi)
                                    distance = random.uniform(10, 50)
                                    self.particles.add(
                                        self.x + math.cos(angle) * distance,
                                        self.y + math.sin(angle) * distance,
                                        (255, 50, 0),
                                        random.uniform(3, 8),
                                        random.uniform(2, 5),
                                        60,
                                        type=random.choice(["circle", "spark"])
                                    )
                                    
                                for i in range(2):
                                    for angle in range(0, 360, 20):
                                        rad = math.radians(angle)
                                        dist = 20 + i * 20
                                        self.particles.add(
                                            self.x + math.cos(rad) * dist,
                                            self.y + math.sin(rad) * dist,
                                            (255, 100, 0),
                                            random.uniform(2, 5),
                                            random.uniform(0.5, 1.5),
                                            40,
                                            gravity=-0.1
                                        )
                                
                # Рев (отталкивает всех людей вокруг и оглушает их)
                if self.abilities["roar"]["unlocked"] and self.abilities["roar"]["current_cooldown"] <= 0 and random.random() < 0.01:
                    self.state = "roar"
                    self.state_timer = 90
                    self.abilities["roar"]["current_cooldown"] = self.abilities["roar"]["cooldown"]
                    self.invulnerable = True
                    self.invulnerable_timer = 60
                
                # Прыжок на дальнюю цель
                if self.abilities["leap"]["unlocked"] and self.abilities["leap"]["current_cooldown"] <= 0 and self.stamina >= 30:
                    # Ищем группу людей подальше
                    if spatial_hash:
                        distant_humans = []
                        for human in humans:
                            if human.health > 0:
                                dist = math.hypot(self.x - human.x, self.y - human.y)
                                if 200 < dist < 400:
                                    distant_humans.append(human)
                                    
                        if len(distant_humans) >= 5 and random.random() < 0.02:
                            # Выбираем случайного человека из группы
                            target_human = random.choice(distant_humans)
                            self.leap_target_x = target_human.x
                            self.leap_target_y = target_human.y
                            self.state = "leap"
                            self.state_timer = 90
                            self.leap_progress = 0
                            self.leap_height = 100
                            self.leap_speed = math.hypot(self.leap_target_x - self.x, self.leap_target_y - self.y) / 90
                            self.abilities["leap"]["current_cooldown"] = self.abilities["leap"]["cooldown"]
                            self.stamina -= 30  # Затраты стамины
                            
                            # Эффект начала прыжка
                            for _ in range(15):
                                angle = random.uniform(0, 2*math.pi)
                                distance = random.uniform(5, 20)
                                self.particles.add(
                                    self.x + math.cos(angle) * distance,
                                    self.y + math.sin(angle) * distance,
                                    (150, 150, 150),
                                    random.uniform(3, 8),
                                    random.uniform(1, 3),
                                    30,
                                    gravity=0.2
                                )
        
        elif self.state == "pound":
            # Удар кулаком по земле - наносит урон всем вокруг и создает ударную волну
            self.state_timer -= 1
            
            if self.state_timer == 30:  # Подготовка к удару
                for angle in range(0, 360, 15):
                    rad = math.radians(angle)
                    self.particles.add(
                        self.x + math.cos(rad) * 20,
                        self.y + math.sin(rad) * 20,
                        (255, 200, 0),
                        random.uniform(2, 5),
                        random.uniform(1, 2),
                        30,
                        type="spark"
                    )
            
            elif self.state_timer <= 0:  # Момент удара
                area_damage = self.attack_damage * 1.5
                pound_radius = self.attack_range * 2
                
                # Эффект ударной волны
                for i in range(3):
                    for angle in range(0, 360, 5):
                        rad = math.radians(angle)
                        dist = 20 + i * 30
                        speed = 3 + i * 2
                        self.particles.add(
                            self.x + math.cos(rad) * 10,
                            self.y + math.sin(rad) * 10,
                            (200, 150, 100),
                            random.uniform(3, 7),
                            speed,
                            40,
                            type="circle",
                            angle=rad,
                            spread=0.1
                        )
                
                # Зона урона
                nearby_humans = []
                if spatial_hash:
                    nearby_humans = spatial_hash.get_nearby(self.x, self.y, int(pound_radius / SPATIAL_HASH_CELL_SIZE) + 1)
                else:
                    nearby_humans = humans
                
                for human in nearby_humans:
                    if human.health > 0:
                        dist = math.hypot(self.x - human.x, self.y - human.y)
                        if dist < pound_radius:
                            # Урон зависит от расстояния
                            dist_factor = 1 - (dist / pound_radius)
                            actual_damage = area_damage * dist_factor
                            human.health -= actual_damage
                            
                            # Отбрасывание
                            force = 15 * dist_factor
                            human.push_back(self.x, self.y, force)
                            
                            # Оглушение
                            human.set_stunned(int(60 * dist_factor))
                            
                            if human.health <= 0:
                                self.kills += 1
                                self.gain_experience(10)
                                
                                # Эффект смерти
                                for _ in range(5):
                                    angle = random.uniform(0, 2*math.pi)
                                    self.particles.add(
                                        human.x + math.cos(angle) * 5,
                                        human.y + math.sin(angle) * 5,
                                        RED,
                                        random.uniform(2, 4),
                                        random.uniform(1, 3),
                                        30,
                                        gravity=0.1
                                    )
                
                # Сотрясение экрана (визуальный эффект)
                # (реализация через интерфейс)
                
                self.state = "idle"
        
        elif self.state == "grab":
            # Захват и бросок человека
            self.state_timer -= 1
            
            if self.grabbed_human and self.grabbed_human.health > 0:
                # Подготовка к броску
                if self.state_timer == 5:
                    for _ in range(5):
                        self.particles.add(
                            self.grabbed_human.x + random.uniform(-5, 5),
                            self.grabbed_human.y + random.uniform(-5, 5),
                            (255, 100, 50),
                            random.uniform(2, 4),
                            random.uniform(1, 2),
                            20,
                            type="spark"
                        )
                
                # Момент броска
                elif self.state_timer <= 0:
                    # Урон от броска
                    throw_damage = self.attack_damage * 1.2
                    self.grabbed_human.health -= throw_damage
                    
                    # Направление броска - можем бросить в других людей
                    throw_target = None
                    max_density = 0
                    
                    if spatial_hash:
                        for angle in range(0, 360, 45):
                            rad = math.radians(angle)
                            test_x = self.x + math.cos(rad) * 150
                            test_y = self.y + math.sin(rad) * 150
                            
                            nearby = spatial_hash.get_nearby(test_x, test_y, 1)
                            human_count = sum(1 for h in nearby if h.health > 0 and h != self.grabbed_human)
                            
                            if human_count > max_density:
                                max_density = human_count
                                throw_target = (test_x, test_y)
                    
                    if throw_target is None:
                        # Выбираем случайное направление
                        angle = random.uniform(0, 2*math.pi)
                        throw_target = (
                            self.x + math.cos(angle) * 150,
                            self.y + math.sin(angle) * 150
                        )
                    
                    # Вычисляем вектор броска
                    throw_dx = throw_target[0] - self.x
                    throw_dy = throw_target[1] - self.y
                    throw_dist = math.hypot(throw_dx, throw_dy)
                    
                    if throw_dist > 0:
                        throw_dx /= throw_dist
                        throw_dy /= throw_dist
                        
                        # Эффект броска
                        self.grabbed_human.push_velocity_x = throw_dx * 20
                        self.grabbed_human.push_velocity_y = throw_dy * 20
                        self.grabbed_human.push_damping = 0.95  # Меньше затухание для большей дистанции полета
                        
                        # Урон всем, в кого попадет брошенный человек
                        self.grabbed_human.set_thrown(throw_dx, throw_dy)
                    
                    # Визуальный эффект броска
                    for _ in range(10):
                        angle = math.atan2(throw_dy, throw_dx) + random.uniform(-0.3, 0.3)
                        speed = random.uniform(2, 5)
                        self.particles.add(
                            self.grabbed_human.x,
                            self.grabbed_human.y,
                            (200, 200, 200),
                            random.uniform(1, 3),
                            speed,
                            25,
                            type="spark",
                            angle=angle,
                            spread=0.3
                        )
                    
                    # Освобождаем человека
                    self.grabbed_human = None
                    self.state = "idle"
            else:
                # Если человек умер во время захвата
                self.grabbed_human = None
                self.state = "idle"
        
        elif self.state == "roar":
            # Рев гориллы - оглушает людей вокруг
            self.state_timer -= 1
            
            if self.state_timer == 60:  # Начало рева
                # Визуальный эффект начала рева
                for i in range(3):
                    for angle in range(0, 360, 10):
                        rad = math.radians(angle)
                        dist = 20 + i * 15
                        self.particles.add(
                            self.x + math.cos(rad) * dist,
                            self.y + math.sin(rad) * dist,
                            (255, 255, 200),
                            random.uniform(2, 4),
                            random.uniform(0.5, 1.5),
                            40,
                            type="circle"
                        )
            
            elif self.state_timer == 30:  # Пик рева
                roar_radius = self.attack_range * 3
                
                # Мощная ударная волна
                for i in range(4):
                    for angle in range(0, 360, 5):
                        rad = math.radians(angle)
                        dist = 30 + i * 25
                        speed = 4 + i
                        color = (255, 200, 100) if i % 2 == 0 else (255, 150, 50)
                        self.particles.add(
                            self.x + math.cos(rad) * 20,
                            self.y + math.sin(rad) * 20,
                            color,
                            random.uniform(3, 6),
                            speed,
                            50,
                            type="circle",
                            angle=rad,
                            spread=0.1
                        )
                
                # Оглушаем и отталкиваем всех людей в радиусе рева
                nearby_humans = []
                if spatial_hash:
                    nearby_humans = spatial_hash.get_nearby(self.x, self.y, int(roar_radius / SPATIAL_HASH_CELL_SIZE) + 1)
                else:
                    nearby_humans = humans
                
                for human in nearby_humans:
                    if human.health > 0:
                        dist = math.hypot(self.x - human.x, self.y - human.y)
                        if dist < roar_radius:
                            # Сила эффекта зависит от расстояния
                            dist_factor = 1 - (dist / roar_radius)
                            
                            # Отталкивание
                            force = 10 * dist_factor
                            human.push_back(self.x, self.y, force)
                            
                            # Оглушение
                            human.set_stunned(int(90 * dist_factor))
                            
                            # Люди в ужасе от рева
                            human.set_feared(int(180 * dist_factor))
            
            elif self.state_timer <= 0:
                self.state = "idle"
        
        elif self.state == "leap":
            # Прыжок на дальнюю цель
            self.state_timer -= 1
            self.leap_progress = 1 - (self.state_timer / 90)  # От 0 до 1
            
            # Перемещение по дуге прыжка
            if self.leap_target_x is not None and self.leap_target_y is not None:
                start_x = self.x
                start_y = self.y
                
                # Линейная интерполяция позиции
                self.x = start_x + (self.leap_target_x - start_x) * self.leap_progress
                self.y = start_y + (self.leap_target_y - start_y) * self.leap_progress
                
                # Добавляем вертикальную составляющую (параболу прыжка)
                vertical_offset = self.leap_height * math.sin(self.leap_progress * math.pi)
                
                # Не изменяем реальную позицию Y, эффект будет достигаться через отрисовку и тень
                
                # Частицы в воздухе
                if random.random() < 0.2:
                    angle = random.uniform(0, 2*math.pi)
                    self.particles.add(
                        self.x + random.uniform(-10, 10),
                        self.y + vertical_offset * 0.7 + random.uniform(-5, 5),
                        (200, 200, 200),
                        random.uniform(1, 3),
                        random.uniform(0.5, 1.5),
                        20,
                        gravity=0.1
                    )
            
            # Завершение прыжка
            if self.state_timer <= 0:
                # Урон в зоне приземления
                landing_radius = self.attack_range * 1.5
                landing_damage = self.attack_damage * 2.0
                
                # Визуальный эффект приземления
                for i in range(3):
                    for angle in range(0, 360, 5):
                        rad = math.radians(angle)
                        dist = 20 + i * 30
                        speed = 3 + i * 1.5
                        self.particles.add(
                            self.x + math.cos(rad) * 10,
                            self.y + math.sin(rad) * 10,
                            (200, 200, 150),
                            random.uniform(3, 6),
                            speed,
                            35,
                            type="circle",
                            angle=rad,
                            spread=0.1
                        )
                
                # Применяем урон всем людям в зоне приземления
                nearby_humans = []
                if spatial_hash:
                    nearby_humans = spatial_hash.get_nearby(self.x, self.y, int(landing_radius / SPATIAL_HASH_CELL_SIZE) + 1)
                else:
                    nearby_humans = humans
                
                for human in nearby_humans:
                    if human.health > 0:
                        dist = math.hypot(self.x - human.x, self.y - human.y)
                        if dist < landing_radius:
                            # Урон зависит от расстояния
                            dist_factor = 1 - (dist / landing_radius)
                            actual_damage = landing_damage * dist_factor
                            human.health -= actual_damage
                            
                            # Отбрасывание
                            force = 12 * dist_factor
                            human.push_back(self.x, self.y, force)
                            
                            # Оглушение
                            human.set_stunned(int(45 * dist_factor))
                            
                            if human.health <= 0:
                                self.kills += 1
                                self.gain_experience(10)
                                
                                # Эффект смерти
                                for _ in range(5):
                                    angle = random.uniform(0, 2*math.pi)
                                    self.particles.add(
                                        human.x + math.cos(angle) * 5,
                                        human.y + math.sin(angle) * 5,
                                        RED,
                                        random.uniform(2, 4),
                                        random.uniform(1, 3),
                                        30,
                                        gravity=0.1
                                    )
                
                # Сброс параметров прыжка
                self.leap_target_x = None
                self.leap_target_y = None
                self.state = "idle"
                
                # Короткий период неуязвимости после прыжка
                self.invulnerable = True
                self.invulnerable_timer = 30
        
        # Атака по области (сплэш)
        if self.area_attack_cooldown <= 0 and random.random() < 0.01 and self.state == "idle":
            targets_in_range = []
            if spatial_hash:
                nearby = spatial_hash.get_nearby(self.x, self.y, int(self.attack_range * 2 / SPATIAL_HASH_CELL_SIZE) + 1)
                for human in nearby:
                    if human.health > 0:
                        dist = math.hypot(self.x - human.x, self.y - human.y)
                        if dist < self.attack_range * 2:
                            targets_in_range.append(human)
            else:
                for human in humans:
                    if human.health > 0:
                        dist = math.hypot(self.x - human.x, self.y - human.y)
                        if dist < self.attack_range * 2:
                            targets_in_range.append(human)
                            
            if len(targets_in_range) >= 5:
                area_damage = self.attack_damage * 0.7
                for _ in range(20):
                    angle = random.uniform(0, 2*math.pi)
                    distance = random.uniform(20, self.attack_range * 2)
                    self.particles.add(
                        self.x + math.cos(angle) * distance,
                        self.y + math.sin(angle) * distance,
                        (255, 100, 50),
                        random.uniform(3, 6),
                        random.uniform(1, 3),
                        30,
                        type="spark"
                    )
                for angle in range(0, 360, 10):
                    rad = math.radians(angle)
                    self.particles.add(
                        self.x,
                        self.y,
                        (255, 50, 0),
                        random.uniform(5, 8),
                        random.uniform(3, 5),
                        40,
                        type="spark"
                    )
                for target in targets_in_range:
                    target.health -= area_damage
                    target.push_back(self.x, self.y, 10)
                    if target.health <= 0:
                        self.kills += 1
                        self.gain_experience(10)
                        if random.random() < 0.3:
                            angle = random.uniform(0, 2*math.pi)
                            self.particles.add(
                                target.x + math.cos(angle) * 5,
                                target.y + math.sin(angle) * 5,
                                RED,
                                random.uniform(2, 4),
                                random.uniform(1, 3),
                                30,
                                gravity=0.1
                            )
                self.area_attack_cooldown = 180

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.area_attack_cooldown > 0:
            self.area_attack_cooldown -= 1

        # Ограничиваем движение границами экрана
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))


class Human:
    def __init__(self, type_name=None):
        # Если тип не указан, выбираем случайно с учетом вероятностей
        if type_name is None:
            types = list(HUMAN_TYPES.keys())
            weights = [HUMAN_TYPES[t]['prob'] for t in types]
            type_name = random.choices(types, weights=weights)[0]
            
        self.type = type_name
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 12
        
        # Характеристики в зависимости от типа
        type_info = HUMAN_TYPES[self.type]
        self.speed = random.uniform(*type_info['speed'])
        self.health = type_info['health']
        self.max_health = self.health
        self.attack_range = 25
        self.attack_damage = type_info['damage']
        self.attack_cooldown = 0