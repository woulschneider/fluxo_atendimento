from PIL import Image, ImageDraw, ImageFont
import os

# Cria uma pasta para armazenar os frames
if not os.path.exists('frames'):
    os.makedirs('frames')

# Parâmetros do GIF
width, height = 800, 300
num_frames = 60
duration = 100  # 100 ms por frame

# Função para desenhar texto centralizado
def draw_text(draw, text, position, font, fill):
    w, h = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text((position[0] - w / 2, position[1] - h / 2), text, font=font, fill=fill)

# Fontes
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

# Cores
colors = {
    'Fetch': 'red',
    'Decode': 'yellow',
    'Execute': 'green',
    'background': 'white',
    'text': 'black'
}

# Posições fixas para os estágios do pipeline
positions = {
    'Fetch': (200, 150),
    'Decode': (400, 150),
    'Execute': (600, 150)
}

# Cria frames da animação
frames = []
for i in range(num_frames):
    frame = Image.new('RGB', (width, height), colors['background'])
    draw = ImageDraw.Draw(frame)
    
    # Desenha os estágios
    draw_text(draw, "Fetch", positions['Fetch'], font, colors['text'])
    draw_text(draw, "Decode", positions['Decode'], font, colors['text'])
    draw_text(draw, "Execute", positions['Execute'], font, colors['text'])
    
    # Movimentação das tarefas
    num_tasks = 3
    for j in range(num_tasks):
        task_position = (i - j * num_frames // num_tasks) % num_frames
        if task_position < num_frames // 3:
            stage = 'Fetch'
        elif task_position < 2 * num_frames // 3:
            stage = 'Decode'
        else:
            stage = 'Execute'
        
        task_x = positions[stage][0]
        task_y = positions[stage][1] + (j - 1) * 50
        
        draw.rectangle([task_x - 20, task_y - 20, task_x + 20, task_y + 20], fill=colors[stage], outline=colors['text'])
        draw_text(draw, f"Tarefa {j+1}", (task_x, task_y), font, colors['text'])
    
    frames.append(frame)
    frame.save(f'frames/frame_{i}.png')

# Salva os frames como um gif animado
frames[0].save('pipeline_animation.gif', save_all=True, append_images=frames[1:], duration=duration, loop=0)

print("GIF animado criado com sucesso!")
